##
# @file settings.py
# @brief Configuración principal para el proyecto Django "adminpostgraduate".
#
# Este archivo contiene las configuraciones del proyecto Django, como la base de datos, las aplicaciones instaladas,
# la autenticación y las configuraciones de CORS, entre otros. Además, se cargan las variables de entorno desde el archivo
# `.env` para configurar las credenciales y otras configuraciones sensibles de manera segura.
#
# @see Django Docs: https://docs.djangoproject.com/en/5.1/topics/settings/
# @see Django Docs Database Settings: https://docs.djangoproject.com/en/5.1/ref/settings/#databases
# @see Django Docs Rest Framework Settings: https://www.django-rest-framework.org/
#

from pathlib import Path
import os

##
# @brief Configuración de la ruta base del proyecto.
# 
# `BASE_DIR` define la ruta base del proyecto Django, que se utiliza para construir rutas relativas dentro del proyecto.
BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv

##
# @brief Cargar variables de entorno desde un archivo `.env`.
# 
# Las variables de entorno, como las credenciales de la base de datos, se cargan desde el archivo `.env.example` que se
# encuentra en la ruta `docker/.env.example`. Esto ayuda a mantener las configuraciones sensibles fuera del código fuente.
ENV_PATH = BASE_DIR / "docker" / ".env.example"
load_dotenv(dotenv_path=ENV_PATH)

##
# @brief Configuración de seguridad y modo de desarrollo.
# 
# Se definen configuraciones clave para la seguridad, como la clave secreta del proyecto y el modo de depuración.
SECRET_KEY = "django-insecure-5)c%-!zyumlks-vp5gs2e_ipn1v#8+wq3vsftnt$&c_x(1o70l"

# Activa o desactiva el modo de depuración. Nunca debe estar habilitado en producción.
DEBUG = True

# Define los hosts permitidos para el servidor, para prevenir ataques de tipo "host header".
ALLOWED_HOSTS = []

##
# @brief Definición de las aplicaciones instaladas.
#
# `INSTALLED_APPS` contiene una lista de todas las aplicaciones Django que están habilitadas en el proyecto, como el admin,
# la autenticación de usuarios, el manejo de sesiones y los paquetes adicionales como Django Rest Framework y CORS.
INSTALLED_APPS = [
    "main",  # La aplicación principal del proyecto
    "django.contrib.admin",  # Interfaz administrativa de Django
    "django.contrib.auth",  # Sistema de autenticación de usuarios
    "django.contrib.contenttypes",  # Sistema de tipos de contenido
    "django.contrib.sessions",  # Manejo de sesiones de usuario
    "django.contrib.messages",  # Sistema de mensajes de usuario
    "django.contrib.staticfiles",  # Manejo de archivos estáticos
    "django_extensions",  # Extensiones útiles para Django
    "rest_framework",  # Django Rest Framework
    "drf_spectacular",  # Generación de esquemas OpenAPI para DRF
    "rest_framework_simplejwt",  # Manejo de JWT para autenticación
    "corsheaders",  # Middleware para permitir CORS (Cross-Origin Resource Sharing)
]

##
# @brief Configuración de CORS (Cross-Origin Resource Sharing).
# 
# Permite que todos los orígenes puedan acceder a los recursos de la API. Esto se utiliza principalmente durante el desarrollo
# cuando se trabaja con aplicaciones frontend que se ejecutan en dominios diferentes.
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

##
# @brief Configuración del middleware.
# 
# `MIDDLEWARE` define la cadena de middleware que se ejecuta para cada solicitud. Cada componente en la lista procesa la
# solicitud antes de pasarla al siguiente middleware.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Seguridad de la aplicación
    "django.contrib.sessions.middleware.SessionMiddleware",  # Manejo de sesiones
    "django.middleware.common.CommonMiddleware",  # Funciones comunes como la redirección de URLs
    "django.middleware.csrf.CsrfViewMiddleware",  # Prevención de CSRF (Cross Site Request Forgery)
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Manejo de autenticación
    "django.contrib.messages.middleware.MessageMiddleware",  # Mensajes de usuario
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Protección contra ataques de clickjacking
    "corsheaders.middleware.CorsMiddleware",  # Middleware para CORS
]

##
# @brief Configuración de URLs.
# 
# `ROOT_URLCONF` define el archivo que maneja las URLs del proyecto. Este archivo se utiliza para enrutar solicitudes
# hacia vistas específicas en el proyecto.
ROOT_URLCONF = "adminpostgraduate.urls"

##
# @brief Configuración de plantillas.
# 
# La configuración de `TEMPLATES` permite la renderización de vistas HTML usando el sistema de plantillas de Django.
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Backend para el sistema de plantillas de Django
        "DIRS": [],  # Directorios donde se buscan las plantillas
        "APP_DIRS": True,  # Habilita la búsqueda de plantillas dentro de las aplicaciones
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Contexto de depuración
                "django.template.context_processors.request",  # Contexto para solicitudes
                "django.contrib.auth.context_processors.auth",  # Contexto para autenticación de usuarios
                "django.contrib.messages.context_processors.messages",  # Contexto para mensajes
            ],
        },
    },
]

##
# @brief Configuración WSGI.
# 
# Define la aplicación WSGI que se utiliza para ejecutar el servidor en producción.
WSGI_APPLICATION = "adminpostgraduate.wsgi.application"

##
# @brief Configuración de la base de datos.
#
# Se configura la base de datos PostgreSQL utilizando las variables de entorno para gestionar las credenciales de manera segura.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",  # Motor de base de datos PostgreSQL
        "NAME": os.getenv("POSTGRES_DB"),  # Nombre de la base de datos (obtenido desde las variables de entorno)
        "USER": os.getenv("POSTGRES_USER"),  # Usuario de la base de datos
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),  # Contraseña de la base de datos
        "HOST": os.getenv("POSTGRES_HOST"),  # Dirección del host de la base de datos
        "PORT": os.getenv("DB_PORT"),  # Puerto del servidor de base de datos
    }
}

##
# @brief Configuración de validadores de contraseñas.
#
# Django proporciona una serie de validadores de contraseñas para mejorar la seguridad, asegurando que las contraseñas
# de los usuarios sean lo suficientemente fuertes.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

##
# @brief Configuración de internacionalización y zona horaria.
#
# Se definen la lengua predeterminada y la zona horaria para el proyecto, así como el uso de la internacionalización.
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

##
# @brief Configuración de archivos estáticos.
#
# `STATIC_URL` define la URL desde la cual se sirven los archivos estáticos, como CSS, JavaScript e imágenes.
STATIC_URL = "static/"

##
# @brief Configuración del tipo de campo de clave primaria.
#
# Define el tipo predeterminado para las claves primarias en los modelos de Django. Se utiliza un campo de tipo `BigAutoField`.
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

##
# @brief Configuración del framework REST.
#
# Configura Django Rest Framework para utilizar un esquema automático de OpenAPI y una clase de autenticación personalizada.
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",  # Generación automática de esquemas OpenAPI
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'main.authentication.CustomJWTAuthentication',  # Autenticación personalizada basada en JWT
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',  # Requiere que el usuario esté autenticado
    ],
}

##
# @brief Configuración de JSON Web Token (JWT).
#
# Se configura la duración de los tokens de acceso y refresco, así como el comportamiento de rotación y validación.
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Duración del access token (30 minutos)
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),    # Duración del refresh token (1 día)
    'ROTATE_REFRESH_TOKENS': False,                  # No rota los tokens de refresco
    'BLACKLIST_AFTER_ROTATION': True,                # Invalida los tokens de refresco rotados
    'UPDATE_LAST_LOGIN': False,                      # No actualiza la fecha del último acceso del usuario
}
