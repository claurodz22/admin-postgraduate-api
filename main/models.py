from django.db import models

##
# @file models.py
# @brief Definición de los modelos para la base de datos de estudiantes, profesores, pagos, y otros elementos relacionados.
#
# Este archivo contiene la definición de los modelos de datos que representan las entidades
# clave en el sistema, como los estudiantes, profesores, materias, pagos y solicitudes. 
# Los modelos son utilizados para la interacción con la base de datos en Django, utilizando 
# PostgreSQL como base de datos para la persistencia de datos.
#
# @see Django Models
# @see Django ORM
# @see PostgreSQL Database

## @class Datos_basicos
# @brief Modelo que almacena los datos básicos de los usuarios, incluyendo estudiantes y profesores.
class Datos_basicos(models.Model):
    """
    @brief Modelo que almacena los datos básicos de los usuarios, incluyendo estudiantes y profesores.
    
    Este modelo tiene los campos necesarios para registrar la cédula, nombre, apellido, tipo de usuario,
    contraseña y correo electrónico de un usuario.
    """
    cedula = models.TextField(primary_key=True)  # CEDULA = PRIMARY KEY
    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)
    tipo_usuario = models.IntegerField(null=False)
    contraseña = models.TextField(null=False)
    correo = models.EmailField(null=False, blank=True)

    def __str__(self):
        """
        @brief Representación en string del modelo, combinando el nombre, apellido, cédula y tipo de usuario.
        """
        return f"{self.nombre} {self.apellido} {self.cedula} {self.tipo_usuario} {self.contraseña}"

## @class datos_maestria
# @brief Modelo que almacena información sobre los programas de maestría disponibles.
class datos_maestria(models.Model):
    """
    @brief Modelo que almacena información sobre los programas de maestría disponibles.
    
    Este modelo tiene un campo para el código de la maestría y su nombre.
    """
    cod_maestria = models.IntegerField(primary_key=True)
    nombre_maestria = models.TextField(null=False)

## @class estudiante_datos
# @brief Modelo que almacena los datos específicos de los estudiantes, como su relación con la maestría.
class estudiante_datos(models.Model):
    """
    @brief Modelo que almacena los datos específicos de los estudiantes, como su relación con la maestría.
    
    Este modelo tiene claves foráneas a `Datos_basicos` (para los estudiantes) y `datos_maestria` (para la maestría).
    También almacena información sobre su estado y carrera.
    """
    cedula_estudiante = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_estudiante",
    )  # CLAVE FORANEA

    cod_maestria = models.ForeignKey(
        datos_maestria,
        on_delete=models.CASCADE,
        to_field="cod_maestria",
        db_column="cod_maestria",
    )  # CLAVE FORANEA

    nombre_est = models.TextField(blank=True, null=True)
    apellido_est = models.TextField(blank=True, null=True)
    año_ingreso = models.TextField(null=False)
    estado_estudiante = models.CharField(
        max_length=10,  # Limitar el largo máximo
        choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
        default="Activo"  # Valor por defecto
    )
    carrera = models.TextField(null=False)

## @class roles
# @brief Modelo que define los roles de los usuarios en el sistema.
class roles(models.Model):
    """
    @brief Modelo que define los roles de los usuarios en el sistema.
    
    Este modelo almacena el código y nombre del rol, como `admin`, `profesor`, `estudiante`.
    """
    codigo_rol = models.IntegerField(primary_key=True)
    nombre_rol = models.TextField(null=False)

## @class datos_login
# @brief Modelo que almacena la información de autenticación de los usuarios.
class datos_login(models.Model):
    """
    @brief Modelo que almacena la información de autenticación de los usuarios.
    
    Relaciona al usuario con su tipo de rol y contraseña.
    """
    cedula_usuario = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_usuario",
    )  # CLAVE FORANEA

    contraseña_usuario = models.TextField(null=False)
    tipo_usuario = models.ForeignKey(
        roles, on_delete=models.CASCADE, to_field="codigo_rol", db_column="tipo_usuario"
    )  # CLAVE FORANEA

    @property
    def is_authenticated(self):
        """
        @brief Propiedad que siempre devuelve True, indicando que el usuario está autenticado si existe.
        """
        return True

