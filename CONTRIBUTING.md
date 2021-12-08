# Guide des contributions

Merci pour votre intéret pour ce projet ! Ce guide devrait vous mettre en selle pour contribuer le plus paisiblement possible.

## Démarrage rapide

**Prérequis** - Vous allez avoir besoin de :

- Python 3.8+

La façon principale d'interagir avec le projet est via des commandes `make`. Elles sont définies dans le `Makefile`.

Vous pouvez à tout moment en consulter l'aide grace à `make help`.

Voici un aperçu...

Pour installer les dépendances :

```
make install
```

Pour démarrer le serveur d'API (_backend_) :

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
