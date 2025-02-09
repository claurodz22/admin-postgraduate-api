##
# @file urls.py
# @brief Configuración de las rutas URL de la API.
# 
# Este archivo define las rutas de la API para diferentes vistas y recursos del sistema. Estas rutas se incluyen en 
# el archivo principal `urls.py`, lo que permite que las URLs se expongan a través del servidor Django. 
# Las rutas son utilizadas para acceder a información y recursos de la API en formato JSON, mediante los métodos HTTP 
# establecidos (GET, POST, etc.).
# 
# Ejemplo: Para acceder a la información de los pagos, se utilizaría la URL: `http://127.0.0.1:8000/api/pagos/`.
# 
# Las siguientes rutas están disponibles en esta sección:
# - `profe-materias/`
# - `api/token/`
# - `listado_estudiantes/`
# - `almacenarestudiante/`
# - `obtenerdatos/`
# - `pagos/`
# - `admin-login/`
#


from django.urls import path
from .views import ListadoEstudiantes,CohorteListAPIView, PlanificacionProfesorAPIView, ProfMaterias, login_profesor, verificar_codigo_cohorte, generar_codigo_cohorte, PagosListAPIView, DatosBasicosCreateView, admin_login, SolicitudesListAPIView, BuscarCedulaEstView, AlmacenarDatosEstView 
from . import views
from .views import UserInfoView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

## @brief Rutas de la API para el acceso a los recursos de la aplicación.
# Estas rutas permiten a los usuarios interactuar con los recursos de la aplicación, como el login de administradores y 
# profesores, la obtención de datos básicos y la verificación de códigos de cohorte.
# 
# @note Las rutas están definidas bajo el prefijo '/api/', permitiendo el acceso a los datos en formato JSON 
# o XML, dependiendo del método HTTP utilizado (GET, POST, etc.).
# 
# @example La ruta 'http://127.0.0.1:8000/api/pagos/' accede a los pagos.
urlpatterns = [
    ## @route /profe-materias/
    # @brief Ruta para obtener las materias de un profesor.
    # @note Se requiere autenticación para acceder a esta ruta.
    # @see ProfMaterias
    path('profe-materias/', ProfMaterias.as_view(), name='profe-materias'),

    path('cohortes/', CohorteListAPIView.as_view(), name='cohortes'),

    path('profe-plan/', PlanificacionProfesorAPIView.as_view(), name='profe-plan'),
        
    ## @route /api/token/
    # @brief Ruta para obtener un token de acceso.
    # @note Esta ruta permite la autenticación mediante JWT, generando un token de acceso válido.
    # @see TokenObtainPairView
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    ## @route /api/token/refresh/
    # @brief Ruta para refrescar un token de acceso.
    # @note Permite obtener un nuevo token de acceso mediante el uso de un token de actualización válido.
    # @see TokenRefreshView
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    ## @route /user-info/
    # @brief Ruta para obtener información sobre el usuario autenticado.
    # @note Solo se puede acceder si el usuario está autenticado.
    # @see UserInfoView
    path('user-info/', UserInfoView.as_view(), name='user-info'),
    
    ## @route /verificar-codigo-cohorte/
    # @brief Ruta para verificar un código de cohorte.
    # @see verificar_codigo_cohorte
    path('verificar-codigo-cohorte/', views.verificar_codigo_cohorte, name='verificar_codigo_cohorte'),
    
    ## @route /cohorte-generar-codigo/
    # @brief Ruta para generar un código de cohorte.
    # @see generar_codigo_cohorte
    path('cohorte-generar-codigo/', views.generar_codigo_cohorte, name='generar_codigo_cohorte'),
    
    ## @route /listado_estudiantes/
    # @brief Ruta para obtener un listado de estudiantes.
    # @see ListadoEstudiantes
    path('listado_estudiantes/', ListadoEstudiantes.as_view(), name='almacenarest-list'),
    
    ## @route /almacenarestudiante/
    # @brief Ruta para almacenar o actualizar los datos de un estudiante.
    # @see AlmacenarDatosEstView
    path('almacenarestudiante/', AlmacenarDatosEstView.as_view(), name='almacenarest-list'),
    
    ## @route /obtenerdatos/
    # @brief Ruta para obtener los datos de un estudiante mediante su cédula.
    # @see BuscarCedulaEstView
    path('obtenerdatos/', BuscarCedulaEstView.as_view(), name='obtenerdatos-list'),
    
    ## @route /solicitudes/
    # @brief Ruta para obtener la lista de solicitudes.
    # @see SolicitudesListAPIView
    path('solicitudes/', SolicitudesListAPIView.as_view(), name='solicitudes-list'),
    
    ## @route /admin-login/
    # @brief Ruta para el login de administrador.
    # @see admin_login
    path('admin-login/', admin_login, name='admin-login'),
    
    ## @route /login_profesor/
    # @brief Ruta para el login de profesor.
    # @see login_profesor
    path('login_profesor/', login_profesor, name='login_profesor'),
    
    ## @route /pagos/
    # @brief Ruta para obtener la lista de pagos.
    # @see PagosListAPIView
    path('pagos/', PagosListAPIView.as_view(), name='pagos-list'),  
    
    ## @route /datosbasicos/
    # @brief Ruta para agregar un nuevo usuario con datos básicos.
    # @see DatosBasicosCreateView
    path('datosbasicos/', views.DatosBasicosCreateView.as_view(), name='agregar_usuario')
]
