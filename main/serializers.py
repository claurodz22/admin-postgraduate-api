##
# @file serializers.py
# @brief Serializadores que permiten convertir estructuras complejas de datos a formatos nativos de Python (como JSON o XML).
#
# Los serializadores son componentes que permiten la conversión de estructuras de datos complejas de un proyecto
# a estructuras nativas de un lenguaje de programación (en este caso, Python). Posteriormente, estas estructuras pueden
# ser convertidas a formatos como JSON o XML para su transmisión o almacenamiento.
#

from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


## @class PlanificacionProfesorSerializer
# @brief Serializa el modelo `PlanificacionProfesor`.
#
# Este serializador convierte el modelo `PlanificacionProfesor` en un formato adecuado para su transmisión en la API.
class PlanificacionProfesorSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.PlanificacionProfesor
        fields = "__all__"


## @class DatosBasicosSerializer
# @brief Serializa el modelo `Datos_basicos`.
#
# Convierte el modelo `Datos_basicos` a un formato que pueda ser transmitido y manipulado fácilmente en la API.
class DatosBasicosSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.Datos_basicos
        fields = "__all__"


## @class UserSerializer
# @brief Serializa el modelo de usuario.
#
# Este serializador se encarga de convertir el modelo `User` de Django en un formato adecuado para su posterior
# serialización a JSON o XML. Además, tiene un método `create` que facilita la creación de nuevos usuarios.
class UserSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = User
        fields = ["username", "password", "role"]
        extra_kwargs = {"password": {"write_only": True}}

    ## @brief Crea un nuevo usuario con los datos validados.
    #
    # Este método se utiliza para crear un nuevo usuario a partir de los datos validados que se proporcionan
    # al serializador. La contraseña es tratada de manera especial mediante el método `create_user`.
    #
    # @param validated_data Los datos validados para crear el usuario.
    # @return El usuario creado.
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


## @class DatosBasicosSerializer
# @brief Serializa el modelo `Datos_basicos`.
#
# Este serializador convierte el modelo `Datos_basicos` en un formato adecuado para su transmisión en formato JSON o XML.
class DatosBasicosSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.Datos_basicos
        fields = "__all__"


## @class DatosMaestriaSerializer
# @brief Serializa el modelo `datos_maestria`.
#
# Este serializador se encarga de convertir el modelo `datos_maestria` en un formato adecuado para su uso en la API.
class DatosMaestriaSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.datos_maestria
        fields = "__all__"


## @class EstudianteDatosSerializer
# @brief Serializa el modelo `estudiante_datos`.
#
# Este serializador convierte el modelo `estudiante_datos` en un formato adecuado para su serialización a JSON o XML.
class EstudianteDatosSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.estudiante_datos
        fields = "__all__"


## @class CohorteSerializer
# @brief Serializa el modelo `Cohorte`.
#
# Este serializador convierte el modelo `Cohorte` a un formato adecuado para su uso en la transmisión de datos.
class CohorteSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.Cohorte
        fields = "__all__"


## @class RolesSerializer
# @brief Serializa el modelo `roles`.
#
# Este serializador convierte el modelo `roles` en un formato adecuado para la API, permitiendo su fácil transmisión.
class RolesSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.roles
        fields = "__all__"


## @class MateriasPensumSerializer
# @brief Serializa el modelo `materias_pensum`.
#
# Este serializador convierte el modelo `materias_pensum` en un formato adecuado para la transmisión de datos
# relacionados con las materias del pensum.
class MateriasPensumSerializer(serializers.ModelSerializer):
    """serializer"""

    # cod_maestria = DatosMaestriaSerializer()

    class Meta:
        model = models.materias_pensum
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Añadir la representación del modelo relacionado en la nueva propiedad 'materia'
        representation["maestria"] = DatosMaestriaSerializer(instance.cod_maestria).data
        return representation


class AsignarProfesorMateriaSerializer(serializers.ModelSerializer):

    # cod_materia = MateriasPensumSerializer()
    class Meta:
        model = models.AsignarProfesorMateria
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # if self.context.get('resolve_relation', False):
        # Añadir la representación del modelo relacionado en la nueva propiedad 'materia'
        representation["materia"] = MateriasPensumSerializer(instance.cod_materia).data
        return representation


## @class DatosLoginSerializer
# @brief Serializa el modelo `datos_login`.
#
# Este serializador convierte el modelo `datos_login` en un formato adecuado para su transmisión, permitiendo el uso
# de la información de inicio de sesión en la API.
class DatosLoginSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.datos_login
        fields = "__all__"


## @class ListadoEstudiantesSerializer
# @brief Serializa el modelo `listado_estudiantes`.
#
# Este serializador convierte el modelo `listado_estudiantes` en un formato adecuado para su uso en la API.
class ListadoEstudiantesSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.listado_estudiantes
        fields = "__all__"


## @class ProfesoresSerializer
# @brief Serializa el modelo `profesores`.
#
# Este serializador convierte el modelo `profesores` en un formato adecuado para la transmisión de datos en la API.
class ProfesoresSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.profesores
        fields = "__all__"


## @class TablaPagosSerializer
# @brief Serializa el modelo `tabla_pagos`.
#
# Este serializador convierte el modelo `tabla_pagos` en un formato adecuado para su uso en la API de pagos.
class TablaPagosSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.tabla_pagos
        fields = "__all__"


## @class TablaSolicitudesSerializer
# @brief Serializa el modelo `tabla_solicitudes`.
#
# Este serializador convierte el modelo `tabla_solicitudes` en un formato adecuado para su uso en la API de solicitudes.
class TablaSolicitudesSerializer(serializers.ModelSerializer):
    """serializer"""

    class Meta:
        model = models.tabla_solicitudes
        fields = "__all__"
