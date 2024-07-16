from rest_framework import serializers
from chat.models import Room, Message
from django.contrib.auth.models import User


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'user', 'user_name', 'room', 'mensagem']

    def get_user_name(self, obj):
        return obj.user.username if obj.user else None


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
