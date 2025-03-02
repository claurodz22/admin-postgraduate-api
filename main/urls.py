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


from django.http import HttpRequest
from django.urls import path
from .views import *
from . import views
from .views import UserInfoView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from rest_framework import routers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


@permission_classes([AllowAny])
@api_view(["*"])
def test(request: HttpRequest):
    print("test")
    return JsonResponse(
        {"test": "ok", "req_method": request.method},
        status=200,
    )


router = routers.DefaultRouter()
router.register("maestrias", DatosMaestriaViewSet)
## @brief Rutas de la API para el acceso a los recursos de la aplicación.
# Estas rutas permiten a los usuarios interactuar con los recursos de la aplicación, como el login de administradores y
# profesores, la obtención de datos básicos y la verificación de códigos de cohorte.
#
# @note Las rutas están definidas bajo el prefijo '/api/', permitiendo el acceso a los datos en formato JSON
# o XML, dependiendo del método HTTP utilizado (GET, POST, etc.).
#
# @example La ruta 'http://127.0.0.1:8000/api/pagos/' accede a los pagos.
urlpatterns = [
    
    # @route /actualizar-pago/
    # @brief Ruta para actualizar el estado de pago de los usuarios.
    # @note Permite modificar el estado de pago de uno o varios usuarios en el sistema.
    # @see actualizar_estado_pagos
    path(
        'actualizar-pago/' , 
        actualizar_estado_pagos, 
        name='actualizar-pago'
    ),

    # @route /listar_usuarios/
    # @brief Ruta para listar usuarios por tipo.
    # @note Proporciona una lista de usuarios filtrada por el tipo de usuario especificado.
    # @see UsuariosPorTipoAPIView
    path(
        'listar_usuarios/', 
        UsuariosPorTipoAPIView.as_view(), 
        name='api_usuarios'
    ),

    # @route /eliminar-usuarios/
    # @brief Ruta para eliminar usuarios seleccionados.
    # @note Permite eliminar uno o varios usuarios del sistema basado en los IDs proporcionados.
    # @see eliminar_usuarios
    path(
        'eliminar-usuarios/', 
         eliminar_usuarios, 
         name='eliminar_usuarios'
    ),

    ## @route /asignar-profesor-materia/
    # @brief Ruta para asignar un profesor a una materia.
    # @note Permite vincular a un profesor con una materia específica dentro del sistema.
    # @see AsignarProfesorMateriaView
    path(
        "asignar-profesor-materia/",
        AsignarProfesorMateriaView.as_view(),
        name="asignar_profesor_materia",
    ),
    
    ## @route /listado-materias/
    # @brief Ruta para obtener el listado de materias disponibles.
    # @note Devuelve una lista con todas las materias registradas en el sistema.
    # @see MateriasPensumAPIView
    path("listado-materias/", MateriasPensumAPIView.as_view(), name="listado-materias"),

    ## @route /listado-profesores/
    # @brief Ruta para obtener el listado de profesores registrados.
    # @note Devuelve una lista con los datos de los profesores disponibles en el sistema.
    # @see ProfesoresAPIView
    path("listado-profesores/", ProfesoresAPIView.as_view(), name="listado-profesores"),

    ## @route /cohortes/
    # @brief Ruta para obtener la lista de cohortes disponibles.
    # @note Devuelve la información de los cohortes registrados en el sistema.
    # @see CohorteListAPIView
    path("cohortes/", CohorteListAPIView.as_view(), name="cohortes"),

    ## @route /profe-plan/
    # @brief Ruta para gestionar la planificación de los profesores.
    # @note Permite registrar y consultar la planificación académica de los profesores.
    # @see PlanificacionProfesorAPIView
    path("profe-plan/", PlanificacionProfesorAPIView.as_view(), name="profe-plan"),

    ## @route /profe-materias/
    # @brief Ruta para obtener las materias de un profesor.
    # @note Se requiere autenticación para acceder a esta ruta.
    # @see ProfMaterias
    path("profe-materias/", ProfMaterias.as_view(), name="profe-materias"),

    ## @route /api/token/
    # @brief Ruta para obtener un token de acceso.
    # @note Esta ruta permite la autenticación mediante JWT, generando un token de acceso válido.
    # @see TokenObtainPairView
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),

    ## @route /api/token/refresh/
    # @brief Ruta para refrescar un token de acceso.
    # @note Permite obtener un nuevo token de acceso mediante el uso de un token de actualización válido.
    # @see TokenRefreshView
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    ## @route /user-info/
    # @brief Ruta para obtener información sobre el usuario autenticado.
    # @note Solo se puede acceder si el usuario está autenticado.
    # @see UserInfoView
    path("user-info/", UserInfoView.as_view(), name="user-info"),

    ## @route /verificar-codigo-cohorte/
    # @brief Ruta para verificar un código de cohorte.
    # @see verificar_codigo_cohorte
    path(
        "verificar-codigo-cohorte/",
        verificar_codigo_cohorte,
        name="verificar_codigo_cohorte",
    ),

    ## @route /cohorte-generar-codigo/
    # @brief Ruta para generar un código de cohorte.
    # @see generar_codigo_cohorte
    path(
        "cohorte-generar-codigo/",
        generar_codigo_cohorte,
        name="generar_codigo_cohorte",
    ),

    ## @route /listado_estudiantes/
    # @brief Ruta para obtener un listado de estudiantes.
    # @see ListadoEstudiantes
    path(
        "listado_estudiantes/", ListadoEstudiantes.as_view(), name="almacenarest-list"
    ),

    ## @route /almacenarestudiante/
    # @brief Ruta para almacenar o actualizar los datos de un estudiante.
    # @see AlmacenarDatosEstView
    path(
        "almacenarestudiante/",
        AlmacenarDatosEstView.as_view(),
        name="almacenarest-list",
    ),

    ## @route /obtenerdatos/
    # @brief Ruta para obtener los datos de un estudiante mediante su cédula.
    # @see BuscarCedulaEstView
    path("obtenerdatos/", BuscarCedulaEstView.as_view(), name="obtenerdatos-list"),

    ## @route /solicitudes/
    # @brief Ruta para obtener la lista de solicitudes.
    # @see SolicitudesListAPIView
    path("solicitudes/", SolicitudesListAPIView.as_view(), name="solicitudes-list"),

    ## @route /admin-login/
    # @brief Ruta para el login de administrador.
    # @see admin_login
    path("admin-login/", admin_login, name="admin-login"),

    ## @route /login_profesor/
    # @brief Ruta para el login de profesor.
    # @see login_profesor
    path("login_profesor/", login_profesor, name="login_profesor"),

    # @route /login_estudiante/
    # @brief Ruta para el inicio de sesión de estudiantes.
    # @note Maneja la autenticación y el inicio de sesión específico para usuarios con rol de estudiante.
    # @see login_estudiante
    path("login_estudiante/", views.login_estudiante, name="login_estudiante"),

    ## @route /pagos/
    # @brief Ruta para obtener la lista de pagos.
    # @see PagosListAPIView
    path("pagos/", PagosListAPIView.as_view(), name="pagos-list"),

    ## @route /datosbasicos/
    # @brief Ruta para agregar un nuevo usuario con datos básicos.
    # @see DatosBasicosCreateView
    path("datosbasicos/", DatosBasicosCreateView.as_view(), name="agregar_usuario"),

    # @route /datos-maestria/
    # @brief Ruta para obtener datos de las maestrías.
    # @note Proporciona una lista de todas las maestrías disponibles y sus detalles asociados.
    # @see DatosMaestriaViewSet
    path(
        "datos-maestria/",
        views.DatosMaestriaViewSet.as_view({"get": "list"}),
        name="datos-maestria",
    ),


    path("test/", test),

    
] + router.urls
