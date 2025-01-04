'''
Vistas: son funciones o clases de Python que reciben 
una solicitud web y devuelven una respuesta.

La respuesta puede ser una respuesta HTTP, 
una respuesta de plantilla HTML o una redirección 
HTTP
'''

from rest_framework import serializers, views, status
from rest_framework.response import Response
from django.contrib.auth.models import User


'''
RegisterUserView se utilizo e la primera presentación de la App
ya no se utiliza debido a que ya se incorporá la base de datos
externa (PostgreSQL) y se utilizo otro mecanismo
de verificación de datos.

class RegisterUserView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''