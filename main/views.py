
from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UserSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tabla_pagos
from .serializers import TablaPagosSerializer

class PagosListAPIView(APIView):
    def get(self, request):
        pagos = tabla_pagos.objects.all()  # Recupera todos los productos
        serializer = TablaPagosSerializer(pagos, many=True)
        return Response(serializer.data)

class RegisterUserView(views.APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
