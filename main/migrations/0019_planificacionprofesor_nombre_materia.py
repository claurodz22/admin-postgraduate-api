# Generated by Django 5.1 on 2025-02-15 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_alter_asignarprofesormateria_fecha_fin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='planificacionprofesor',
            name='nombre_materia',
            field=models.TextField(blank=True),
        ),
    ]
