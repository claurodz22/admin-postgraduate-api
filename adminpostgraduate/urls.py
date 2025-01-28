##
# @file urls.py
# @brief Configuración de las URLs del proyecto "adminpostgraduate".
#
# Este archivo contiene la configuración de URLs del proyecto Django para enrutar solicitudes a vistas específicas.
# La lista `urlpatterns` define las rutas que mapean las URLs a vistas y otras configuraciones relacionadas. 
# Este archivo se utiliza para configurar las rutas a las vistas y APIs de la aplicación, como se especifica en
# la documentación oficial de Django. 
#
# @see Django Docs: https://docs.djangoproject.com/en/stable/topics/http/urls/
#

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # Vista para obtener el token de acceso
    TokenRefreshView,     # Vista para refrescar el token de acceso
    TokenVerifyView       # Vista para verificar la validez del token
)
# Se puede agregar una vista para registrar usuarios si es necesario.
#from .views import RegisterUserView

'''
Comentario adicional:
El archivo "urls.py" contiene las rutas de la aplicación. Para acceder a las vistas o a las APIs de la aplicación, 
se debe agregar el segmento de la URL correspondiente a la URL base de la aplicación. 

Por ejemplo:
    - URL base: http://127.0.0.1:8000/
    - Para acceder a la vista del admin: http://127.0.0.1:8000/admin/
    - Para acceder a la API definida en "main.urls": http://127.0.0.1:8000/api/
'''

urlpatterns = [
    # Ruta para incluir las URLs de la aplicación "main"
    path('api/', include('main.urls')),  # Se incluyen las URLs del archivo main.urls
    
    # Rutas comentadas para acceder a las vistas relacionadas con JWT y registro de usuario.
    #path('admin/', admin.site.urls),  # Descomentar si se desea acceder a la interfaz de administración de Django
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Vista para obtener el token JWT
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Vista para refrescar el token JWT
    #path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),  # Vista para verificar el token JWT
    #path('register/', RegisterUserView.as_view(), name='register'),  # Vista para registrar nuevos usuarios
]
