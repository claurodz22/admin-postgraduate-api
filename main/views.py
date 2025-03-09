"""
@file views.py
@brief Vistas de la API para manejar la lógica del negocio y los datos.

Este archivo contiene las vistas que definen la lógica de negocio para interactuar con los modelos
de la base de datos y devolver respuestas a través de la API.
"""

from rest_framework import status, viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
import json
import sys
import traceback
import datetime

from main.permissions import IsPublic
from . import models
from .models import (
    AsignarProfesorMateria, materias_pensum, profesores, Cohorte, 
    PlanificacionProfesor, listado_estudiantes, tabla_solicitudes, 
    tabla_pagos, Datos_basicos, datos_login, roles, estudiante_datos,
    datos_maestria
)
from .serializers import (
    AsignarProfesorMateriaSerializer, MateriasPensumSerializer, 
    ProfesoresSerializer, CohorteSerializer, PlanificacionProfesorSerializer,
    ListadoEstudiantesSerializer, TablaSolicitudesSerializer, 
    TablaPagosSerializer, DatosBasicosSerializer, DatosLoginSerializer,
    EstudianteDatosSerializer, DatosMaestriaSerializer
)

# Utilidad para convertir texto a mayúsculas
def convert_to_uppercase(data):
    """
    @brief Convierte todos los campos de texto en un diccionario a mayúsculas.
    @param data Diccionario con los datos a convertir.
    @return Diccionario con los campos de texto convertidos a mayúsculas.
    """
    uppercase_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            uppercase_data[key] = value.upper()
        else:
            uppercase_data[key] = value
    return uppercase_data

