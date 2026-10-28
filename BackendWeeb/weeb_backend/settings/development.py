#Ce fichier sera utilisé pour le développement local. Il importe tout depuis base.py et définit les spécificités du développement.
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR/ 'db.sqlite3',
    }
}