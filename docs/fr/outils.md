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

### Icônes supplémentaires

Le DSFR tire ses [icônes](https://gouvfr.atlassian.net/wiki/spaces/DB/pages/222331396/Ic+nes+-+Icons) de RemixIcon, mais seule une petite partie est incluse (pour des raisons de poids).

Des icônes supplémentaires utilisées dans ce projet sont fournies par un fichier CSS `client/src/styles/dsfr-icon-extras.css`. Celui-ci est généré par un script s'appuyant sur l'API de [Fontello](https://github.com/fontello/fontello) pour générer une fonte à partir des icônes supplémentaires.

Pour ajouter de nouvelles icônes supplémentaires :

- Récupérer le SVG (24px) sur https://remixicon.com/
- Ajouter le fichier SVG au dossier `client/src/assets/icon/dsfr-icon-extras/`
  - **Important** : Conformément à [Importing SVG images (Wiki Fontello)](https://github.com/fontello/fontello/wiki/How-to-use-custom-images#importing-svg-images), modifier le SVG pour retirer l'élément `<path fill="...">`. Il ne doit rester qu'un seul `<path d="...">` contenant le trait de l'icône. Exemple :
    ```xml
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24"><path d="M2 20h20v2H2v-2zm2-8h2v7H4v-7zm5 0h2v7H9v-7zm4 0h2v7h-2v-7zm5 0h2v7h-2v-7zM2 7l10-5 10 5v4H2V7zm2 1.236V9h16v-.764l-8-4-8 4zM12 8a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/></svg>
    ```
- Lancer `$ make dsfr-icon-extras` pour synchroniser le CSS.
- Utiliser les icônes comme d'habitude, mais avec `fr-fi-x-<icon>` (`x` pour "extra") au lieu de `fr-fi-<icon>`.