# Clase base para vistas CRUD simples
class BaseCRUDView(APIView):
    """
    @brief Clase base para operaciones CRUD simples.
    """
    model = None
    serializer_class = None
    permission_classes = []
    
    def get(self, request, format=None):
        """
        @brief Obtiene todos los registros del modelo.
        """
        objects = self.model.objects.all()
        serializer = self.serializer_class(objects, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        """
        @brief Crea un nuevo registro.
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Vistas específicas que extienden la clase base
class AsignarProfesorMateriaView(BaseCRUDView):
    """
    @brief Vista para asignar un profesor a una materia y listar asignaciones.
    """
    model = AsignarProfesorMateria
    serializer_class = AsignarProfesorMateriaSerializer
    
    def post(self, request):
        """
        @brief Crea nuevas asignaciones de profesor a materia.
        """
        planning_data = request.data.get("planning", [])
        if not planning_data:
            return Response(
                {"detail": "No se proporcionaron datos de planificación."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        created_assignments = []
        errors = []

        for item in planning_data:
            uppercase_item = convert_to_uppercase(item)
            serializer = self.serializer_class(data=uppercase_item)
            if serializer.is_valid():
                serializer.save()
                created_assignments.append(serializer.data)
            else:
                errors.append(serializer.errors)

        if errors:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"created": created_assignments}, status=status.HTTP_201_CREATED
        )

class MateriasPensumAPIView(BaseCRUDView):
    """
    @brief API View para listar y registrar materias del pensum de cada maestría.
    """
    model = materias_pensum
    serializer_class = MateriasPensumSerializer
    permission_classes = [IsAuthenticated]

class ProfesoresAPIView(BaseCRUDView):
    """
    @brief Clase que gestiona los profesores mediante solicitudes HTTP.
    """
    model = profesores
    serializer_class = ProfesoresSerializer

class CohorteListAPIView(BaseCRUDView):
    """
    @brief Clase que gestiona los cohortes mediante solicitudes HTTP.
    """
    model = Cohorte
    serializer_class = CohorteSerializer
    permission_classes = [IsAuthenticated]

class PlanificacionProfesorAPIView(APIView):
    """
    @brief Clase que gestiona la planificación de profesores mediante solicitudes HTTP.
    Esta clase permite recuperar (GET) o crear (POST) registros en la tabla de planificación de profesores.
    """
    
    def convert_to_uppercase(self, data):
        """
        @brief Convierte todos los valores string del diccionario a mayúsculas.
        @param data Diccionario con los datos a convertir.
        @return Diccionario con los valores string convertidos a mayúsculas.
        """
        if isinstance(data, dict):
            result = {}
            for key, value in data.items():
                if isinstance(value, str):
                    result[key] = value.upper()
                elif isinstance(value, dict) or isinstance(value, list):
                    result[key] = self.convert_to_uppercase(value)
                else:
                    result[key] = value
            return result
        elif isinstance(data, list):
            return [self.convert_to_uppercase(item) for item in data]
        return data
    
    def get(self, request):
        """
        @brief Recupera todas las planificaciones de profesores registradas en la base de datos.
        @param request Objeto HTTP Request.
        @return Response Objeto HTTP Response con la lista de planificaciones en formato JSON.
        """
        try:
            # Opcionalmente, podemos filtrar por cedula_profesor si se proporciona en los parámetros de consulta
            cedula_profesor = request.query_params.get('cedula_profesor')
            
            if cedula_profesor:
                planificaciones = PlanificacionProfesor.objects.filter(cedula_profesor=cedula_profesor)
            else:
                planificaciones = PlanificacionProfesor.objects.all()
                
            serializer = PlanificacionProfesorSerializer(planificaciones, many=True)
            return Response(serializer.data)
        except Exception as e:
            # Registrar el error para depuración
            print(f"Error en PlanificacionProfesorAPIView.get: {str(e)}")
            traceback.print_exc()
            return Response(
                {"error": "Error al obtener las planificaciones", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """
        @brief Crea un nuevo registro de planificación en la base de datos.
        @param request Objeto HTTP Request que contiene los datos de la planificación en formato JSON.
        @return Response Objeto HTTP Response:
            - Si los datos son válidos, retorna la planificación creada y un código de estado 201 (CREATED).
            - Si los datos son inválidos, retorna los errores de validación y un código de estado 400 (BAD REQUEST).
        """
        try:
            # Convertir los datos a mayúsculas antes de validarlos
            uppercase_data = self.convert_to_uppercase(request.data)
            
            serializer = PlanificacionProfesorSerializer(data=uppercase_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Registrar el error para depuración
            print(f"Error en PlanificacionProfesorAPIView.post: {str(e)}")
            traceback.print_exc()
            return Response(
                {"error": "Error al crear la planificación", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ListadoEstudiantes(BaseCRUDView):
    """
    @brief Clase para recuperar listado de estudiantes.
    """
    model = listado_estudiantes
    serializer_class = ListadoEstudiantesSerializer
    
    def get(self, request):
        """
        @brief Método GET: Para obtener todos los estudiantes con filtros opcionales.
        """
        q_code = request.query_params.get("q_code")
        m_code = request.query_params.get("m_code")
        estudiantes = self.model.objects.all()
        
        if q_code:
            estudiantes = estudiantes.filter(codigo_cohorte=q_code)
        if m_code:
            estudiantes = estudiantes.filter(cod_materia=m_code)
            
        serializer = self.serializer_class(estudiantes, many=True)
        return Response(serializer.data)

class SolicitudesListAPIView(BaseCRUDView):
    """
    @brief Clase que gestiona las solicitudes estudiantiles.
    """
    model = tabla_solicitudes
    serializer_class = TablaSolicitudesSerializer

class PagosListAPIView(BaseCRUDView):
    """
    @brief Clase que gestiona los pagos mediante solicitudes HTTP.
    """
    model = tabla_pagos
    serializer_class = TablaPagosSerializer
    
    def get(self, request):
        """
        @brief Recupera todos los pagos con relaciones.
        """
        pagos = self.model.objects.select_related().all()
        serializer = self.serializer_class(pagos, many=True)
        return Response(serializer.data)

class DatosBasicosCreateView(BaseCRUDView):
    """
    @brief Clase que gestiona la creación y actualización de los datos básicos de los usuarios.
    """
    model = Datos_basicos
    serializer_class = DatosBasicosSerializer
    
    def post(self, request):
        """
        @brief Crea o actualiza los datos de un usuario según la cédula proporcionada.
        """
        # Convertir los datos a mayúsculas (excepto la contraseña)
        data = request.data.copy()
        for key, value in data.items():
            if key != 'contraseña' and isinstance(value, str):
                data[key] = value.upper()
        
        cedula_exp = data.get("cedula")
        tipo_usuario_exp = data.get("tipo_usuario")
        
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
            
        # Intentar buscar el usuario por cédula
        usuario = self.model.objects.filter(cedula=cedula_exp).first()
        
        if usuario:  # Si el usuario existe, se actualizan los datos
            serializer = self.serializer_class(usuario, data=data, partial=True)
            if serializer.is_valid():
                updated_usuario = serializer.save()
                
                # Actualizar datos_login si tipo_usuario no es None
                if tipo_usuario_obj is not None:
                    datos_login.objects.update_or_create(
                        cedula_usuario=usuario,
                        defaults={
                            "contraseña_usuario": updated_usuario.contraseña,
                            "tipo_usuario": tipo_usuario_obj,
                        },
                    )
                
                # Si es un profesor, crear registro en tabla profesores
                if tipo_usuario_exp == 3:
                    profesores.objects.create(
                        ci_profesor=usuario,
                        cod_maestria_prof=None,
                        nom_profesor_materia=usuario.nombre,
                        ape_profesor_materia=usuario.apellido,
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
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                usuario_guardado = serializer.save()
                
                # Guardar en datos_login si tipo_usuario no es None
                if tipo_usuario_obj is not None:
                    datos_login.objects.create(
                        cedula_usuario=usuario_guardado,
                        contraseña_usuario=usuario_guardado.contraseña,
                        tipo_usuario=tipo_usuario_obj,
                    )
                
                # Si es un profesor, crear registro en tabla profesores
                if tipo_usuario_exp == 3:
                    profesores.objects.create(
                        ci_profesor=usuario_guardado,
                        cod_maestria_prof=None,
                        nom_profesor_materia=usuario_guardado.nombre,
                        ape_profesor_materia=usuario_guardado.apellido,
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

class BuscarCedulaEstView(APIView):
    """
    @brief Vista para obtener y buscar datos básicos de estudiantes por cédula.
    """
    def get(self, request):
        """
        @brief Recupera los datos básicos de todos los estudiantes.
        """
        datosbasicos = Datos_basicos.objects.all()
        serializer = DatosBasicosSerializer(datosbasicos, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        @brief Busca un estudiante por su cédula y verifica su tipo de usuario.
        """
        cedula_exp = request.data.get("cedula")
        estudiante = Datos_basicos.objects.filter(cedula=cedula_exp).first()

        if estudiante:
            if estudiante.tipo_usuario == 2:
                serializer = DatosBasicosSerializer(estudiante)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"message": "El estudiante no tiene el tipo de usuario requerido."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"message": "Estudiante no encontrado. Por favor, regístrese."},
                status=status.HTTP_404_NOT_FOUND,
            )

