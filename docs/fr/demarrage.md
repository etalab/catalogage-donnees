# Démarrage rapide

Cette page indique les quelques étapes qui vous permettront d'avoir un projet fonctionnel à partir duquel travailler.

* 👉 Je suis une personne non-technique et je souhaite rapidement lancer le projet : jetez un oeil à [Raccourci : usage Docker](#raccourci--usage-docker)
* 👉 Je suis une personne technique et je souhaite participer au développement détaillé : suivez le guide !

**Table des matières**

* [Usage Docker](#raccourci--usage-docker)
* [Prérequis](#pr%C3%A9requis)
* [Interagir avec le projet](#interagir-avec-le-projet)
* [Configuration](#configuration)

---

## Usage Docker

Pour faciliter un démarrage rapide du projet, une configuration `docker-compose` est disponible, comprenant le serveur, le client, et une base de données.

Installez d'abord les outils nécessaires :

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

Puis lancez :

```
make compose-up
```

Le client (application web) sera alors disponible sur http://localhost:3000.

Le client se rechargera automatiquement après des modifications dans le dossier `client/src/`, ce qui vous permettra d'y faire des modifications et de voir rapidement le résultat.

Pour toute autre modification, il faudra relancer Docker Compose : `make compose-down` puis `make compose-up`.

Pour arrêter le Docker Compose :

```
make compose-down
```

---

## Prérequis

Selon que vous vouliez contribuer au serveur ou au client, vous allez avoir besoin de :

### Pour le serveur

- Python 3.8+
- PostgreSQL 12

### Pour le client

- Une version récente de node (testé avec 16.3.0)
- Une version récente de npm (testé avec 8.1.3)

## Base de données

Il vous faut d'abord configurer une base de données PostgreSQL pour le développement.

Si vous avez un [serveur PostgreSQL](https://www.postgresql.org/download/linux/) sur votre machine hôte, lancez :

```bash
createdb catalogage
```

Sinon, vous pouvez utiliser la configuration `docker-compose` (voir [Raccourci : usage Docker](#raccourci--usage-docker)) :

```bash
docker-compose up -d -- db
```

[Configurez](#configuration) ensuite votre `APP_DATABASE_URL` :

```
cp .env.example .env
```

```bash
# .env
APP_DATABASE_URL="postgresql+asyncpg://user:pass@localhost:5432/${DB:-catalogage}"
```

## Interagir avec le projet

La façon principale d'interagir avec le projet est via des commandes `make`. Elles sont définies dans le `Makefile`.

Vous pouvez à tout moment en consulter l'aide grace à `make help`.

Pour la plupart des commandes, il y a une déclinaison pour le serveur et pour le client.
Par exemple : `make install` est l'équivalent de `make install-server install-client`.
Vous pouvez ainsi soit installer toutes les dépendances pour le serveur ainsi que pour le client,
soit spécifier explicitement ce qui vous intéresse.

Voici la suite de commandes à exécuter pour démarrer.

Installez les dépendances :

```
make install
```

Ensuite, exécutez les migrations de la base de données :

```
make migrate
```

Démarrez le serveur d'API (_backend_) sur http://localhost:3579 :

```
make serve-server
```

Démarrez le client (_frontend_) sur http://localhost:3000 :

```
make serve-client
```

Pour lancer les deux en parallèle dans le même shell :

```
make serve
```

Pour lancer l'ensemble des tests unitaires sur le client et le serveur, ainsi que les tests end-to-end (nécessite un `make serve` au préalable pour que les tests end-to-end fonctionnent) :

```
make test
```

Pour formatter le code automatiquement :

```
make format
```

Pour lancer les vérifications de qualité du code (_code linting_) :

```
make check
```

## Configuration

Le projet est configurable à l'aide des variables d'environnement suivantes.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_DATABASE_URL` | URL vers la base de données PostgreSQL | `postgresql+asyncpg://localhost:5432/catalogage` |

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet, que vous pouvez créer à partir du modèle `.env.example` :

```
cp .env .env.example
```

Les variables peuvent aussi être passées en arguments, elles sont alors utilisées en priorité par rapport au `.env`. Par exemple :

```bash
APP_DATABASE_URL="postgresql+asyncpg://..." make serve
```

Des paramètres avancés (principalement dédiés au déploiement - voir [Opérations](./ops.md)) sont également disponibles :

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_SERVER_MODE` | Un mode d'opération qui configure Uvicorn en conséquence : <br> - `local` : pour le développement local (_hot reload_ activé, etc) <br> - `live` : pour tout déploiement tel que défini via Ansible | `local` |
| `APP_PORT` | Port du server d'API | `3579` |
| `VITE_API_BROWSER_URL` | URL utilisée par le navigateur lors de requêtes d'API. En mode `live`, indiquer le chemin vers l'API configuré sur Nginx : `/api`. | `http://localhost:3579` |
| `VITE_API_SSR_URL` | URL utilisée par le serveur frontend lors de requêtes d'API | `http://localhost:3579` |
