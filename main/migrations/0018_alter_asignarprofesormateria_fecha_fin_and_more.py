# Generated by Django 5.1 on 2025-02-15 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0017_asignarprofesormateria_nom_materia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asignarprofesormateria',
            name='fecha_fin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='asignarprofesormateria',
            name='fecha_inicio',
            field=models.DateTimeField(),
        ),
    ]
