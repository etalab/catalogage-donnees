# Guide des contributions

Merci pour votre intéret pour ce projet ! Ce guide devrait vous mettre en selle pour contribuer le plus paisiblement possible.

## Prérequis

Vous allez avoir besoin de :

- Python 3.10
- PostgreSQL 12

## Démarrage rapide

### Base de données

Il vous faut d'abord configurer une base de données PostgreSQL pour le développement.

Si vous avez un [serveur PostgreSQL](https://www.postgresql.org/download/linux/) sur votre machine hôte, lancez :

```bash
createdb catalogage
```

Sinon, vous pouvez utiliser un [conteneur Docker](https://linuxiac.com/postgresql-docker/) :

```bash
docker pull postgres:12
docker volume create pg-data
docker run -d --name=postgres12 -p 5432:5432 -v pg-data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=[mdp] postgres:12
```

Assurez-vous de [configurer](#configuration) votre `APP_DATABASE_URL` en conséquence.

### Interagir avec le projet

La façon principale d'interagir avec le projet est via des commandes `make`. Elles sont définies dans le `Makefile`.

Vous pouvez à tout moment en consulter l'aide grace à `make help`.

Voici la suite de commandes à exécuter pour démarrer.

Installez les dépendances :

```
make install
```

Ensuite, exécutez les migrations de la base de données :

```
make migrate
```

Démarrez le serveur d'API (_backend_) :

```
make serve
```

Vérifiez sa bonne exécution avec un `$ curl localhost:3579`.

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

## Outils de développement

### mypy

Ce projet est équipé du _type checking_ avec [`mypy`](https://mypy.readthedocs.io).

La vérification se fait avec une exécution standard de `$ mypy` lors de `make check`.

### Migrations

Les migrations de la base de données sont gérées avec [`alembic`](https://alembic.sqlalchemy.org/en/latest/).

Pour appliquer les migrations en attente :

```bash
make migrate
```

Pour créer une nouvelle migration :

```bash
name=create-some-table make migration
```

Pour voir l'état actuel des migrations :

```bash
make currentmigration
```

### Configuration

Le serveur de développement est configurable à l'aide des variables d'environnement suivantes.

| Variable | Description | Valeur par défaut |
|---|---|---|
| `APP_DATABASE_URL` | URL vers la base de données PostgreSQL | `postgresql+asyncpg://localhost:5432/catalogage` |

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet.

Exemple :

```bash
# .env
APP_DATABASE_URL="postgresql+asyncpg://user:pass@localhost:6543/catalogage"
```

Les variables peuvent aussi être passées en arguments, par exemple :

```bash
APP_DATABASE_URL="..." make serve
```
