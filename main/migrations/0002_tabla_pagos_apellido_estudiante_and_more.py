# Generated by Django 5.1 on 2025-01-06 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tabla_pagos',
            name='apellido_estudiante',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tabla_pagos',
            name='nombre_estudiante',
            field=models.TextField(blank=True, null=True),
        ),
    ]