class AlmacenarDatosEstView(APIView):
    """
    @brief Vista para registrar o actualizar los datos de un estudiante.
    """
    def post(self, request):
        """
        @brief Registrar o actualizar un estudiante en la base de datos.
        """
        # Obtener los datos del request y convertirlos a mayúsculas
        cedula = request.data.get("cedula_estudiante", "").upper()
        nombre = request.data.get("nombre_est", "").upper()
        apellido = request.data.get("apellido_est", "").upper()
        carrera = request.data.get("carrera", "").upper()
        año_ingreso = request.data.get("año_ingreso")
        estado_estudiante = request.data.get("estado_estudiante", "").upper()
        cod_maestria = request.data.get("cod_maestria", "").upper()

        # Buscar el estudiante en la tabla Datos_basicos
        datos_basicos = Datos_basicos.objects.filter(cedula=cedula).first()
        if not datos_basicos:
            return Response(
                {"message": "Estudiante no encontrado en Datos_basicos."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Buscar la instancia de datos_maestria
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
            cedula_estudiante=datos_basicos,
            defaults={
                "nombre_est": nombre,
                "apellido_est": apellido,
                "carrera": carrera,
                "año_ingreso": año_ingreso,
                "estado_estudiante": estado_estudiante,
                "cod_maestria": datos_maestria_instance if cod_maestria else None,
            },
        )

        message = "Estudiante registrado con éxito." if created else "Estudiante actualizado con éxito."
        return Response({"message": message}, status=status.HTTP_200_OK)

class UserInfoView(APIView):
    """
    @brief Endpoint para obtener información del usuario autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        @brief Obtener los datos del usuario autenticado.
        Si el tipo de usuario es 2, también obtiene los datos de estudiante.
        """
        user = request.user
        try:
            serialized_user = DatosLoginSerializer(user).data
            cedula = serialized_user["cedula_usuario"]
            datos_usuario = Datos_basicos.objects.get(cedula=cedula)
            
            # obtener datos basicos 
            user_data = DatosBasicosSerializer(datos_usuario).data
            
            # verifica si es tipo_usuario = 2 (q es estudiante)
            if datos_usuario.tipo_usuario == 2:
                try:
                    # obtiene datos del estudiante
                    estudiante = estudiante_datos.objects.get(cedula_estudiante=cedula)
                    estudiante_serializer = EstudianteDatosSerializer(estudiante)
                    
                    # combina datos de ambas tablas
                    response_data = {
                        **user_data,
                        "datos_estudiante": estudiante_serializer.data
                    }
                    return Response(response_data, status=200)
                except estudiante_datos.DoesNotExist:
                    # si no existe
                    return Response({
                        **user_data,
                        "datos_estudiante": None,
                        "error": "Datos de estudiante no encontrados"
                    }, status=200)
            
            # si no existe
            return Response(user_data, status=200)
            
        except Datos_basicos.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

class ProfMaterias(APIView):
    """
    @brief Endpoint para obtener las materias asociadas a un profesor autenticado.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        @brief Obtener las materias del profesor autenticado.
        """
        user = request.user
        try:
            serializedUser = DatosLoginSerializer(user).data
            profesor = profesores.objects.select_related(
                "cod_maestria_prof", "ci_profesor"
            ).get(ci_profesor=serializedUser["cedula_usuario"])
            
            materias = materias_pensum.objects.filter(
                cod_maestria=profesor.cod_maestria_prof
            )
            serializer = MateriasPensumSerializer(materias, many=True)
            return Response(serializer.data, status=200)
        except materias_pensum.DoesNotExist:
            return Response({"error": "Usuario no encontrado"}, status=404)

class DatosMaestriaViewSet(viewsets.ModelViewSet):
    """
    @brief ViewSet para gestionar datos de maestrías.
    """
    serializer_class = DatosMaestriaSerializer
    queryset = datos_maestria.objects.all()
    permission_classes = [IsPublic]

class UsuariosPorTipoAPIView(APIView):
    """
    @brief API View que devuelve usuarios filtrados por tipo.
    """
    def get(self, request, format=None):
        """
        @brief Maneja las solicitudes GET para obtener usuarios por tipo.
        """
        tipo_usuario = request.query_params.get('tipo_usuario')
        
        if tipo_usuario is not None:
            try:
                tipo_usuario = int(tipo_usuario)
                usuarios = Datos_basicos.objects.filter(tipo_usuario=tipo_usuario)
            except ValueError:
                return Response(
                    {"error": "El tipo de usuario debe ser un número entero"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            usuarios = Datos_basicos.objects.all()
        
        serializer = DatosBasicosSerializer(usuarios, many=True)
        return Response(serializer.data)

# Funciones para autenticación
@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    """
    @brief Autenticación de usuario admin utilizando nombre de usuario y contraseña.
    """
    data = json.loads(request.body)
    cedula = data.get("username")
    password = data.get("password")

    try:
        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=1)
        if user.contraseña_usuario == password:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=200,
            )
        else:
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except datos_login.DoesNotExist:
        return JsonResponse(
            {"error": "Usuario no encontrado o no es admin"}, status=401
        )

@csrf_exempt
@require_http_methods(["POST"])
def login_profesor(request):
    """
    @brief Endpoint para el login de un profesor.
    """
    try:
        data = json.loads(request.body)
        cedula = data.get("username")
        password = data.get("password")

        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=3)
        if user.contraseña_usuario == password:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=200,
            )
        else:
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        if isinstance(e, datos_login.DoesNotExist):
            return JsonResponse(
                {"error": "Usuario no encontrado o no es profesor"}, status=401
            )
        return JsonResponse(
            {"error": str(e), "traceback": traceback.format_exc()}, status=500
        )

