# Generated by Django 5.1 on 2025-01-07 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_estudiante_datos_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estudiante_datos',
            name='estado_estudiante',
            field=models.CharField(choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')], default='Activo', max_length=10),
        ),
    ]
