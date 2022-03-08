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

## Données initiales

Le script `tools/initdata.py` permet de définir des données initiales à charger en base.

Il peut être lancé comme suit :

```
make initdata
```

Des entités seront ainsi chargées en base de données.

Si celles-ci ont changé (suite à des manipulations manuelles dans le frontend, par exemple) et que vous souhaitez les remettre dans leur état initial, lancer :

```
make initdatareset
```

Les données à charger sont définies dans le fichier YAML `tools/initdata.yml`. Sa structure est ad-hoc. Elle est fortement corrélée au traitement réalisé par le script.

```yaml
users:
  - id: "<UUID>"
    params:
      email: "<email>"
      password: "<password>"
  - # ...
  
datasets:
  - id: "<UUID>"
    params:
      title: "<title>"
      description: "<description>"
      formats:
        - "<format>"
  - # ...
```

Avant de créer chaque entité, le script s'assure qu'elle n'existe pas déjà en base.

(Lire le code source pour les détails.)

## Générer un ID

Pour générer un ID d'entité, lancer :

```
make id
```

Exemple de sortie :

```
9355b423-4417-4153-8fd6-524697f8c88f
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

## Tests

### Tests E2E

Les tests _end-to-end_ sont lancés avec [`Playwright`](https://playwright.dev/).
Il sont soit exécutés en mode _ci_ (continuous integration, par exemple dans
notre cas avec github actions), et donc en _headless_, soit de manière
interactive (en dev).

### Tests unitaires - Client

Les tests unitaires côté client utilisent [`svelte-testing-library`](https://github.com/testing-library/svelte-testing-library).

Autres ressources pour démarrer :

- [Svelte Testing Library: Example](https://testing-library.com/docs/svelte-testing-library/example)
- [Unit Testing Svelte Components](https://sveltesociety.dev/recipes/testing-and-debugging/unit-testing-svelte-component/)

## DSFR

Le site utilise le [Design System de
l'État](https://gouvfr.atlassian.net/wiki/spaces/DB/overview) (aussi appelé
*DSFR*).

Il existe aussi le site très pratique de [Démo du design système
de l'état](https://template.incubateur.net/) pour la mise en œuvre et
l'utilisation de ce DSFR.