@csrf_exempt
@require_http_methods(["POST"])
def login_estudiante(request):
    """
    @brief Endpoint para el login de un estudiante.
    """
    try:
        data = json.loads(request.body)
        cedula = data.get("username")
        password = data.get("password")

        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=2)
        if user.contraseña_usuario == password:
            refresh = RefreshToken.for_user(user)
            return JsonResponse(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=200,
            )
        else:
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except Exception as e:
        traceback.print_exc(file=sys.stderr)
        if isinstance(e, datos_login.DoesNotExist):
            return JsonResponse(
                {"error": "Usuario no encontrado o no es estudiante"}, status=401
            )
        return JsonResponse(
            {"error": str(e), "traceback": traceback.format_exc()}, status=500
        )

# Funciones para gestión de cohortes
@api_view(["POST"])
def generar_codigo_cohorte(request):
    """
    @brief Genera un código único para una nueva cohorte y la registra en la base de datos.
    """
    if request.method == "POST":
        codigo_cohorte = request.data.get("codigo_cohorte")
        fecha_inicio = request.data.get("fecha_inicio")
        fecha_fin = request.data.get("fecha_fin")
        sede_cohorte = request.data.get("sede_cohorte")
        tipo_maestria = request.data.get("tipo_maestria")

        # Función para generar un nuevo código
        def generate_new_code(code):
            prefix = code[:-6]
            year = code[-4:]
            current_letter = code[-6]
            next_letter = chr(ord(current_letter) + 1)
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
    """
    if request.method == "POST":
        codigo_cohorte = request.data.get("codigo_cohorte")

        if not codigo_cohorte:
            return JsonResponse(
                {"error": "Código de cohorte no proporcionado"}, status=400
            )

        # Función para generar un nuevo código
        def generate_new_code(code):
            prefix = code[:-6]
            year = code[-4:]
            current_letter = code[-6]
            next_letter = chr(ord(current_letter) + 1)
            return f"{prefix}{next_letter}-{year}"

        # Verifica si el código de cohorte ya existe
        if Cohorte.objects.filter(codigo_cohorte=codigo_cohorte).exists():
            new_code = generate_new_code(codigo_cohorte)
            return JsonResponse({"exists": True, "new_code": new_code})
        else:
            return JsonResponse({"exists": False})

# Funciones para eliminar usuarios y actualizar estados
@csrf_exempt
@require_http_methods(["POST"])
def eliminar_usuarios(request):
    """
    @brief Elimina usuarios seleccionados y sus datos de login asociados, excepto el usuario con cédula "V-27943668".
    """
    try:
        data = json.loads(request.body)
        user_ids = data.get('user_ids', [])
        
        if not user_ids:
            return JsonResponse({'error': 'No se proporcionaron IDs de usuario'}, status=400)
        
        # Excluir el usuario con cédula "V-27943668"
        protected_user_id = "V-27943668"
        user_ids = [uid for uid in user_ids if uid != protected_user_id]
        
        login_count = datos_login.objects.filter(cedula_usuario__cedula__in=user_ids).count()
        deleted_count = Datos_basicos.objects.filter(cedula__in=user_ids).exclude(cedula=protected_user_id).delete()[0]
        
        message = f'Se eliminó la lista de usuarios seleccionados'
        if protected_user_id in data.get('user_ids', []):
            message += f', excepto el usuario con cédula {protected_user_id}'
        
        return JsonResponse({
            'message': message,
            'deleted_users_count': deleted_count,
            'deleted_login_count': login_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def listar_usuarios(request):
    """
    @brief Lista usuarios filtrados por tipo de usuario.
    """
    tipo_usuario = request.GET.get('tipo_usuario')
    
    if not tipo_usuario:
        return JsonResponse({'error': 'Se requiere el parámetro tipo_usuario'}, status=400)
    
    usuarios = Datos_basicos.objects.filter(tipo_usuario=tipo_usuario).values('cedula', 'nombre', 'apellido', 'correo')
    return JsonResponse(list(usuarios), safe=False)

@csrf_exempt
@require_http_methods(["POST"])
def actualizar_estado_pagos(request):
    """
    @brief Actualiza el estado de los pagos proporcionados.
    """
    try:
        data = json.loads(request.body)
        pagos = data.get('pagos', [])

        if not pagos:
            return JsonResponse({'error': 'No se proporcionaron pagos para actualizar'}, status=400)

        updated_count = 0
        for pago in pagos:
            numero_referencia = pago.get('numero_referencia')
            nuevo_estado = pago.get('nuevoEstado')

            if numero_referencia and nuevo_estado:
                try:
                    numero_referencia = int(numero_referencia)
                    updated = tabla_pagos.objects.filter(numero_referencia=numero_referencia).update(estado_pago=nuevo_estado)
                    updated_count += updated
                except ValueError:
                    return JsonResponse({'error': f'Número de referencia inválido: {numero_referencia}'}, status=400)

        return JsonResponse({
            'message': f'Se actualizaron {updated_count} pagos exitosamente',
            'updated_count': updated_count
        })
    except Exception as e:
        print("Error en actualizar_estado_pagos:", traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def actualizar_estado_solicitudes(request):
    """
    @brief Actualiza el estado de las solicitudes proporcionadas.
    """
    try:
        data = json.loads(request.body)
        solicitudes = data.get('solicitudes', [])
        
        if not solicitudes:
            return JsonResponse({'error': 'No se proporcionaron solicitudes para actualizar'}, status=400)
        
        updated_count = 0
        for solicitud in solicitudes:
            cod_solicitudes = solicitud.get('cod_solicitudes')
            nuevo_estado = solicitud.get('nuevoEstado')
            if cod_solicitudes and nuevo_estado:
                try:
                    solicitud_obj = tabla_solicitudes.objects.get(cod_solicitudes=cod_solicitudes)
                    solicitud_obj.status_solicitud = nuevo_estado
                    solicitud_obj.fecha_solicitud = timezone.now()
                    solicitud_obj.save()
                    updated_count += 1
                except tabla_solicitudes.DoesNotExist:
                    continue
        
        return JsonResponse({
            'message': f'Se actualizaron {updated_count} solicitudes exitosamente',
            'updated_count': updated_count
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

