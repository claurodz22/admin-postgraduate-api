'''
Modelos: define la estructura de los datos de una carga. 
Los modelos se pueden utilizar para: 
- Validar solicitudes de manera básica
- Crear plantillas de mapeo para transformar datos
- Generar un tipo de datos definido por el usuario (UDT) al crear un SDK
'''

from django.db import models

class Datos_basicos(models.Model):
    cedula = models.TextField(primary_key=True) # CEDULA = PRIMARY KEY
    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)
    tipo_usuario = models.IntegerField(null=False)
    contraseña = models.TextField(null=False)

class datos_maestria(models.Model):
    cod_maestria = models.IntegerField(primary_key=True)
    nombre_maestria = models.TextField(null=False)

class estudiante_datos(models.Model):
    cedula_estudiante = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='cedula_estudiante')  # CLAVE FORANEA

    cod_maestria = models.ForeignKey(datos_maestria, 
    on_delete=models.CASCADE, to_field='cod_maestria', db_column ='cod_maestria')  # CLAVE FORANEA
    
    nombre_est = models.TextField(blank=True,null=True)
    apellido_est = models.TextField(blank=True,null=True)
    año_ingreso = models.TextField(null=False)
    estado_estudiante = models.CharField(
        max_length=10,  # Limitar el largo máximo
        choices=[("Activo", "Activo"), ("Inactivo", "Inactivo")],
        default="Activo"  # Valor por defecto
    )
    carrera = models.TextField(null=False)
    
class Cohorte(models.Model):
    codigo_cohorte = models.TextField(primary_key=True)
    fecha_inicio = models.DateTimeField(null=False)
    fecha_fin = models.DateTimeField(null=  False)
    sede_cohorte = models.TextField(null=False)
        
class roles(models.Model):
    codigo_rol = models.IntegerField(primary_key=True)
    nombre_rol = models.TextField(null=False)

class datos_login(models.Model):
    cedula_usuario = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='cedula_usuario')  # CLAVE FORANEA

    tipo_usuario = models.ForeignKey(roles, 
    on_delete=models.CASCADE, to_field='codigo_rol', db_column ='tipo_usuario')  # CLAVE FORANEA    

    contraseña_usuario = models.TextField(null=False)

class materias_pensum(models.Model):
    cod_materia = models.TextField(primary_key=True)
    nombre_materia = models.TextField(null=False)
    nom_profesor_materia = models.TextField(blank=True,null=True)
    ape_profesor_materia = models.TextField(blank=True,null=True)

    cod_maestria = models.ForeignKey(datos_maestria, 
    on_delete=models.CASCADE, to_field='cod_maestria', db_column ='cod_maestria')  # CLAVE FORANEA

class listado_estudiantes(models.Model):

    cedula_estudiante = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='cedula_estudiante')  # CLAVE FORANEA

    nombre = models.TextField(null=False)
    apellido = models.TextField(null=False)

    cod_materia = models.ForeignKey(materias_pensum, 
    on_delete=models.CASCADE, to_field='cod_materia', db_column ='cod_materia')  # CLAVE FORANEA

    codigo_cohorte = models.ForeignKey(Cohorte, 
    on_delete=models.CASCADE, to_field='codigo_cohorte', db_column ='codigo_cohorte')  # CLAVE FORANEA
    
    nombre_materia = models.TextField(null=False)
    
    profesor_ci = models.TextField(null=False)

    nom_profesor_materia = models.TextField(blank=True,null=True)
    ape_profesor_materia = models.TextField(blank=True,null=True)


class profesores(models.Model):
    ci_profesor = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='ci_profesor')  # CLAVE FORANEA

    nom_profesor_materia = models.TextField(blank=True,null=True)
    ape_profesor_materia = models.TextField(blank=True,null=True)
    
    cod_maestria_prof = models.ForeignKey(datos_maestria, 
    on_delete=models.CASCADE, to_field='cod_maestria', db_column ='cod_maestria_prof')  # CLAVE FORANEA


class tabla_pagos(models.Model):
    cedula_responsable = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='cedula_responsable')  # CLAVE FORANEA
    
    numero_referencia = models.IntegerField(primary_key=True)
    banco_pago = models.TextField(null=False)
    fecha_pago = models.DateTimeField(null=False)
    monto_pago = models.DecimalField(null=False)
    nombre_estudiante = models.TextField(blank=True,null=True)
    apellido_estudiante = models.TextField(blank=True,null=True)

class tabla_solicitudes(models.Model):
    cedula_responsable = models.ForeignKey(Datos_basicos, 
    on_delete=models.CASCADE, to_field='cedula', db_column ='cedula_responsable')  # CLAVE FORANEA
    
    cod_solicitudes = models.TextField(primary_key=True)
    nombre_estudiante = models.TextField(null=False)
    apellido_estudiante = models.TextField(null=False)
    fecha_solicitud = models.DateTimeField(null=False)
    status_solicitud = models.TextField(null=False)
    tipo_solicitud = models.TextField(null=False)