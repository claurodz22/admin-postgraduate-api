# Generated by Django 5.1 on 2025-01-06 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_tabla_pagos_apellido_estudiante_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cohorte',
            name='profesor_cohorte',
        ),
        migrations.RemoveField(
            model_name='listado_estudiantes',
            name='nombre_profesor_ci',
        ),
        migrations.RemoveField(
            model_name='materias_pensum',
            name='profesor_materia',
        ),
        migrations.RemoveField(
            model_name='profesores',
            name='profesor',
        ),
        migrations.AddField(
            model_name='listado_estudiantes',
            name='ape_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='listado_estudiantes',
            name='nom_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='materias_pensum',
            name='ape_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='materias_pensum',
            name='nom_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profesores',
            name='ape_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profesores',
            name='nom_profesor_materia',
            field=models.TextField(blank=True, null=True),
        ),
    ]