#!/usr/bin/env sh
# Démarrage du conteneur web : migrations, statics, puis gunicorn (port 8010).
set -e

echo "📦 Migrations..."
python manage.py migrate --noinput

echo "📁 Fichiers statiques..."
python manage.py collectstatic --noinput --clear

echo "🌐 Gunicorn sur :8010..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8010 \
  --workers 3 \
  --timeout 120 \
  --keep-alive 5 \
  --max-requests 1000 \
  --max-requests-jitter 50 \
  --access-logfile - \
  --error-logfile -
