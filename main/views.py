##
# @file views.py
# @brief Vistas de la API para manejar la lógica del negocio y los datos.
#
# Este archivo contiene las vistas que definen la lógica de negocio para interactuar con los modelos
# de la base de datos y devolver respuestas en formato JSON o XML a través de la API.
# Las vistas están diseñadas para manejar operaciones CRUD, autenticación, autorización
# y otros procesos relacionados con el sistema.
#
# Las vistas están implementadas utilizando el framework Django Rest Framework (DRF)
# y las clases de vista genéricas de DRF, como `APIView`, que permiten la creación de
# vistas basadas en clases para simplificar la gestión de los métodos HTTP (GET, POST, PUT, DELETE).
#
# @note Este archivo es clave para la interacción entre el frontend y el backend,
# ya que procesa las solicitudes y devuelve las respuestas adecuadas.
#
# @example Para obtener los datos básicos de un estudiante, la ruta correspondiente
# invoca la vista `DatosBasicosCreateView` definida en este archivo.
#
# @see Django Rest Framework
# @see APIView
#
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import AsignarProfesorMateria
from .serializers import AsignarProfesorMateriaSerializer

class AsignarProfesorMateriaView(APIView):
    """
    @class AsignarProfesorMateriaView
    @brief Vista para asignar un profesor a una materia y listar asignaciones.
    """

    def get(self, request):
        """
        @brief Obtiene todas las asignaciones de profesores a materias.
        @param request Petición HTTP.
        @return Response con los datos de las asignaciones.
        """
        asignaciones = AsignarProfesorMateria.objects.all()
        serializer = AsignarProfesorMateriaSerializer(asignaciones, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea nuevas asignaciones de profesor a materia.
        @param request Petición HTTP con los datos de planificación.
        @return Response con las asignaciones creadas o errores.
        """
        planning_data = request.data.get('planning', [])
        if not planning_data:
            return Response({"detail": "No se proporcionaron datos de planificación."}, status=status.HTTP_400_BAD_REQUEST)

        created_assignments = []
        errors = []

        for item in planning_data:
            serializer = AsignarProfesorMateriaSerializer(data=item)
            if serializer.is_valid():
                serializer.save()
                created_assignments.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"created": created_assignments}, status=status.HTTP_201_CREATED)


# ----------- CLASE: MATERIAS PENSUM ----------------
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import materias_pensum
from .serializers import MateriasPensumSerializer

class MateriasPensumAPIView(APIView):
    """
    @class MateriasPensumAPIView
    @brief API View para listar y registrar materias del pensum de cada maestría.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        @brief Obtiene la lista de todas las materias del pensum.
        @param request Petición HTTP.
        @return Response con la lista de materias.
        """
        materias = materias_pensum.objects.all()
        serializer = MateriasPensumSerializer(materias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        @brief Crea una nueva materia en el pensum.
        @param request Petición HTTP con los datos de la materia.
        @return Response con la materia creada o errores de validación.
        """
        serializer = MateriasPensumSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
---------------CLASE: PROFESORES-------------------
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import profesores
from .serializers import ProfesoresSerializer

class ProfesoresAPIView(APIView):
    """
    @brief Clase que gestiona los profesores mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros de profesores.
    """

    def get(self, request):
        """
        @brief Recupera todos los profesores registrados en la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de profesores en formato JSON.
        """
        Profes = profesores.objects.all()  # Recupera todos los registros de profesores
        print(profesores)
        serializer = ProfesoresSerializer(Profes, many=True)  # Serializa los datos para su retorno en formato JSON
    
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea un nuevo registro de profesor en la base de datos.
        @param request Objeto HTTP Request que contiene los datos del nuevo profesor en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna el profesor creado y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        serializer = ProfesoresSerializer(data=request.data)  # Deserializa los datos enviados en la solicitud
        if serializer.is_valid():  # Valida los datos recibidos
            serializer.save()  # Guarda el nuevo registro en la base de datos
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # Retorna el registro creado
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Retorna errores si la validación falla




"""
------------------CLASE: LISTADOS COHORTE---------------------
"""
import sys
import traceback
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Cohorte, Roles
from .serializers import CohorteSerializer, DatosMaestriaSerializer

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsPublic(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios con rol ...
    """

    def has_permission(self, request, view):
        return True


class IsProfesor(permissions.BasePermission):
    """
    Permiso personalizado que permite el acceso solo a usuarios con rol ...
    """

    def has_permission(self, request, view):
        # Verifica si el usuario está autenticado y tiene el rol adecuado
        if not request.user.is_authenticated:
            raise PermissionDenied("Usuario no autenticado")

        if (
            not getattr(request.user, "tipo_usuario", None).codigo_rol
            == Roles.PROFESOR.value
        ):
            raise PermissionDenied("Recurso requiere privilegios de profesor.")

        return True


class CohorteListAPIView(APIView):
    """
    @brief Clase que gestiona los cohortes mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros de cohortes.
    """

    permission_classes = [permissions.IsAuthenticated, IsProfesor]

    def get(self, request):
        """
        @brief Recupera todos los cohortes registrados en la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de cohortes en formato JSON.
        """
        cohortes = Cohorte.objects.all()  # Recupera todos los registros de cohortes
        serializer = CohorteSerializer(
            cohortes, many=True
        )  # Serializa los datos para su retorno en formato JSON
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea un nuevo registro de cohorte en la base de datos.
        @param request Objeto HTTP Request que contiene los datos del nuevo cohorte en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna el cohorte creado y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        serializer = CohorteSerializer(
            data=request.data
        )  # Deserializa los datos enviados en la solicitud
        if serializer.is_valid():  # Valida los datos recibidos
            serializer.save()  # Guarda el nuevo registro en la base de datos
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Retorna el registro creado
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Retorna errores si la validación falla


"""
------------------CLASE: PLANIFICACION PROFESOR---------------------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import PlanificacionProfesor
from .serializers import PlanificacionProfesorSerializer


class PlanificacionProfesorAPIView(APIView):
    """
    @brief Clase que gestiona la planificación de profesores mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros en la tabla de planificación de profesores.
    """

    def get(self, request):
        """
        @brief Recupera todas las planificaciones de profesores registradas en la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de planificaciones en formato JSON.
        """
        planificaciones = (
            PlanificacionProfesor.objects.all()
        )  # Recupera todos los registros de planificación
        serializer = PlanificacionProfesorSerializer(
            planificaciones, many=True
        )  # Serializa los datos
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea un nuevo registro de planificación en la base de datos.
        @param request Objeto HTTP Request que contiene los datos de la planificación en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna la planificación creada y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        serializer = PlanificacionProfesorSerializer(
            data=request.data
        )  # Deserializa los datos enviados en la solicitud
        if serializer.is_valid():  # Valida los datos recibidos
            serializer.save()  # Guarda el nuevo registro en la base de datos
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Retorna el registro creado
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Retorna errores si la validación falla


"""
------------------CLASE: LISTADO ESTUDIANTES---------------------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request

from rest_framework import status
from .models import listado_estudiantes
from .serializers import ListadoEstudiantesSerializer


class ListadoEstudiantes(APIView):
    """Clase para recuperar listado de estudiantes para el frontend
    de control de notas en el administrador.

    Esta clase define los métodos GET y POST para interactuar con los datos
    relacionados con estudiantes.
    """

    def get(self, request):
        """Método GET: Para obtener todos los estudiantes.

        Este método recupera todos los estudiantes y filtra opcionalmente
        por `q_code` o `m_code` recibidos como parámetros de consulta.

        @param self: Referencia a la instancia de la clase.
        @param request: Objeto Request que contiene los datos de la solicitud.
        @return: Una respuesta JSON con la lista de estudiantes.
        """
        q_code = request.query_params.get("q_code")
        m_code = request.query_params.get("m_code")
        estudiantes = listado_estudiantes.objects.all()
        if q_code:
            estudiantes = estudiantes.filter(codigo_cohorte=q_code)
        if m_code:
            estudiantes = estudiantes.filter(cod_materia=m_code)
        serializer = ListadoEstudiantesSerializer(estudiantes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """Método POST: Para agregar un estudiante nuevo.

        Este método permite agregar un nuevo estudiante al listado.

        @param self: Referencia a la instancia de la clase.
        @param request: Objeto Request que contiene los datos de la solicitud.
        @return: Una respuesta JSON con los datos del estudiante creado si es válido,
                 o un error con el código de estado correspondiente.
        """
        serializer = ListadoEstudiantesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
--------FUNCIONES PARA GENERAR CÓDIGO DEL COHORTE----------
"""
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Cohorte
from .serializers import CohorteSerializer
import datetime


@api_view(["POST"])
def generar_codigo_cohorte(request):
    """
    @brief Genera un código único para una nueva cohorte y la registra en la base de datos.
    @param request Objeto HTTP Request con los datos necesarios para crear la cohorte:
        - codigo_cohorte: Código inicial de la cohorte.
        - fecha_inicio: Fecha de inicio de la cohorte en formato 'YYYY-MM-DD'.
        - fecha_fin: Fecha de fin de la cohorte en formato 'YYYY-MM-DD'.
        - sede_cohorte: Sede de la cohorte.
        - tipo_maestria: Tipo de maestría asociada a la cohorte.
    @return Response con el código generado si el registro fue exitoso, o JsonResponse con un error en caso contrario.
    """
    if request.method == "POST":
        codigo_cohorte = request.data.get("codigo_cohorte")
        fecha_inicio = request.data.get("fecha_inicio")
        fecha_fin = request.data.get("fecha_fin")
        sede_cohorte = request.data.get("sede_cohorte")
        tipo_maestria = request.data.get("tipo_maestria")

        # Función para generar un nuevo código
        def generate_new_code(code):
            """
            @brief Genera un nuevo código único basado en el código proporcionado.
            @param code Código inicial de la cohorte.
            @return Nuevo código generado.
            """
            prefix = code[
                :-6
            ]  # Toma todo excepto los últimos 6 caracteres (ej. FIIA-2024 -> FII)
            year = code[-4:]  # Toma los últimos 4 caracteres (el año)
            current_letter = code[-6]  # Toma la letra actual (A, B, C, etc.)
            next_letter = chr(ord(current_letter) + 1)  # Genera la siguiente letra
            return f"{prefix}{next_letter}-{year}"

        # Verifica si el código de cohorte ya existe
        while Cohorte.objects.filter(codigo_cohorte=codigo_cohorte).exists():
            codigo_cohorte = generate_new_code(codigo_cohorte)

        # Crea el nuevo cohorte
        try:
            cohorte = Cohorte.objects.create(
                codigo_cohorte=codigo_cohorte,
                fecha_inicio=datetime.datetime.strptime(fecha_inicio, "%Y-%m-%d"),
                fecha_fin=datetime.datetime.strptime(fecha_fin, "%Y-%m-%d"),
                sede_cohorte=sede_cohorte,
                tipo_maestria=tipo_maestria,
            )
            serializer = CohorteSerializer(cohorte)
            return Response({"codigo_cohorte": codigo_cohorte}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


@api_view(["POST"])
def verificar_codigo_cohorte(request):
    """
    @brief Verifica si un código de cohorte ya existe en la base de datos y genera uno nuevo si es necesario.
    @param request Objeto HTTP Request con los datos necesarios:
        - codigo_cohorte: Código de cohorte a verificar.
    @return JsonResponse indicando si el código ya existe y, en caso positivo, sugiere un nuevo código.
    """
    if request.method == "POST":
        codigo_cohorte = request.data.get("codigo_cohorte")

        if not codigo_cohorte:
            return JsonResponse(
                {"error": "Código de cohorte no proporcionado"}, status=400
            )

        # Función para generar un nuevo código
        def generate_new_code(code):
            """
            @brief Genera un nuevo código único basado en el código proporcionado.
            @param code Código inicial de la cohorte.
            @return Nuevo código generado.
            """
            prefix = code[
                :-6
            ]  # Toma todo excepto los últimos 6 caracteres (ej. FIIA-2024 -> FII)
            year = code[-4:]  # Toma los últimos 4 caracteres (el año)
            current_letter = code[-6]  # Toma la letra actual (A, B, C, etc.)
            next_letter = chr(ord(current_letter) + 1)  # Genera la siguiente letra
            return f"{prefix}{next_letter}-{year}"

        # Verifica si el código de cohorte ya existe
        if Cohorte.objects.filter(codigo_cohorte=codigo_cohorte).exists():
            new_code = generate_new_code(codigo_cohorte)
            return JsonResponse({"exists": True, "new_code": new_code})
        else:
            return JsonResponse({"exists": False})


"""
--------------- CLASE: SOLICITUDES ESTUDIANTILES -----------------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tabla_solicitudes
from .serializers import TablaSolicitudesSerializer


class SolicitudesListAPIView(APIView):
    """
    @brief Clase que gestiona las solicitudes estudiantiles mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros en la tabla de solicitudes estudiantiles.
    """

    def get(self, request):
        """
        @brief Recupera todas las solicitudes estudiantiles de la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de solicitudes estudiantiles en formato JSON.
        """
        solicitudes = tabla_solicitudes.objects.all()
        serializer = TablaSolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea una nueva solicitud estudiantil en la base de datos.
        @param request Objeto HTTP Request que contiene los datos de la nueva solicitud en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna la nueva solicitud creada y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        serializer = TablaSolicitudesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
--------------- CLASE: PAGOS ESTUDIANTILES -----------------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tabla_pagos
from .serializers import TablaPagosSerializer


class PagosListAPIView(APIView):
    """
    @brief Clase que gestiona los pagos mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros en la tabla de pagos.
    """

    def get(self, request):
        """
        @brief Recupera todos los pagos registrados en la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de pagos en formato JSON.
        """
        pagos = (
            tabla_pagos.objects.all()
        )  # Recupera todos los registros de la tabla de pagos
        serializer = TablaPagosSerializer(
            pagos, many=True
        )  # Serializa los datos para su retorno en formato JSON
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea un nuevo registro de pago en la base de datos.
        @param request Objeto HTTP Request que contiene los datos del nuevo pago en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna el pago creado y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        serializer = TablaPagosSerializer(
            data=request.data
        )  # Deserializa los datos enviados en la solicitud
        if serializer.is_valid():  # Valida los datos recibidos
            serializer.save()  # Guarda el nuevo registro en la base de datos
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )  # Retorna el registro creado
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )  # Retorna errores si la validación falla


"""
--------------- CLASE: DATOS BASICOS (ADMIN, PROF Y ESTUDIANTES) -----------------
"""
from .models import Datos_basicos, datos_login, roles, profesores
from .serializers import DatosBasicosSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class DatosBasicosCreateView(APIView):
    """
    @brief Clase que gestiona la creación y actualización de los datos básicos de los usuarios.

    Esta clase proporciona métodos para:
    - Recuperar los datos básicos de los usuarios (GET).
    - Crear un nuevo usuario o actualizar los datos de un usuario existente (POST).
    """

    def get(self, request):
        """
        @brief Recupera todos los registros de datos básicos de los usuarios.

        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con los datos básicos de los usuarios en formato JSON.
        """
        datosbasicos = (
            Datos_basicos.objects.all()
        )  # Recupera todos los registros de la tabla Datos_basicos
        serializer = DatosBasicosSerializer(
            datosbasicos, many=True
        )  # Serializa los datos para su retorno en formato JSON
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Crea o actualiza los datos de un usuario según la cédula proporcionada.

        @param request Objeto HTTP Request que contiene los datos del usuario, incluyendo cédula y tipo de usuario.

        @return Response Objeto HTTP Response:
            - Si el usuario ya existe, se actualizan sus datos y se retorna el resultado con un código de estado 200 (OK).
            - Si el usuario no existe, se crea un nuevo registro y se retorna con un código de estado 201 (CREATED).
            - Si ocurre un error durante el proceso de validación o creación/actualización, se retorna un código de estado 400 (BAD REQUEST).
        """
        cedula_exp = request.data.get("cedula")  # Obtiene la cédula del usuario
        print(f"Cédula recibida: {cedula_exp}")

        # Intentar buscar el usuario por cédula
        usuario = Datos_basicos.objects.filter(cedula=cedula_exp).first()

        # Obtener tipo_usuario directamente desde el request
        tipo_usuario_exp = request.data.get(
            "tipo_usuario"
        )  # Obtiene el tipo de usuario desde el request
        print(f"Tipo de usuario recibido: {tipo_usuario_exp}")

        # Buscar la instancia del rol correspondiente al tipo_usuario
        if tipo_usuario_exp:
            try:
                tipo_usuario_obj = roles.objects.get(codigo_rol=tipo_usuario_exp)
            except roles.DoesNotExist:
                return Response(
                    {"error": "Tipo de usuario no encontrado."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            tipo_usuario_obj = None

        if usuario:  # Si el usuario existe, se actualizan los datos
            serializer = DatosBasicosSerializer(
                usuario, data=request.data, partial=True
            )
            if serializer.is_valid():
                # Guardar los datos actualizados en la tabla Datos_basicos
                updated_usuario = serializer.save()

                # Solo actualizamos datos_login si tipo_usuario no es None
                if tipo_usuario_obj is not None:
                    datos_login.objects.update_or_create(
                        cedula_usuario=usuario,  # Usamos la instancia de Datos_basicos
                        defaults={
                            "contraseña_usuario": updated_usuario.contraseña,
                            "tipo_usuario": tipo_usuario_obj,  # Usamos la instancia del rol
                        },
                    )

                # Si es un profesor (tipo_usuario == 3), se crea un registro en la tabla de profesores
                if tipo_usuario_exp == 3:
                    profesores.objects.create(
                        ci_profesor=usuario,  # Relacionamos con los datos básicos del profesor
                        cod_maestria_prof=None,  # Establecemos cod_maestria_prof como null
                        nom_profesor_materia=usuario.nombre,
                        ape_profesor_materia=usuario.apellido,
                    )
                    print(
                        f"Profesor creado con cédula {usuario.cedula}, sin maestría asignada."
                    )

                print(
                    f"Datos guardados en datos_login: {usuario.cedula}, {updated_usuario.contraseña}, {tipo_usuario_obj.nombre_rol if tipo_usuario_obj else 'sin rol'}"
                )

                return Response(
                    {
                        "message": "Usuario encontrado y actualizado con éxito.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:  # Si el usuario no existe, se crea uno nuevo
            serializer = DatosBasicosSerializer(data=request.data)
            if serializer.is_valid():
                # Guardar los datos en la tabla Datos_basicos
                usuario_guardado = serializer.save()

                # Solo guardamos en datos_login si tipo_usuario no es None
                if tipo_usuario_obj is not None:
                    datos_login.objects.create(
                        cedula_usuario=usuario_guardado,  # Usamos la instancia de Datos_basicos
                        contraseña_usuario=usuario_guardado.contraseña,
                        tipo_usuario=tipo_usuario_obj,  # Usamos la instancia del rol
                    )

                # Si es un profesor (tipo_usuario == 3), se crea un registro en la tabla de profesores
                if tipo_usuario_exp == 3:
                    profesores.objects.create(
                        ci_profesor=usuario_guardado,  # Relacionamos con los datos básicos del profesor
                        cod_maestria_prof=None,  # Establecemos cod_maestria_prof como null
                        nom_profesor_materia=usuario_guardado.nombre,
                        ape_profesor_materia=usuario_guardado.apelllido,
                    )
                    print(
                        f"Profesor creado con cédula {usuario_guardado.cedula}, sin maestría asignada."
                    )

                return Response(
                    {
                        "message": "Usuario registrado con éxito.",
                        "data": serializer.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
--------------- FUNCIÓN: LOGIN ADMINISTRADOR -----------------
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import datos_login
from rest_framework_simplejwt.tokens import RefreshToken

"""
request involucra todo lo que es proceso de https, se puede 
hacer request id, headers, o user etc 
"""


@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    """
    @brief Autenticación de usuario admin utilizando nombre de usuario y contraseña.

    Este endpoint permite que los administradores se autentiquen usando su nombre de usuario (cédula)
    y contraseña. Si las credenciales son correctas, se genera un par de tokens JWT (access y refresh).

    @param request Objeto HTTP Request que contiene las credenciales del usuario (nombre de usuario y contraseña) en el cuerpo de la solicitud.

    @return JsonResponse Objeto HTTP Response con el siguiente comportamiento:
    - Si las credenciales son correctas, se retornan los tokens `access` y `refresh` con un código de estado 200 (OK).
    - Si las credenciales son incorrectas (contraseña inválida), se retorna un error con un código de estado 401 (Unauthorized).
    - Si el usuario no existe o no es un administrador, se retorna un error con un código de estado 401 (Unauthorized).
    """
    import json

    data = json.loads(
        request.body
    )  # Obtiene los datos del cuerpo de la solicitud (JSON)
    cedula = data.get("username")  # Obtiene el nombre de usuario (cedula) del JSON
    password = data.get("password")  # Obtiene la contraseña del JSON

    try:
        # Intenta obtener el usuario con la cédula y tipo de usuario 1 (administrador)
        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=1)
        if user.contraseña_usuario == password:  # Verifica si la contraseña es correcta
            # Si la contraseña es correcta, genera los tokens JWT
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access": str(refresh.access_token),  # Token de acceso
                    "refresh": str(refresh),  # Token de refresco
                },
                status=200,
            )
        else:
            # Si la contraseña es incorrecta, retorna un error 401
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except datos_login.DoesNotExist:
        # Si el usuario no existe o no es un administrador, retorna un error 401
        return JsonResponse(
            {"error": "Usuario no encontrado o no es admin"}, status=401
        )


"""
--------------- CLASE: BUSCAR CEDULA PARA FORMALIZAR REGISTRO ESTUDIANTE -----------------
"""
from rest_framework.response import Response
from rest_framework import status
from .models import Datos_basicos
from .serializers import DatosBasicosSerializer
from rest_framework.views import APIView


class BuscarCedulaEstView(APIView):
    """
    @brief Vista para obtener y buscar datos básicos de estudiantes por cédula.

    Esta vista maneja dos métodos HTTP:
    - **GET**: Recupera todos los datos básicos de los estudiantes.
    - **POST**: Permite buscar un estudiante específico por su cédula y verificar su tipo de usuario.
    """

    def get(self, request):
        """
        @brief Recupera los datos básicos de todos los estudiantes.

        Este método responde con todos los registros de estudiantes almacenados en la base de datos.

        @param request Objeto HTTP Request.

        @return Response Datos de todos los estudiantes, serializados en formato JSON.
        """
        datosbasicos = Datos_basicos.objects.all()  # Recupera todos los estudiantes
        serializer = DatosBasicosSerializer(
            datosbasicos, many=True
        )  # Serializa los datos
        return Response(serializer.data)  # Retorna los datos serializados

    def post(self, request):
        """
        @brief Busca un estudiante por su cédula y verifica su tipo de usuario.

        Este método permite buscar a un estudiante en función de la cédula proporcionada. Si el estudiante
        existe y su tipo de usuario es "estudiante" (tipo_usuario == 2), se retornan los datos básicos del estudiante.
        Si no es un estudiante, se retorna un mensaje de error.

        @param request Objeto HTTP Request que debe contener la cédula del estudiante en el cuerpo de la solicitud.

        @return Response Datos del estudiante si se encuentra y es del tipo correcto, o un mensaje de error si no.
        """
        cedula_exp = request.data.get("cedula")  # Obtiene la cédula del request
        print(cedula_exp)  # Debug: Muestra la cédula recibida

        estudiante = Datos_basicos.objects.filter(
            cedula=cedula_exp
        ).first()  # Busca el estudiante por cédula

        if estudiante:  # Si el estudiante existe
            if (
                estudiante.tipo_usuario == 2
            ):  # Verifica si el tipo de usuario es estudiante
                serializer = DatosBasicosSerializer(
                    estudiante
                )  # Serializa los datos del estudiante
                return Response(
                    serializer.data, status=status.HTTP_200_OK
                )  # Retorna los datos del estudiante
            else:
                # Si el tipo de usuario no es estudiante, retorna un error
                return Response(
                    {"message": "El estudiante no tiene el tipo de usuario requerido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:  # Si no se encuentra el estudiante con la cédula proporcionada
            return Response(
                {"message": "Estudiante no encontrado. Por favor, regístrese."},
                status=status.HTTP_404_NOT_FOUND,
            )


"""
--------------- CLASE: ALMACENAR DATOS DEL ESTUDIANTE EN LA TABLA DE ESTUDIANTES -----------------
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .models import estudiante_datos, datos_maestria
from .serializers import EstudianteDatosSerializer
from rest_framework.views import APIView


class DatosMaestriaViewSet(viewsets.ModelViewSet):
    serializer_class = DatosMaestriaSerializer
    queryset = datos_maestria.objects.all()
    permission_classes = [IsPublic]

    # @action(['POST'], detail=True, url_path='set-on-vacation')
    # def set_on_vacation(self, request, pk):
    #     doctor = self.get_object()
    #     doctor.is_on_vacation = True
    #     doctor.save()
    #     return Response({"status": "El doctor está en vacaciones"})

    # @action(['POST'], detail=True, url_path='set-off-vacation')
    # def set_off_vacation(self, request, pk):
    #     doctor = self.get_object()
    #     doctor.is_on_vacation = False
    #     doctor.save()
    #     return Response({"status": "El doctor NO está en vacaciones"})

    # @action(['POST', 'GET'], detail=True, serializer_class=AppointmentSerializer)
    # def appointments(self, request, pk):
    #     doctor = self.get_object()

    #     if request.method == 'POST':
    #         data = request.data.copy()
    #         data['doctor'] = doctor.id
    #         serializer = AppointmentSerializer(data=data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     if request.method == 'GET':
    #         appointments = Appointment.objects.filter(doctor=doctor)
    #         serializer = AppointmentSerializer(appointments, many=True)
    #         return Response(serializer.data)

    # @action(['POST'], detail=True, url_path='create')
    # def create_new_doctor(self, request, pk):
    #     user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")

    #     return Response({"status": "El doctor está en vacaciones"})


class AlmacenarDatosEstView(APIView):
    """
    @brief Vista para registrar o actualizar los datos de un estudiante.

    Este endpoint permite registrar un estudiante si no existe en la base de datos,
    o actualizar sus datos si ya existe en la tabla `estudiante_datos`.
    También valida la existencia del estudiante en la tabla `Datos_basicos` y la existencia del código de maestría.
    """

    def post(self, request):
        """
        @brief Registrar o actualizar un estudiante en la base de datos.

        Este método recibe los datos de un estudiante y verifica si el estudiante existe en la base de datos.
        Si el estudiante existe, actualiza su información; si no, lo registra como un nuevo estudiante.

        @param request Objeto HTTP Request que debe contener los datos del estudiante en el cuerpo de la solicitud:
        - cedula_estudiante: Cédula del estudiante.
        - nombre_est: Nombre del estudiante.
        - apellido_est: Apellido del estudiante.
        - carrera: Carrera del estudiante.
        - año_ingreso: Año de ingreso del estudiante.
        - estado_estudiante: Estado del estudiante (activo o inactivo).
        - cod_maestria: Código de maestría asociado al estudiante.

        @return Response Mensaje indicando si el estudiante fue registrado o actualizado correctamente.
        """
        cedula = request.data.get("cedula_estudiante")  # Cédula del estudiante
        nombre = request.data.get("nombre_est")  # Nombre del estudiante
        apellido = request.data.get("apellido_est")  # Apellido del estudiante
        carrera = request.data.get("carrera")  # Carrera del estudiante
        año_ingreso = request.data.get("año_ingreso")  # Año de ingreso del estudiante
        estado_estudiante = request.data.get(
            "estado_estudiante"
        )  # Estado del estudiante ("Activo" o "Inactivo")
        cod_maestria = request.data.get(
            "cod_maestria"
        )  # Código de la maestría asociada al estudiante

        # Buscar el estudiante en la tabla Datos_basicos usando la cédula
        datos_basicos = Datos_basicos.objects.filter(cedula=cedula).first()

        if not datos_basicos:
            return Response(
                {"message": "Estudiante no encontrado en Datos_basicos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buscar la instancia de datos_maestria usando el código de maestría
        datos_maestria_instance = datos_maestria.objects.filter(
            cod_maestria=cod_maestria
        ).first()

        if cod_maestria and not datos_maestria_instance:
            return Response(
                {"message": "Código de maestría no encontrado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Crear o actualizar los datos del estudiante
        estudiante, created = estudiante_datos.objects.update_or_create(
            cedula_estudiante=datos_basicos,  # Relaciona el estudiante con la instancia de Datos_basicos
            defaults={  # Datos a actualizar o registrar
                "nombre_est": nombre,
                "apellido_est": apellido,
                "carrera": carrera,
                "año_ingreso": año_ingreso,
                "estado_estudiante": estado_estudiante,  # Estado del estudiante
                "cod_maestria": (
                    datos_maestria_instance if cod_maestria else None
                ),  # Relaciona con la instancia de datos_maestria, si se proporciona
            },
        )

        if created:
            message = (
                "Estudiante registrado con éxito."  # Mensaje si el estudiante es creado
            )
        else:
            message = "Estudiante actualizado con éxito."  # Mensaje si el estudiante es actualizado

        # Retorna un mensaje indicando el resultado de la operación
        return Response(
            {"message": message}, status=status.HTTP_200_OK
        )  # Usamos el código HTTP 200 OK


"""
------------------ FUNCION LOGIN DEL PROFESOR -------------------
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import datos_login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action

"""
request involucra todo lo que es proceso de https, se puede 
hacer request id, headers, o user etc 
"""

import json


@csrf_exempt
@require_http_methods(["POST"])
def login_profesor(request: Request):
    """
    @brief Endpoint para el login de un profesor.

    Este endpoint permite que un profesor inicie sesión proporcionando su cédula y contraseña.
    Si las credenciales son correctas, se generan tokens de acceso y refresco utilizando el paquete JWT.
    Si las credenciales son incorrectas o el usuario no es encontrado, se devuelve un mensaje de error.

    @param request Objeto de la solicitud HTTP que debe contener las credenciales del usuario:
    - username: Cédula del profesor.
    - password: Contraseña del profesor.

    @return JsonResponse Respuesta en formato JSON con los tokens de acceso y refresco si las credenciales son correctas.
    En caso de error, devuelve un mensaje con el error correspondiente.
    """

    try:
        print("klk")
        data = json.loads(request.body)  # Cargar los datos recibidos en formato JSON
        cedula = data.get("username")  # Obtener la cédula del profesor
        password = data.get("password")  # Obtener la contraseña del profesor

        # Buscar el usuario en la base de datos, asegurándose que sea un profesor (tipo_usuario=3)
        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=3)

        # Verificar si la contraseña proporcionada es correcta
        if user.contraseña_usuario == password:
            # Si la contraseña es correcta, generar tokens de acceso y refresco
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access": str(refresh.access_token),  # Token de acceso
                    "refresh": str(refresh),  # Token de refresco
                },
                status=200,
            )
        else:
            # Si la contraseña es incorrecta, devolver un error de autenticación
            return JsonResponse({"error": "Contraseña invalida"}, status=401)

    except Exception as e:

        # TODO: hacer funcion que se implemente en todos los casos de error comunes como por ejemplo mostrar el traceback en consola.
        # Log the error with traceback to stderr
        traceback.print_exc(file=sys.stderr)

        if isinstance(e, datos_login.DoesNotExist):
            # Si no se encuentra el usuario o no es un profesor, devolver un error
            return JsonResponse(
                {"error": "Usuario no encontrado o no es profesor"}, status=401
            )
        return JsonResponse(
            {"error": str(e), "traceback": traceback.format_exc()}, status=500
        )


"""
----- CLASE USERINFOVIEW: PARA RECUPERAR DATOS DE USUARIO AUTENTICADO ----------
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import DatosLoginSerializer


class UserInfoView(APIView):
    """
    @brief Endpoint para obtener información del usuario autenticado.

    Este endpoint permite a los usuarios autenticados obtener su propia información almacenada en la base de datos.
    La información se obtiene a través de la cédula del usuario, que es asociada a los datos del usuario en la base de datos.

    @note: El acceso a este endpoint requiere que el usuario esté autenticado.
    """

    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request):
        """
        @brief Obtener los datos del usuario autenticado.

        Este método obtiene los datos del usuario autenticado a través de su cédula almacenada en la base de datos.
        Si el usuario es encontrado, sus datos serán serializados y devueltos en la respuesta.
        Si no se encuentra al usuario, se devuelve un mensaje de error.

        @param request Objeto de solicitud HTTP que contiene la información del usuario autenticado.

        @return Response Respuesta con los datos del usuario si es encontrado, o un mensaje de error si no.
        """

        # Obtener la cédula del usuario autenticado
        user = (
            request.user
        )  # Esto asume que request.user está vinculado con Datos_basicos

        try:
            # Imprimir el tipo de objeto del usuario (para depuración)
            print(type(user))
            # Serializar los datos del usuario utilizando el serializador de login
            serializedUser = DatosLoginSerializer(user).data
            # Buscar el usuario en Datos_basicos por su cédula
            datos_usuario = Datos_basicos.objects.get(
                cedula=serializedUser["cedula_usuario"]
            )
            # Serializar los datos del usuario
            serializer = DatosBasicosSerializer(datos_usuario)
            return Response(serializer.data, status=200)

        except Datos_basicos.DoesNotExist:
            # Si el usuario no es encontrado, devolver un mensaje de error
            return Response({"error": "Usuario no encontrado"}, status=404)


"""
------- CLASE: PROFMATERIAS PARA RECUPERAR MATERIAS DE ESE PROFESOR ---- 
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import MateriasPensumSerializer
from .models import materias_pensum


class ProfMaterias(APIView):
    """
    @brief Endpoint para obtener las materias asociadas a un profesor autenticado.

    Este endpoint permite a los profesores autenticados obtener las materias que están asociadas a su cédula.
    La consulta se realiza sobre la tabla de materias asociadas al profesor, utilizando su cédula como identificador.

    @note: Este endpoint requiere que el usuario esté autenticado.
    """

    permission_classes = [IsAuthenticated]  # Requiere autenticación

    def get(self, request):
        """
        @brief Obtener las materias del profesor autenticado.

        Este método obtiene todas las materias asociadas al profesor autenticado. Se utiliza la cédula del
        usuario autenticado para realizar la búsqueda en la base de datos y obtener las materias asociadas
        a ese profesor. Si el profesor es encontrado y tiene materias asociadas, los datos serán devueltos en
        formato serializado.

        @param request Objeto de solicitud HTTP que contiene la información del usuario autenticado.

        @return Response Respuesta con las materias asociadas al profesor, o un mensaje de error si no se encuentran.
        """

        # Obtener la cédula del usuario autenticado
        user = (
            request.user
        )  # Esto asume que request.user está vinculado con Datos_basicos

        try:
            # Imprimir el tipo de objeto del usuario (para depuración)
            print(type(user))
            # Serializar los datos del usuario utilizando el serializador de login
            serializedUser = DatosLoginSerializer(user).data
            # Buscar las materias asociadas al profesor usando la cédula
            materias = materias_pensum.objects.filter(
                cedula_profesor=serializedUser["cedula_usuario"]
            )
            # Serializar los datos de las materias
            serializer = MateriasPensumSerializer(materias, many=True)
            print(type(serializer.data))
            return Response(serializer.data, status=200)

        except materias_pensum.DoesNotExist:
            # Si no se encuentran materias asociadas, devolver un mensaje de error
            return Response({"error": "Usuario no encontrado"}, status=404)
