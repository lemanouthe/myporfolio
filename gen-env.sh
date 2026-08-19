#!/usr/bin/env bash
# Génère le fichier .env de PRODUCTION (à lancer sur le serveur, dans ce dossier).
#   - DJANGO_SECRET_KEY générée automatiquement (forte, aléatoire)
#   - valeurs demandées de façon interactive (défauts entre crochets)
#   - mots de passe saisis en masqué
# Le .env produit est gitignoré : il ne part JAMAIS dans le repo.
#
#   ./gen-env.sh
set -euo pipefail
cd "$(dirname "$0")"

ENV_FILE=".env"

if [ -f "$ENV_FILE" ]; then
  ans=""
  read -rp "⚠ $ENV_FILE existe déjà. L'écraser ? [y/N] " ans || true
  case "$ans" in [yY]*) ;; *) echo "Annulé."; exit 0 ;; esac
fi

# ask VAR "libellé" "défaut"  — valeur préexistante (env) prioritaire comme défaut
ask() {
  local var="$1" prompt="$2" def="${3:-}" input=""
  local shown="${!var:-$def}"
  read -rp "$prompt [$shown] : " input || true
  printf -v "$var" '%s' "${input:-$shown}"
}

# ask_secret VAR "libellé"  — saisie masquée, pas de défaut affiché
ask_secret() {
  local var="$1" prompt="$2" input=""
  if [ -n "${!var:-}" ]; then return; fi   # déjà fourni via l'environnement
  read -rsp "$prompt : " input || true; echo
  printf -v "$var" '%s' "$input"
}

gen_secret() {
  if command -v python3 >/dev/null 2>&1; then
    python3 -c "import secrets; print(secrets.token_urlsafe(64))"
  else
    openssl rand -base64 64 | tr -d '\n='
  fi
}

echo "=== Génération de $ENV_FILE (production) ==="
DJANGO_SECRET_KEY="$(gen_secret)"

ask        VIRTUAL_HOST         "Domaine du site"              "lemanouthe.com"
ask        LETSENCRYPT_EMAIL    "Email Let's Encrypt"          "mamoutoudoumbia89@gmail.com"
ask        POSTGRES_DB          "Nom de la base"               "portfolio"
ask        POSTGRES_USER        "Utilisateur BD"               "portfoliouser"
ask_secret POSTGRES_PASSWORD    "Mot de passe BD"
ask        POSTGRES_HOST        "Hôte BD"                      "host.docker.internal"
ask        POSTGRES_PORT        "Port BD"                      "5432"
ask        EMAIL_HOST           "SMTP host"                    "smtp.gmail.com"
ask        EMAIL_PORT           "SMTP port"                    "587"
ask        EMAIL_HOST_USER      "SMTP utilisateur"             "mamoutoudoumbia89@gmail.com"
ask_secret EMAIL_HOST_PASSWORD  "SMTP mot de passe (app password)"
ask        CONTACT_NOTIFY_EMAIL "Email de réception contact"   "mamoutoudoumbia89@gmail.com"

umask 077   # le fichier sera lisible par le seul propriétaire
cat > "$ENV_FILE" <<EOF
# Généré par gen-env.sh — NE PAS COMMITER

# --- Reverse proxy (nginx-proxy + acme-companion) ---
VIRTUAL_HOST=$VIRTUAL_HOST
LETSENCRYPT_EMAIL=$LETSENCRYPT_EMAIL

# --- Django ---
DJANGO_ENV=prod
DJANGO_SECRET_KEY=$DJANGO_SECRET_KEY
DJANGO_ALLOWED_HOSTS=$VIRTUAL_HOST,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=https://$VIRTUAL_HOST

# --- PostgreSQL (base externe) ---
POSTGRES_DB=$POSTGRES_DB
POSTGRES_USER=$POSTGRES_USER
POSTGRES_PASSWORD=$POSTGRES_PASSWORD
POSTGRES_HOST=$POSTGRES_HOST
POSTGRES_PORT=$POSTGRES_PORT

# --- Email (notifications de contact) ---
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=$EMAIL_HOST
EMAIL_PORT=$EMAIL_PORT
EMAIL_HOST_USER=$EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=$EMAIL_HOST_PASSWORD
EMAIL_USE_TLS=true
DEFAULT_FROM_EMAIL=$EMAIL_HOST_USER
CONTACT_NOTIFY_EMAIL=$CONTACT_NOTIFY_EMAIL
EOF

chmod 600 "$ENV_FILE"
echo "✓ $ENV_FILE généré (permissions 600, non commité)."
echo "  Secret Django généré automatiquement. Relis le fichier avant de déployer."
