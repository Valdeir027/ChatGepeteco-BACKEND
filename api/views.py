from rest_framework import viewsets
from chat.models import Room, Message
from .serializers import RoomSerializer, UserSerializer,MessageSerializer
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.decorators import action
from rest_framework import serializers

class RoomViewSet(viewsets.ModelViewSet):
  queryset = Room.objects.all()
  serializer_class = RoomSerializer

class MessageList(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['get'])
    def by_room(self, request, *args, **kwargs):
        room_id = request.query_params.get('room_id', None)
        if room_id is not None:
            messages = self.queryset.filter(room__id=room_id)
            serializer = self.get_serializer(messages, many=True)
            return Response(serializer.data)
        else:
            return Response({"error": "room_id is required"}, status=400)


class RegisterView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  permission_classes = (permissions.AllowAny, )

  def create(self, request, *args, **kwargs):
    response = super().create(request, *args, **kwargs)
    user = User.objects.get(username=response.data['username'])
    refresh = RefreshToken.for_user(user)
    return Response({
        'user': response.data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        # Add custom response data here
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email
        }
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer