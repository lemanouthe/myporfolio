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

Le serveur n'exécute **pas** le code source : il héberge seulement `docker-compose.yml`
+ `.env` et **tire l'image** depuis GHCR. Pas besoin de cloner tout le repo ni de builder.

**Setup serveur (une fois)** dans `/home/<user>/projects/myporfolio/` :
```bash
# récupérer les fichiers de déploiement (au choix) :
#   - copier docker-compose.yml (+ docker-compose.proxy.yml, gen-env.sh) via scp, ou
#   - git clone https://github.com/lemanouthe/myporfolio.git .   (le repo sert de source)
./gen-env.sh                                 # génère le .env (secret Django auto, saisie guidée)
docker network create net                   # réseau externe partagé avec le reverse proxy (si absent)
mkdir -p static media logs                   # dossiers montés dans le conteneur
sudo chown -R 1000:1000 static media logs    # uid utilisé par le conteneur
```
Si le serveur n'a **pas encore** de reverse proxy, lancer aussi (une fois, pour tout le
serveur) : `docker compose -f docker-compose.proxy.yml up -d` — voir
[NOTE-SERVEUR-PARTAGE.md](NOTE-SERVEUR-PARTAGE.md). Sinon, ignorer ce fichier.

> Le déploiement auto **ne fait pas** `git pull`. Si tu modifies `docker-compose.yml`,
> re-copie-le (ou `git pull`) manuellement sur le serveur une fois.

**Démarrer / redéployer** (le serveur TIRE l'image, il ne build pas) :
```bash
echo <token> | docker login ghcr.io -u lemanouthe --password-stdin   # si package privé
docker compose up -d --pull always --remove-orphans
```
Au démarrage du conteneur, `backend/start.sh` lance `migrate` + `collectstatic` puis
gunicorn (qui sert à la fois l'API et le SPA Vue). `static/`, `media/`, `logs/` sont des
dossiers du serveur montés dans le conteneur (uid 1000). nginx-proxy détecte `VIRTUAL_HOST`
et route tout vers `web:8010` ; le SPA, l'API, `/static` et `/media` sortent du même conteneur.

**TLS** : géré par acme-companion (Let's Encrypt) via `LETSENCRYPT_HOST`/`LETSENCRYPT_EMAIL`.

## CI/CD (GitHub Actions)

Sur `git push origin main` → 3 jobs : **test** (tests back + build front) → **build-push**
(image `ghcr.io/lemanouthe/myporfolio:latest` construite et poussée sur GHCR) → **deploy**
(SSH sur le serveur : `docker login ghcr` + `docker compose up -d --pull always`, puis
nettoyage scopé `label=com.docker.compose.project=portfolio`). Le serveur ne build ni ne
`git pull` : il tire simplement la nouvelle image.

Secrets repo requis : `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY` (accès SSH). Le push/pull
GHCR utilise le `GITHUB_TOKEN` intégré — aucun secret supplémentaire.

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
