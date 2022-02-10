# Démarrage rapide

Cette page indique les quelques étapes qui vous permettront d'avoir un projet fonctionnel à partir duquel travailler.

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

Sinon, vous pouvez utiliser [Docker Compose](https://docs.docker.com/compose/install/) :

```bash
docker-compose up
```

Assurez-vous de [configurer](#configuration) votre `APP_DATABASE_URL` en conséquence.

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

Le serveur d'API est configurable à l'aide des variables d'environnement suivantes.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_SERVER_MODE` | Un mode d'opération qui configure Uvicorn en conséquence : <br> - `local` : pour le développement local (_hot reload_ activé, etc) <br> - `live` : pour tout déploiement tel que défini via Ansible (voir [Opérations](./ops.md)) | `local` |
| `APP_DATABASE_URL` | URL vers la base de données PostgreSQL | `postgresql+asyncpg://localhost:5432/catalogage` |
| `APP_PORT` | Port du server d'API | `3579` |
| `VITE_API_PORT` | Doit être égal à `APP_PORT` si jamais ce dernier diffère de sa valeur par défaut, afin de permettre la communication directe entre le frontend et le serveur d'API le cas échéant (SSR, proxy local...). Pour plus de contexte, voir [#48](https://github.com/etalab/catalogage-donnees/pull/48) | `3579` |

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet, que vous pouvez créer à partir du modèle `.env.example`.

Les variables peuvent aussi être passées en arguments, elles sont alors utilisées en priorité par rapport au `.env`. Par exemple :

```bash
APP_DATABASE_URL="..." make serve
```

## Tests

### Tests unitaires - Client

Les tests unitaires côté client utilisent [`svelte-testing-library`](https://github.com/testing-library/svelte-testing-library).

Autres ressources pour démarrer :

- [Svelte Testing Library: Example](https://testing-library.com/docs/svelte-testing-library/example)
- [Unit Testing Svelte Components](https://sveltesociety.dev/recipes/testing-and-debugging/unit-testing-svelte-component/)
