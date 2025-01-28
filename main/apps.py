##
# @file apps.py
# @brief Configuración de la aplicación Django llamada "main".
#
# Este archivo contiene la configuración para la aplicación Django llamada "main". La clase `MainConfig`
# hereda de `AppConfig` y define la configuración básica para la aplicación, como el nombre de la aplicación
# y el tipo de campo automático para los identificadores de base de datos. Este archivo generalmente es generado
# automáticamente cuando se crea una nueva aplicación en Django.
#
# @see Django Docs: https://docs.djangoproject.com/en/stable/ref/applications/
#

from django.apps import AppConfig

class MainConfig(AppConfig):
    """
    @brief Configuración de la aplicación "main".
    
    La clase `MainConfig` es la configuración de la aplicación Django llamada "main". 
    En este archivo, se define el campo automático por defecto para los identificadores de la base de datos
    y se establece el nombre de la aplicación.
    """

    default_auto_field = 'django.db.models.BigAutoField'  # Definir el campo automático por defecto como BigAutoField
    name = 'main'  # Nombre de la aplicación Django
