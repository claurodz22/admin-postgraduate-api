'''
Vistas: son funciones o clases de Python que reciben 
una solicitud web y devuelven una respuesta.

La respuesta puede ser una respuesta HTTP, 
una respuesta de plantilla HTML o una redirección 
HTTP
'''
'''
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UserSerializer

ya se hizo una explicacion previa en otro .py
esto se uso en una fase de prueba
class RegisterUserView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
Vista correspondiente a solicitar los
datos de las solicitudes a la BDD para que se los muestre
al administrador en una lista
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import tabla_solicitudes
from .serializers import TablaSolicitudesSerializer

class SolicitudesListAPIView(APIView):
    def get(self, request):         # <-- get request: recupera datos a la bdd 
        solicitudes = tabla_solicitudes.objects.all()
        serializer = TablaSolicitudesSerializer(solicitudes, many=True)
        return Response(serializer.data)

    def post(self, request):        # <-- post request: manda datos a la bdd 
        serializer = TablaSolicitudesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Vista correspondiente a solicitar los
datos de los pagos a la BDD para que se los muestre
al administrador en una lista
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tabla_pagos
from .serializers import TablaPagosSerializer

class PagosListAPIView(APIView):
    def get(self, request):     # <-- get request: recupera datos a la bdd 
        pagos = tabla_pagos.objects.all()  
        serializer = TablaPagosSerializer(pagos, many=True)
        return Response(serializer.data)

    def post(self, request): # <-- post request: manda datos a la bdd 
        serializer = TablaPagosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Vista correspondiente para poder enviar datos
a la BDD para poder registrar usuarios
en la aplicacion web
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DatosBasicosSerializer
from .models import Datos_basicos

class DatosBasicosCreateView(APIView):
    
    def get(self, request):
        datosbasicos = Datos_basicos.objects.all()
        serializer = DatosBasicosSerializer(datosbasicos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        cedula_exp = request.data.get('cedula')
        print(f"Cédula recibida: {cedula_exp}")
        
        # Intentar buscar el usuario por cédula
        usuario = Datos_basicos.objects.filter(cedula=cedula_exp).first()

        if usuario:  # si existe, lo retorna para modificar/actualizar datos
            serializer = DatosBasicosSerializer(usuario, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print(usuario)
                return Response(
                    {"message": "Usuario encontrado con éxito.", "data": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:  # si no existe, pues, toma datos del front para luego crearlo
            serializer = DatosBasicosSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {"message": "Usuario registrado con éxito.", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
Vista responsable del logeo de usuarios
a la app, solo responsable de log a los
administraodores,, por ello, uno de los 
parametros es 'tipo_usuario=1'
'''
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import datos_login
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    import json
    data = json.loads(request.body)
    cedula = data.get("username")
    password = data.get("password")

    try:
        user = datos_login.objects.get(cedula_usuario=cedula, tipo_usuario=1)
        if user.contraseña_usuario == password:
            # Si la contraseña es correcta, generar tokens
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)
        else:
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except datos_login.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado o no es admin"}, status=401)

'''
Vista responsable de visualizar si el estudiante esta registrado
Funccionalidad en la pestaña de registrar estudiantes
'''
from rest_framework.response import Response
from rest_framework import status
from .models import Datos_basicos
from .serializers import DatosBasicosSerializer
from rest_framework.views import APIView

class BuscarCedulaEstView(APIView):
    def get(self, request):  # <-- get: obtener los datos basicos
        datosbasicos = Datos_basicos.objects.all()
        serializer = DatosBasicosSerializer(datosbasicos, many=True)
        return Response(serializer.data)

    def post(self, request):  # <-- post: buscar estudiante por cédula
        cedula_exp = request.data.get('cedula')
        print(cedula_exp)    # <-- ver qué estaba recibiendo        
        estudiante = Datos_basicos.objects.filter(cedula=cedula_exp).first()
        
        if estudiante:  # si estudiante es un valor no nulo
            if estudiante.tipo_usuario == 2: #tipo_usuario == 2 es que representa que es estudiante
                serializer = DatosBasicosSerializer(estudiante)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response( # la cedula ingresada es de prof o de admi
                    {"message": "El estudiante no tiene el tipo de usuario requerido."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:  # caso contrario, si no se encuentra la cedula
            return Response(
                {"message": "Estudiante no encontrado. Por favor, regístrese."},
                status=status.HTTP_404_NOT_FOUND
            )


'''
Vista responsable de formalizar la inscripción de 
los estudiantes en el sistema ya una vez encontrados por
cedula
'''
from rest_framework.response import Response
from rest_framework import status
from .models import estudiante_datos, datos_maestria
from .serializers import EstudianteDatosSerializer
from rest_framework.views import APIView

class AlmacenarDatosEstView(APIView):
    def post(self, request):
        """
        Registrar o actualizar un estudiante.
        """
        cedula = request.data.get('cedula_estudiante')
        nombre = request.data.get('nombre_est')
        apellido = request.data.get('apellido_est')
        carrera = request.data.get('carrera')
        año_ingreso = request.data.get('año_ingreso')
        estado_estudiante = request.data.get('estado_estudiante')  # Ahora es un texto ("Activo" o "Inactivo")
        cod_maestria = request.data.get('cod_maestria')

        # Buscar la instancia de Datos_basicos por la cédula
        datos_basicos = Datos_basicos.objects.filter(cedula=cedula).first()

        if not datos_basicos:
            return Response({"message": "Estudiante no encontrado en Datos_basicos."}, status=http_status.HTTP_400_BAD_REQUEST)

        # Buscar la instancia de datos_maestria por el código de maestría
        datos_maestria_instance = datos_maestria.objects.filter(cod_maestria=cod_maestria).first()

        if cod_maestria and not datos_maestria_instance:
            return Response({"message": "Código de maestría no encontrado."}, status=http_status.HTTP_400_BAD_REQUEST)

        # Crear o actualizar el estudiante
        estudiante, created = estudiante_datos.objects.update_or_create(
            cedula_estudiante=datos_basicos,  # Instancia de Datos_basicos
            defaults={
                'nombre_est': nombre,
                'apellido_est': apellido,
                'carrera': carrera,
                'año_ingreso': año_ingreso,
                'estado_estudiante': estado_estudiante,  # Ahora es texto ("Activo" o "Inactivo")
                'cod_maestria': datos_maestria_instance if cod_maestria else None  # Instancia de datos_maestria o None
            }
        )

        if created:
            message = "Estudiante registrado con éxito."
        else:
            message = "Estudiante actualizado con éxito."

        return Response({"message": message}, status=status.HTTP_200_OK)  # Usamos 'status.HTTP_200_OK'

