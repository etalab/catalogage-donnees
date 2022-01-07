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

Sinon, vous pouvez utiliser [Docker Compose](https://docs.docker.com/compose/install/) :

```bash
docker-compose up
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

Définissez les valeurs spécifiques à votre situation dans un fichier `.env` placé à la racine du projet, que vous pouvez créer à partir du modèle `.env.example`.

Les variables peuvent aussi être passées en arguments, elles sont alors utilisées en priorité par rapport au `.env`. Par exemple :

```bash
APP_DATABASE_URL="..." make serve
```

### Diagramme de la base de données

Le fichier `docs/db.erd.json` permet de générer un diagramme du schéma de la base de données.

Pour cela, installer d'abord [`graphviz`](https://graphviz.org/download/) (sous Linux : `$ sudo apt install graphviz`).

Puis lancer :

```
make dbdiagram
```

Ce qui génèrera `docs/db.png`.

Le format de `docs/db.erd.json` reprend celui de [`erdot`](https://github.com/ehne/ERDot), dont la documentation peut donc vous être utile.

## Trucs et astuces

### Base de données de branche

Si vous travaillez sur une branche qui inclut une modification de la base de données (exemple : ajout d'une table, altération d'une colonne...), il peut être pratique d'utiliser une base de données spécifique à cette branche ("BDD de branche"). Cela permet de garder la base `catalogage` en l'état si jamais vous deviez travailler à nouveau à partir de `master`.

Pour ce faire, créez d'abord une copie de votre base de données comme suit :

```bash
createdb -T catalogage catalogage-toto
```

> Si vous utilisez Docker Compose, vous devrez exécuter cette commande à l'intérieur du conteneur : `$ docker-compose exec postgresql createdb ...`.

Vous devez maintenant indiquer aux commandes `make` d'utiliser cette base `catalogage-toto`.

En principe, vous pourriez le faire en spécifiant une `APP_DATABASE_URL` en entier (voir [Configuration](#configuration)). Par exemple : `$ APP_DATABASE_URL=asyncpg://localhost:5432/catalogage-toto make serve`. Mais c'est peut-être un peu lourd.

Nous vous proposons donc mieux : si vous avez créé un `.env` à partir de `.env.example`, votre `APP_DATABASE_URL` acceptera par défaut une variable d'environnement `DB` permettant de ne passer que le nom de la base de données le serveur doit s'adresser.

Vous pouvez alors indiquer aux commandes `make` d'utiliser cette BDD de branche comme suit :

```bash
# Créer une migration à partir de la BDD de branche
DB=catalogage-toto name=add-some-table make migration

# Lancer les migrations sur la BDD de branche
DB=catalogage-toto make migrate

# Démarrer le serveur en utilisant la BDD de branche
DB=catalogage-toto make serve
```

Lorsque vous n'avez plus besoin de votre BDD de branche (par exemple quand celle-ci a été _mergée_), vous pouvez la supprimer :

```bash
dropdb catalogage-toto
```

En pratique, le processus est donc le suivant :

1. Créer une branche
2. Créer une BDD de branche à partir de votre BDD de développement principale.
3. Utiliser `DB=... make ...`.
4. Supprimer cette BDD de branche lorsque vous n'en avez plus besoin.
