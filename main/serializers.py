'''
Serializador: es un componente que permite convertir estructuras 
complejas de un proyecto en estructuras nativas de un lenguaje 
de programación, como Python, para que puedan 
ser convertidas en JSON o XML.
'''

from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

class UserSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = User
        fields = ['username', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class DatosBasicosSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.Datos_basicos
        fields = '__all__'

class DatosMaestriaSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.datos_maestria
        fields = '__all__'

class EstudianteDatosSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.estudiante_datos
        fields = '__all__'

class CohorteSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.Cohorte
        fields = '__all__'

class RolesSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.roles
        fields = '__all__'

class DatosLoginSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.datos_login
        fields = '__all__'

class MateriasPensumSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.materias_pensum
        fields = '__all__'

class ListadoEstudiantesSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.listado_estudiantes
        fields = '__all__'

class ProfesoresSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.profesores
        fields = '__all__'

class TablaPagosSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.tabla_pagos
        fields = '__all__'

class TablaSolicitudesSerializer(serializers.ModelSerializer):
    """serializer"""
    class Meta:
        model = models.tabla_solicitudes
        fields = '__all__'