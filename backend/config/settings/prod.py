"""Environnement de production (conteneur Docker derrière nginx-proxy)."""
import os

from .base import *  # noqa: F401,F403

DEBUG = False

# SMTP par défaut (surchargé si DJANGO_EMAIL_BACKEND est défini).
EMAIL_BACKEND = os.getenv(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend"
)

# TLS terminé par le reverse proxy (nginx-proxy + acme-companion).
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
