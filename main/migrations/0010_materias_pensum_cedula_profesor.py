# Generated by Django 5.1 on 2025-01-27 19:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_cohorte_tipo_maestria_alter_cohorte_sede_cohorte'),
    ]

    operations = [
        migrations.AddField(
            model_name='materias_pensum',
            name='cedula_profesor',
            field=models.ForeignKey(blank=True, db_column='cedula_profesor', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.datos_basicos'),
        ),
    ]
