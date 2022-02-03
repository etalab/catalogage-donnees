# Outils de développement

## Migrations

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

## Diagramme de la base de données

Le fichier `docs/db.erd.json` permet de générer un diagramme du schéma de la base de données.

Pour cela, installer d'abord [`graphviz`](https://graphviz.org/download/) (sous Linux : `$ sudo apt install graphviz`).

Puis lancer :

```
make dbdiagram
```

Ce qui génèrera `docs/db.png`.

Le format de `docs/db.erd.json` reprend celui de [`erdot`](https://github.com/ehne/ERDot), dont la documentation peut donc vous être utile.

## mypy

Ce projet est équipé du _type checking_ avec [`mypy`](https://mypy.readthedocs.io).

La vérification se fait avec une exécution standard de `$ mypy` lors de `make check`.

## Cypress

Les tests _end-to-end_ sont lancés avec [`cypress`](https://www.cypress.io/).
Il sont soit exécutés en mode _ci_ (continuous integration, par exemple dans
notre cas avec github actions), et donc en _headless_, soit de manière
interactive (en dev).

En mode interactif avec `cd client && npm run test-e2e:watch`, une fenêtre
cypress s'ouvre qui permet de lancer les tests dans différents navigateurs, et
de pouvoir remonter dans le déroulé de chaque test.
