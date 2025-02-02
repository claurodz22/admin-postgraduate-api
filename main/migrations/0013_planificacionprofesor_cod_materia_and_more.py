# Generated by Django 5.1 on 2025-02-02 14:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_planificacionprofesor_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionprofesor',
            name='cod_materia',
            field=models.ForeignKey(blank=True, db_column='cod_materia', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.materias_pensum'),
        ),
        migrations.AddField(
            model_name='planificacionprofesor',
            name='codigo_cohorte',
            field=models.ForeignKey(blank=True, db_column='codigo_cohorte', null=True, on_delete=django.db.models.deletion.CASCADE, to='main.cohorte'),
        ),
    ]
