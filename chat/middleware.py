from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpRequest
from rest_framework.exceptions import AuthenticationFailed

def get_user_from_access_token(access_token):
    try:
        # Criar uma instância de JWTAuthentication
        jwt_authentication = JWTAuthentication()

        # Criar um objeto HttpRequest simulado para a autenticação
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        # Autenticar o token e obter o usuário associado
        user, token = jwt_authentication.authenticate(request)

        return user
    except AuthenticationFailed as e:
        print(f"Erro ao autenticar token: {str(e)}")
        return None
    except Exception as e:
        print(f"Erro ao autenticar token: {str(e)}")
        return None
