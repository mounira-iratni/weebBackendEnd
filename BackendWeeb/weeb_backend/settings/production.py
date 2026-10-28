#contrairement au mode de developpement, nous devons appliquer nos régles de sécurites

import os # Un module Python standard qui nous permet d'interagir avec le système d'exploitation, et plus particulièrement de lire les variables d'environnement .env
import dj_database_url # Le package que nous avons installé pour nous simplifier la configuration de la base de données
from .base import * # Cette ligne est fondamentale. Elle dit : "Charge toutes les configurations du fichier base.py". Cela nous évite de dupliquer des dizaines de lignes (INSTALLED_APPS, MIDDLEWARE, etc.) et nous permet de nous concentrer uniquement sur ce qui change en production.

 # ==============================================================
 # Sécurité
 # ==============================================================

SECURITY_KEY = os.environ.get('SECRET_KEY')
DEBUG = False #  impérativement être à False pour ne jamais exposer d'informations internes. Les erreurs doivent être gérées silencieusement et enregistrées dans des logs ou des outils de monitoring, 
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')  # Récupère les hôtes autorisés depuis les variables d'environnement
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', '').split(',')  # Récupère les origines autorisées pour CORS depuis les variables d'environnement

# ==============================================================
# Base de données
# ==============================================================
#Cette fonction va chercher une variable d'environnement (par défaut DATABASE_URL), qui contient une URL de connexion complète fournie par notre hébergeur de base de données (Render, Railway, Supabase...).

DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        ssl_require=True
    )
}

#==============================================================
# Fichiers statiques (WHITENOISE)
#==============================================================

STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'