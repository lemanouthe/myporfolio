"""Réglages communs à tous les environnements.

Ne pas utiliser directement : voir `dev.py` / `prod.py`, sélectionnés par
`__init__.py` selon la variable d'environnement `DJANGO_ENV` (défaut : dev).
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Chemins & environnement
# ---------------------------------------------------------------------------
# base.py -> config/settings/base.py ; remonter à backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR.parent / ".env")

# Compiled Vue build (copied into the image at build time). Serves the SPA
# (index.html) and its /static/assets/* through Django/WhiteNoise — single
# origin, single container, no CORS.
FRONTEND_DIST = BASE_DIR / "frontend_build"


def env_bool(key, default=False):
    return os.getenv(key, str(default)).lower() in ("1", "true", "yes", "on")


# ---------------------------------------------------------------------------
# Sécurité
# ---------------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-insecure-change-me")
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
CSRF_TRUSTED_ORIGINS = [
    o for o in os.getenv("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",") if o
]

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "portfolio",
]

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # serves /static (admin, DRF)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------------------------
# URLs & WSGI
# ---------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_DIST],  # so the catch-all view finds index.html
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------------------------
# Base de données
# ---------------------------------------------------------------------------
# POSTGRES_* fournis par docker-compose en prod. Fallback SQLite pour un run
# local sans conteneur de base de données — zéro config.
if os.getenv("POSTGRES_DB"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", "db"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------------
# Authentification
# ---------------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Fichiers statiques & media
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# Vue's assets are already content-hashed, and index.html references them by
# fixed name — so use the non-manifest storage (compression only) to avoid a
# second hashing pass that would break those references.
STATICFILES_DIRS = [FRONTEND_DIST] if FRONTEND_DIST.exists() else []
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# ---------------------------------------------------------------------------
# Django REST Framework
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_THROTTLE_CLASSES": ["rest_framework.throttling.ScopedRateThrottle"],
    "DEFAULT_THROTTLE_RATES": {"contact": "5/hour"},
}

# ---------------------------------------------------------------------------
# Email (notifications de contact)
# ---------------------------------------------------------------------------
# Hôte/creds communs ; le backend (console vs SMTP) est choisi par dev.py/prod.py.
EMAIL_HOST = os.getenv("EMAIL_HOST", "")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "portfolio@localhost")
CONTACT_NOTIFY_EMAIL = os.getenv("CONTACT_NOTIFY_EMAIL", "mamoutoudoumbia89@gmail.com")
