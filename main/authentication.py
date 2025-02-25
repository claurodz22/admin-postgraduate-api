##
# @file authentication.py
# @brief Implementación de autenticación personalizada para manejar JWT en la API.
#
# Este archivo contiene la implementación de un sistema de autenticación personalizada utilizando
# JSON Web Tokens (JWT) en el framework Django REST. La clase `CustomJWTAuthentication` hereda de 
# `BaseAuthentication` de Django REST Framework y se utiliza para verificar la validez de un token JWT
# proporcionado en los encabezados de las solicitudes HTTP. Si el token es válido, se obtiene el usuario
# correspondiente y se permite el acceso a la API.
#
# @see Django REST Framework
# @see JWT (JSON Web Token)
# @see `rest_framework_simplejwt`
#

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import datos_login
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import AllowAny


class CustomJWTAuthentication(BaseAuthentication):
    """
    @brief Clase de autenticación personalizada para manejar JWT (JSON Web Token).
    
    Esta clase extiende `BaseAuthentication` de Django REST Framework para implementar una
    autenticación personalizada utilizando el esquema de token Bearer. El token debe estar incluido
    en el encabezado `Authorization` de la solicitud. Se valida el token, se extrae el payload y 
    se obtiene el usuario correspondiente.
    
    @throws AuthenticationFailed Si el token no es válido o el usuario no existe.
    """

    def authenticate(self, request):
        """
        @brief Autentica a un usuario basado en el token JWT proporcionado en la solicitud.
        
        Este método verifica si el encabezado `Authorization` contiene un token Bearer válido.
        Si el token es válido, se obtiene el usuario correspondiente y se devuelve junto con el token.
        
        @param request Solicitud HTTP que contiene el encabezado `Authorization`.
        
        @return Tuple: Un par (usuario, token) si la autenticación es exitosa.
        
        @throws AuthenticationFailed Si no se encuentra el encabezado `Authorization` o si el token es inválido.
        """
        
        # Obtener el valor del encabezado 'Authorization' de la solicitud
        auth = request.headers.get('Authorization')
        
        if self.has_allow_any_permission(request):
            return None
        # Verificar si se proporcionó el encabezado de autorización
        if not auth:
            raise AuthenticationFailed('No authorization header provided')

        # Separar el encabezado para obtener el tipo de token y el token en sí
        parts = auth.split()

        # Verificar si el encabezado sigue el formato 'Bearer <token>'
        if parts[0].lower() != 'bearer' or len(parts) == 1:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        elif len(parts) > 2:
            raise AuthenticationFailed('Authorization header must be Bearer token')

        # Obtener el token del encabezado
        token = parts[1]

        try:
            # Verificar si el token es válido y obtener el payload
            payload = AccessToken(token)
        except Exception as e:
            # Si el token es inválido, lanzar una excepción con el mensaje de error
            raise AuthenticationFailed(f'Invalid token: {str(e)}')

        # Usar el payload del token para obtener el usuario correspondiente
        try:
            user = datos_login.objects.get(id=payload['user_id'])
            
        except datos_login.DoesNotExist:
            # Si no se encuentra el usuario asociado al token, lanzar una excepción
            raise AuthenticationFailed('User not found')

        # Si la autenticación es exitosa, devolver el usuario y el token
        return (user, token)
    def has_allow_any_permission(self, request):   
        # Acceder a la vista actual
        view = request.resolver_match.func  # Esto puede variar según tu configuración
        
        # Obtener los permisos aplicados a la vista
        permissions = getattr(view, 'permission_classes', [])
        
        # Comprobar si AllowAny está en los permisos
        return AllowAny in permissions
