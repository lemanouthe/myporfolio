"""Sélection de l'environnement de settings.

`DJANGO_SETTINGS_MODULE=config.settings` (inchangé). Le choix dev/prod se fait
via la variable d'environnement `DJANGO_ENV` : "prod" charge prod.py, sinon dev.py.
En prod, docker-compose injecte `DJANGO_ENV=prod` via `env_file: .env`.
"""
import os

if os.getenv("DJANGO_ENV", "dev").lower() == "prod":
    from .prod import *  # noqa: F401,F403
else:
    from .dev import *  # noqa: F401,F403
