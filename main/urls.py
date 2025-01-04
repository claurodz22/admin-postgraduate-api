from django.urls import path
from .views import PagosListAPIView, DatosBasicosCreateView, admin_login 
from . import views

'''
se utiliza igualmente que el archivo urls.py de la carpeta principal,
la diferencia es que este es un derivado del otro, de tal manera que este 
se llama en el otro archivo urls.py. Para acceder a la información de aca
en formato JSON (si fue establecido el metodo post / get) se utiliza el 
siguiente enlace: http://127.0.0.1:8000/api/pagos/ 

se le hace el añadido del /api/pagos/

de los tres disponibles (admin-login, pagos y datosbasicos) el unico
con metodo get es el de pagos (esto con objetivo de ver si se hacia 
la conexión de la bdd al front)
'''
urlpatterns = [
    path('admin-login/', admin_login, name='admin-login'),
    path('pagos/', PagosListAPIView.as_view(), name='pagos-list'),  
    path('datosbasicos/', views.DatosBasicosCreateView.as_view(), name='agregar_usuario')
]
