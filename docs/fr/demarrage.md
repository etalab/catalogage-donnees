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

Pour lancer les tests :

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

Le serveur de développement est configurable à l'aide des variables d'environnement suivantes.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_DEBUG` | Lance le serveur en mode développement (_hot reload_, etc) | `False` |
| `APP_DATABASE_URL` | URL vers la base de données PostgreSQL | `postgresql+asyncpg://localhost:5432/catalogage` |

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet, que vous pouvez créer à partir du modèle `.env.example`.

Les variables peuvent aussi être passées en arguments, elles sont alors utilisées en priorité par rapport au `.env`. Par exemple :

```bash
APP_DATABASE_URL="..." make serve
```
