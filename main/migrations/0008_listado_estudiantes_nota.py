# Generated by Django 5.1 on 2025-01-15 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_datos_basicos_correo'),
    ]

    operations = [
        migrations.AddField(
            model_name='listado_estudiantes',
            name='nota',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
