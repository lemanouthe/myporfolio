# Note — Cohabitation du projet `portfolio` sur le serveur partagé

À l'attention des dev/ops des **autres projets** hébergés sur ce serveur.
Ce document décrit comment le projet **portfolio** (Django + Vue, dev : Doumbia Mamoutou)
cohabite avec vos projets, ce dont il dépend, et ce qu'il ne faut pas casser.

---

## TL;DR

- Le portfolio tourne dans **son propre projet Docker Compose** nommé `portfolio`.
  Toutes ses ressources sont préfixées `portfolio-*` / `portfolio_*` → **aucune collision**
  avec vos conteneurs, images ou volumes.
- Ses mises à jour (`docker compose up -d --build`) **ne touchent que lui**.
- Il **ne publie aucun port hôte** → zéro conflit de port.
- Il **s'attache** au reverse proxy partagé (réseau `net` + nginx-proxy) mais ne le
  gère pas et ne le modifie pas.

---

## Ce dont le portfolio DÉPEND (infra partagée, à garder en vie)

Le portfolio suppose que l'infra suivante existe déjà sur le serveur — probablement
gérée par l'un de vos projets ou par l'admin :

| Ressource | Rôle | Impact si supprimée |
|---|---|---|
| Réseau Docker externe **`net`** | relie les apps au reverse proxy | le portfolio ne démarre plus |
| Conteneur **nginx-proxy** (jwilder/nginxproxy) | routage HTTP par `VIRTUAL_HOST` | le portfolio devient injoignable |
| Conteneur **acme-companion** | certificats TLS Let's Encrypt | plus de HTTPS auto |

> Si **aucun** de vos projets ne fournit déjà nginx-proxy + acme-companion + le réseau
> `net`, un fichier prêt à l'emploi est fourni : **`docker-compose.proxy.yml`**.
> À lancer **une seule fois** pour tout le serveur :
>
> ```bash
> docker ps --filter "publish=80"     # vérifier qu'aucun proxy n'écoute déjà sur :80
> docker network create net
> docker compose -f docker-compose.proxy.yml up -d
> ```
>
> ⚠️ Ne PAS le lancer si un reverse proxy existe déjà (conflit sur les ports 80/443).

Le portfolio se déclare auprès de nginx-proxy via ces variables (dans son `.env`) :
`VIRTUAL_HOST`, `VIRTUAL_PORT=8010`, `LETSENCRYPT_HOST`, `LETSENCRYPT_EMAIL`.

---

## Ce que le portfolio CRÉE (et qui lui est propre)

- Conteneur : `portfolio-web-1` (Django+Vue, gunicorn :8010 interne). **Un seul conteneur.**
- Dossiers montés (bind) dans son propre répertoire : `./static`, `./media`, `./logs`.
- Image buildée : `portfolio-web`.
- **Base de données : EXTERNE** (créée sur le serveur). Le portfolio ne lance pas de
  conteneur PostgreSQL ni de volume — il se connecte via `POSTGRES_*` (voir `.env`).

Rien de tout cela n'entre en conflit avec vos ressources tant que vos projets portent
un **nom de projet Compose différent** (ce qui est le cas par défaut si vos dossiers
diffèrent, ou si vous fixez `name:` dans vos compose).

---

## Règles pour ne rien casser (des deux côtés)

**À NE PAS faire sur ce serveur partagé** (ces commandes touchent TOUS les projets) :

```bash
docker system prune -a      # ✗ supprime images/volumes inutilisés de TOUS les projets
docker image prune -a       # ✗ idem, images
docker network rm net       # ✗ casse le routage de toutes les apps derrière le proxy
docker compose down -v      # ✗ (dans un projet) supprime SON volume de données
```

**Nettoyage sûr** (n'affecte que les images orphelines, sans tag) :

```bash
docker image prune -f       # ✓ supprime seulement les images "dangling"
```

**Un domaine par projet** : chaque `VIRTUAL_HOST` doit être **unique**. Le portfolio
utilise le sien ; n'attribuez pas le même domaine à deux projets, sinon nginx-proxy
route au hasard.

---

## En résumé

- Vous pouvez déployer/redéployer vos projets librement : le portfolio n'y touche pas.
- Le portfolio se redéploie de son côté sans vous impacter.
- **Seul terrain commun** : le réseau `net` + nginx-proxy + acme-companion. Tant qu'ils
  restent en place, tout le monde cohabite sans friction.

Contact : Doumbia Mamoutou — mamoutoudoumbia89@gmail.com
