#!/usr/bin/env sh
# Démarrage du conteneur web : migrations, statics, puis gunicorn (port 8010).
set -e

echo "📦 Migrations..."
python manage.py migrate --noinput

# Données initiales : chargées UNIQUEMENT si la base est vide (premier déploiement).
# Évite d'écraser le contenu édité via l'admin aux redémarrages suivants.
echo "🌱 Données initiales (si base vide)..."
if python manage.py shell -c "import sys; from portfolio.models import Project; sys.exit(0 if Project.objects.exists() else 1)"; then
  echo "  → base déjà peuplée, chargement ignoré."
else
  python manage.py loaddata initial
  echo "  → fixture 'initial' chargée."
fi

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