## @class Cohorte
# @brief Modelo que almacena la información de los cohorte de estudiantes.
class Cohorte(models.Model):
    """
    @brief Modelo que almacena la información de los cohorte de estudiantes.
    
    Define las opciones para los tipos de maestría y sedes de los cohorte.
    Incluye fechas de inicio y fin del cohorte.
    """
    # Definir los posibles valores para 'tipo_maestria' y 'sede_cohorte'
    TIPO_MAESTRIA_CHOICES = [
        ('GG', 'Cs Administrativas / Gerencia General (GG)'),
        ('FI', 'Cs Administrativas / Finanzas (FI)'),
        ('RH', 'Cs Administrativas / Gerencia de Recursos Humanos (RRHH)')
    ]

    SEDE_CHOICES = [
        ('barcelona', 'Barcelona'),
        ('cantaura', 'Cantaura')
    ]

    codigo_cohorte = models.TextField(primary_key=True)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)
    sede_cohorte = models.CharField(max_length=50, choices=SEDE_CHOICES, null=False)
    tipo_maestria = models.CharField(max_length=2, choices=TIPO_MAESTRIA_CHOICES, null=False, blank=True)

    def __str__(self):
        """
        @brief Representación en string del cohorte, incluyendo código, tipo de maestría y sede.
        """
        return f"Cohorte {self.codigo_cohorte} - {self.tipo_maestria} ({self.sede_cohorte})"

## @class materias_pensum
# @brief Modelo que almacena información sobre las materias del pensum de cada maestría.
class materias_pensum(models.Model):
    """
    @brief Modelo que almacena información sobre las materias del pensum de cada maestría.
    
    Este modelo incluye la relación con los profesores y las materias asociadas.
    """
    cod_materia = models.TextField(primary_key=True)
    cod_maestria = models.ForeignKey(
        datos_maestria,
        on_delete=models.CASCADE,
        to_field="cod_maestria",
        db_column="cod_maestria",
    )  # CLAVE FORANEA

    nombre_materia = models.TextField(null=False)
  
## @class AsignarProfesorMateria
# @brief Modelo que asigna profesores a materias dentro de una cohorte específica.
class AsignarProfesorMateria(models.Model):
    """
    @brief Modelo que asigna profesores a materias dentro de una cohorte específica.
    
    Relaciona un profesor con una materia, especificando su fecha de inicio y fin.
    """
    cod_materia = models.ForeignKey(
        materias_pensum,
        on_delete=models.CASCADE,
        to_field="cod_materia",
        db_column="cod_materia",
        blank=True,
        null=True
    )  # CLAVE FORANEA

    nom_materia = models.TextField(null=False, blank=True)

    cedula_profesor = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_profesor",
        blank=True,
        null=True
    )  # CLAVE FORANEA

    nombre_profesor = models.TextField(blank=True, null=True)
    apellido_profesor = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=False)

    codigo_cohorte = models.ForeignKey(
        Cohorte,
        on_delete=models.CASCADE,
        to_field="codigo_cohorte",
        db_column="codigo_cohorte",
        blank=True,
        null=True
    )  # CLAVE FORANEA

## @class PlanificacionProfesor
# @brief Modelo que almacena la planificación de un profesor.
class PlanificacionProfesor(models.Model):
    """
    @brief Modelo que almacena la planificación de un profesor.
    
    Incluye las actividades planificadas y su porcentaje de evaluación dentro de una materia y cohorte específica.
    """
    codplanificacion = models.CharField(
        primary_key=True, max_length=50, db_column="codplanificacion",
    )
    actividades_planificacion = models.TextField(blank=True, null=True)
    actividades_porcentaje = models.TextField(blank=True, null=True)
    cod_materia = models.ForeignKey(
        materias_pensum,
        on_delete=models.CASCADE,
        to_field="cod_materia",
        db_column="cod_materia",
        blank=True, null=True
    )  # CLAVE FORANEA

    codigo_cohorte = models.ForeignKey(
        Cohorte,
        on_delete=models.CASCADE,
        to_field="codigo_cohorte",
        db_column="codigo_cohorte",
        blank=True, null=True
    )  # CLAVE FORANEA

    cedula_profesor = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_profesor",
        blank=True,
        null=True
    )  # CLAVE FORANEA

    nombre_materia = models.TextField(null=False, blank=True)

