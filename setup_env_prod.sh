#!/usr/bin/env bash
# Génère le .env de PRODUCTION dans la CI (GitHub Actions), puis il est copié
# sur le serveur par scp (job before-deploy).
#
# Valeurs non sensibles : en dur ci-dessous.
# Valeurs sensibles : lues depuis l'environnement (secrets GitHub) :
#   DJANGO_SECRET_KEY, POSTGRES_PASSWORD, EMAIL_HOST_PASSWORD
#
# ⚠️ DJANGO_SECRET_KEY doit être "URL-safe" (A-Z a-z 0-9 _ -) : PAS de $ # " ' espace,
#    sinon Docker Compose casse le .env (interpolation $VAR, commentaire #).
#    Générer : python3 -c "import secrets; print(secrets.token_urlsafe(64))"
set -e

cat > .env <<EOF
# Généré par setup_env_prod.sh (CI) — ne pas éditer à la main sur le serveur.

# --- Reverse proxy ---
VIRTUAL_HOST=lemanouthe.com
LETSENCRYPT_EMAIL=mamoutoudoumbia89@gmail.com

# --- Django ---
DJANGO_ENV=prod
DJANGO_SECRET_KEY=${DJANGO_SECRET_KEY}
DJANGO_ALLOWED_HOSTS=lemanouthe.com,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=https://lemanouthe.com

# --- PostgreSQL (base externe) ---
POSTGRES_DB=portfolio
POSTGRES_USER=portfoliouser
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_HOST=172.17.0.1
POSTGRES_PORT=5432

# --- Email ---
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=mamoutoudoumbia89@gmail.com
EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=mamoutoudoumbia89@gmail.com
CONTACT_NOTIFY_EMAIL=mamoutoudoumbia89@gmail.com
EOF

echo "✓ .env généré ($(wc -l < .env) lignes)"
