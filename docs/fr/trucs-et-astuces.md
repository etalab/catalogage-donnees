# Trucs et astuces

## Base de données de branche

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
