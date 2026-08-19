# Portfolio — Mamoutou (Django + Vue)

Portfolio dev backend. API Django/DRF + front Vue 3, déployé via Docker Compose derrière nginx.
Voir [`note-dev-portfolio.md`](note-dev-portfolio.md) pour la conception (design, archi, déploiement).

## Structure

```
backend/                    Django + DRF — sert l'API ET le SPA Vue compilé (WhiteNoise)
  config/settings/base.py   réglages communs
  config/settings/dev.py    DEBUG, email console (défaut)
  config/settings/prod.py   DEBUG off, cookies sécurisés, email SMTP
frontend/                   Vue 3 + Vite (dev sur :5173 ; build intégré à l'image en prod)
backend/start.sh            unique sh : entrypoint du conteneur (migrate + collectstatic + gunicorn)
docker-compose.yml          un seul service `web` (BD PostgreSQL externe), réseau externe `net`
```

Settings en module : `DJANGO_ENV=prod` charge `prod.py`, sinon `dev.py` (défaut).
`DJANGO_SETTINGS_MODULE` reste `config.settings`. En prod, `.env` fixe `DJANGO_ENV=prod`.

**Un seul conteneur en prod** : l'image Django embarque le build Vue et le sert en
même origine (`/` = SPA, `/api` = API, `/static` + `/media` par WhiteNoise/Django).
Pas de CORS. Le **reverse proxy (nginx-proxy + acme-companion)** est un conteneur
séparé sur le réseau externe `net` — il route `VIRTUAL_HOST` → `web:8010` et gère TLS.

## Développement local

Deux terminaux. Le venv est optionnel (dev seulement) et se crée **hors du projet**.
Le backend tombe sur SQLite si aucun `POSTGRES_DB` n'est défini — zéro config.

```bash
# Terminal 1 — backend (http://localhost:8000)
python3 -m venv ../.venv && source ../.venv/bin/activate
pip install -r backend/requirements.txt
python backend/manage.py migrate
python backend/manage.py createsuperuser     # pour saisir le contenu via l'admin
python backend/manage.py runserver

# Terminal 2 — frontend (http://localhost:5173)
cd frontend && npm install && npm run dev
```
Admin : http://localhost:8000/admin/. Le proxy Vite renvoie `/api` vers `:8000` (same-origin → pas de CORS).

## Tests

```bash
source ../.venv/bin/activate && python backend/manage.py test   # backend
cd frontend && npm run build                                    # le front compile
```

## Production (Docker Compose)

Aucun venv : tout est dans les conteneurs.

Le serveur n'exécute **pas** le code source et ne clone **pas** le repo : la CI lui **copie**
(`scp`) `docker-compose.yml` + `.env`, et il **tire l'image** depuis GHCR. Tout est piloté
par le push GitHub.

**Setup serveur (une fois)** :
```bash
mkdir -p /home/<user>/projects/myporfolio       # dossier cible du scp (doit exister)
docker network create net                        # réseau partagé avec le reverse proxy (si absent)
```
Si le serveur n'a **pas encore** de reverse proxy, lancer aussi (une fois, pour tout le
serveur) : `docker compose -f docker-compose.proxy.yml up -d` — voir
[NOTE-SERVEUR-PARTAGE.md](NOTE-SERVEUR-PARTAGE.md). Sinon, ignorer ce fichier.

Le reste est **automatique** : `git push origin main` → la CI génère le `.env`, le copie
avec le compose, et déploie. `backend/start.sh` (dans l'image) lance `migrate` +
`collectstatic` + gunicorn ; `static/`, `media/`, `logs/` sont créés/montés au déploiement.
nginx-proxy route `VIRTUAL_HOST` → `web:8010` ; TLS par acme-companion.

## CI/CD (GitHub Actions)

Sur `git push origin main`, 4 jobs s'enchaînent :
1. **test** — tests backend + build front (vérif compilation).
2. **build-push** — build de l'image (front + back) → push `ghcr.io/lemanouthe/myporfolio:latest`.
3. **before-deploy** — `setup_env_prod.sh` génère le `.env` depuis les secrets, puis `scp`
   copie `.env` + `docker-compose.yml` sur le serveur.
4. **deploy** — SSH : `docker login ghcr` + `docker compose up -d --pull always`, nettoyage
   scopé `label=com.docker.compose.project=portfolio`. Le serveur ne build ni ne `git pull`.

**Secrets repo à créer** (Settings → Secrets and variables → Actions) :

| Secret | Rôle |
|---|---|
| `SERVER_HOST` | IP / domaine du serveur (SSH) |
| `SERVER_USER` | utilisateur SSH (ex. `ubuntu`) |
| `SERVER_SSH_KEY` | clé privée SSH |
| `DJANGO_SECRET_KEY` | secret Django (génère une longue chaîne aléatoire) |
| `POSTGRES_PASSWORD` | mot de passe de la base |
| `EMAIL_HOST_PASSWORD` | mot de passe SMTP (app password Gmail) |

Le push/pull GHCR utilise le `GITHUB_TOKEN` intégré — pas de secret supplémentaire. Les
valeurs **non sensibles** (domaine, nom/host BD, SMTP host, emails) sont en dur dans
`setup_env_prod.sh` — édite-les là si besoin.

## Cohabitation avec d'autres projets sur le serveur

Ce projet est **isolé** : `name: portfolio` dans le compose préfixe toutes ses ressources
(`portfolio-web-1`, image `portfolio-web`). La base PostgreSQL est **externe** (sur le serveur),
donc ce projet ne crée ni conteneur `db` ni volume de données.

Une mise à jour **n'impacte pas** les autres conteneurs :
- `docker compose up -d --pull always` ne (re)crée **que** les services de ce projet. Il ne
  touche ni les conteneurs, ni les images, ni les volumes des autres projets.
- Aucun port hôte n'est publié (`expose` seul) → **zéro conflit de port**.
- Le réseau `net` est `external` → Compose ne le crée ni ne le supprime jamais ; les
  autres projets qui y sont attachés ne sont pas affectés.
- La base PostgreSQL est externe (non gérée par ce compose) → aucun risque de la recréer/supprimer.

**À FAIRE pour nettoyer sans risque** (images de ce projet devenues obsolètes après rebuild) :
```bash
docker image prune -f          # supprime UNIQUEMENT les images "dangling" (sans tag)
```

**À NE JAMAIS FAIRE sur ce serveur partagé** (touche tous les projets) :
```bash
docker system prune -a         # ✗ supprime toutes les images/volumes inutilisés des AUTRES projets
docker image prune -a          # ✗ idem pour les images
docker compose down -v         # ✗ supprimerait des volumes (ici surtout à éviter par principe)
```
Pour arrêter ce projet seul, sans rien supprimer d'autre : `docker compose stop`
(la base étant externe, elle n'est de toute façon jamais touchée par ce compose).

## API

| Méthode | Endpoint | Rôle |
|---|---|---|
| GET | `/api/projects/` | études de cas |
| GET | `/api/skills/` | groupes + compétences |
| GET | `/api/education/` | formations |
| GET | `/api/certifications/` | certifications |
| GET | `/api/appointments/` | créneaux proposés + créneaux déjà pris |
| POST | `/api/contact/` | message (throttle 5/h/IP + honeypot) |
| POST | `/api/appointments/` | réserver un créneau (throttle 10/h/IP + honeypot) |
