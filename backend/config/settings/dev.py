"""Environnement de développement local (runserver, DEBUG)."""
import os

from .base import *  # noqa: F401,F403

DEBUG = True

# Les emails de contact sont affichés dans la console (aucun envoi réel).
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
