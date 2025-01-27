from django.urls import path
from .views import ListadoEstudiantes, ProfMaterias, AdminProfesorView, admin_profesor, verificar_codigo_cohorte, generar_codigo_cohorte, PagosListAPIView, DatosBasicosCreateView, admin_login, SolicitudesListAPIView, BuscarCedulaEstView, AlmacenarDatosEstView 
from . import views
from .views import UserInfoView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

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
    path('profe-materias/', ProfMaterias.as_view(), name='profe-materias'),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    path('verificar-codigo-cohorte/', views.verificar_codigo_cohorte, name='verificar_codigo_cohorte'),
    path('cohorte-generar-codigo/', views.generar_codigo_cohorte, name='generar_codigo_cohorte'),
    path('listado_estudiantes/', ListadoEstudiantes.as_view(), name='almacenarest-list'),
    path('almacenarestudiante/', AlmacenarDatosEstView.as_view(), name='almacenarest-list'),
    path('obtenerdatos/', BuscarCedulaEstView.as_view(), name='obtenerdatos-list'),
    path('solicitudes/', SolicitudesListAPIView.as_view(), name='solicitudes-list'),
    path('admin-login/', admin_login, name='admin-login'),
    path('admin-profe/', admin_profesor, name='admin_profesor'),
    # path('admin-profe/', AdminProfesorView.as_view(), name='admin_profesor'),
    path('pagos/', PagosListAPIView.as_view(), name='pagos-list'),  
    path('datosbasicos/', views.DatosBasicosCreateView.as_view(), name='agregar_usuario')
]
