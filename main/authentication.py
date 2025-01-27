from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import datos_login
from rest_framework_simplejwt.tokens import AccessToken


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get('Authorization')
        
        if not auth:
            raise AuthenticationFailed('No authorization header provided')

        parts = auth.split()

        if parts[0].lower() != 'bearer' or len(parts) == 1:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        elif len(parts) > 2:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        token = parts[1]

        try:
            # Verificamos si el token es válido y obtenemos el payload
            payload = AccessToken(token)
        except Exception as e:
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

        # Usamos el payload del token para obtener el usuario
        try:
            user = datos_login.objects.get(id=payload['user_id'])
            
        except datos_login.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, token)  # Devuelve el usuario y el token