## @class listado_estudiantes
# @brief Modelo que almacena el listado de estudiantes inscritos en una materia y cohorte específica.
class listado_estudiantes(models.Model):
    """
    @brief Modelo que almacena el listado de estudiantes inscritos en una materia y cohorte específica.
    
    Contiene información sobre el estudiante, la materia y el profesor que la imparte.
    """
    cedula_estudiante = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_estudiante",
    )  # CLAVE FORANEA

    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)
    
    cod_materia = models.ForeignKey(
        materias_pensum,
        on_delete=models.CASCADE,
        to_field="cod_materia",
        db_column="cod_materia",
    )  # CLAVE FORANEA

    codigo_cohorte = models.ForeignKey(
        Cohorte,
        on_delete=models.CASCADE,
        to_field="codigo_cohorte",
        db_column="codigo_cohorte",
    )  # CLAVE FORANEA

    nombre_materia = models.TextField(null=False)
    profesor_ci = models.TextField(null=False)
    nom_profesor_materia = models.TextField(blank=True, null=True)
    ape_profesor_materia = models.TextField(blank=True, null=True)
    nota = models.IntegerField(blank=True, null=True)

    codplanificacion = models.ForeignKey(
        PlanificacionProfesor,
        on_delete=models.CASCADE,
        to_field="codplanificacion",
        db_column="codplanificacion",
        blank=True, null=True
    )  # CLAVE FORANEA


## @class profesores
# @brief Modelo que almacena la información de los profesores.
class profesores(models.Model):
    """
    @brief Modelo que almacena la información de los profesores.
    
    Relaciona a los profesores con las materias y maestrías que imparten.
    """
    ci_profesor = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="ci_profesor",
    )  # CLAVE FORANEA

    nom_profesor_materia = models.TextField(blank=True, null=True)
    ape_profesor_materia = models.TextField(blank=True, null=True)
    cod_maestria_prof = models.ForeignKey(
        datos_maestria,
        on_delete=models.CASCADE,
        to_field="cod_maestria",
        db_column="cod_maestria_prof",
        null=True,  # Cambiar a null=True para permitir valores nulos
    )  # CLAVE FORANEA

## @class tabla_pagos
# @brief Modelo que almacena la información sobre los pagos realizados por los estudiantes.
class tabla_pagos(models.Model):
    """
    @brief Modelo que almacena la información sobre los pagos realizados por los estudiantes.
    
    Relaciona los pagos con el estudiante y proporciona detalles sobre el pago.
    """
    ESTADOS_PAGO = [
        ("Pendiente", "Pendiente"),
        ("Confirmado", "Confirmado"),
        ("Negado", "Negado"),
    ]

    cedula_responsable = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_responsable",
    )  # CLAVE FORANEA

    numero_referencia = models.IntegerField(primary_key=True)
    banco_pago = models.TextField(null=False)
    fecha_pago = models.DateTimeField(null=False)
    monto_pago = models.IntegerField(null=False)
    nombre_estudiante = models.TextField(blank=True, null=True)
    apellido_estudiante = models.TextField(blank=True, null=True)
    estado_pago = models.CharField(max_length=10, choices=ESTADOS_PAGO, default="Pendiente")

    def __str__(self):
        """
        @brief Representación en string del pago, utilizando el nombre del estudiante.
        """
        return f"{self.nombre_estudiante} - {self.estado_pago}"


## @class tabla_solicitudes
# @brief Modelo que almacena la información sobre las solicitudes de los estudiantes.
class tabla_solicitudes(models.Model):
    """
    @brief Modelo que almacena la información sobre las solicitudes de los estudiantes.
    
    Relaciona las solicitudes con los estudiantes y proporciona detalles sobre su estado y tipo.
    """
    cedula_responsable = models.ForeignKey(
        Datos_basicos,
        on_delete=models.CASCADE,
        to_field="cedula",
        db_column="cedula_responsable",
    )  # CLAVE FORANEA

    cod_solicitudes = models.TextField(primary_key=True)
    nombre_estudiante = models.TextField(null=False)
    apellido_estudiante = models.TextField(null=False)
    fecha_solicitud = models.DateTimeField(null=False)
    status_solicitud = models.TextField(null=False)
    tipo_solicitud = models.TextField(null=False)