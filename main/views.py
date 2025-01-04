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
datos de los pagos a la BDD para que se los muestre
al administrador en una lista
'''
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tabla_pagos
from .serializers import TablaPagosSerializer

class PagosListAPIView(APIView):
    def get(self, request):
        pagos = tabla_pagos.objects.all()  # Recupera todos los productos
        serializer = TablaPagosSerializer(pagos, many=True)
        return Response(serializer.data)

'''
Vista correspondiente para poder enviar datos
a la BDD para poder registrar usuarios
en la aplicacion web
'''
## agregado
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DatosBasicosSerializer
from .models import Datos_basicos

class DatosBasicosCreateView(APIView):
    def post(self, request):
        serializer = DatosBasicosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }, status=200)
        else:
            return JsonResponse({"error": "Contraseña invalida"}, status=401)
    except datos_login.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado o no es admin"}, status=401)