# Opérations

**Table des matières**

- [Généralités](#généralités)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Tests](#tests)
- [Débogage](#débogage)
- [Versions](#versions)

## Généralités

Le déploiement et la gestion des serveurs distants est réalisée à l'aide de [Ansible](https://docs.ansible.com/ansible/latest/user_guide/index.html).

Les différents déploiements sont organisés en _environnements_ (copies de l'infrastructure) :

| Nom | Description |
|---|---|
| demo | Environnement de démo |
| staging | Environnement de staging |

Il y a un seul _groupe_ Ansible : `web`.

## Architecture

L'architecture du service déployé est la suivante :

```
        ┌---------------------------------┐
WWW ------- nginx (:443) --- node (:3000) |
        |      |               |          |
        |      └--------- uvicorn (:3579) |
        └----------------------|----------┘
                               |
                         ┌ - - ┴ - - -┐
                           PostgreSQL 
                         └ - - - - - -┘
```

Description : un Nginx sert de frontale web, et transmet les requêtes à un serveur applicatif Uvicorn qui communique avec la base de données PostgreSQL (pour les requêtes d'API), ou à un serveur Node (pour les requêtes client).

Par ailleurs :

* Uvicorn et Node sont gérés par le _process manager_ `supervisor`, ce qui permet notamment d'assurer leur redémarrage en cas d'arrêt inopiné.
* Le lien entre Uvicorn et la base de données PostgreSQL est paramétrable (_database URL_). Cette dernier ne vit donc pas nécessairement sur la même machine que le serveur applicatif.
* Nginx fait la terminaison TLS avec des certificats gérés avec [Certbot](https://eff-certbot.readthedocs.io) (LetsEncrypt).

## Installation

Installez les dépendances supplémentaires pour interagir avec les outils d'infrastructure :

```
make install-ops
```

Munissez-vous également du mot de passe de déploiement, puis placez-le dans :

```
ops/ansible/vault-password
```

## Usage

### Déployer

Pour déployer l'environnement `<ENV>`, lancez :

```
make deploy env=<ENV>
```

Exemple :

```
make deploy env=staging
```

En cas de problème, voir [Débogage](#débogage).

### Ajouter un nouvel environnement

Créez le dossier de l'environnement dans `ops/ansible/environments/`, sur le modèle de ceux qui existent déjà.

Les fichiers suivants sont attendus :

- `hosts` : _inventory_ Ansible.
- `secrets` : fichier de variables secrètes - voir [Secrets](#secrets) pour comment le modifier.
- `group_vars/web.yml` : variables spécifiques à l'environnement.

Quand tout semble prêt, initialisez l'environnement `<ENV>` :

```
make provision env=<ENV>
```

Vous pouvez ensuite [déployer](#déployer).

### Secrets

La gestion des secrets s'appuie sur [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html).

Pour modifier le fichier de secrets d'un environnement, lancez :

```
cd ops && make secrets env=<ENV>
```

## Tests

Il est possible de tester la configuration Ansible sur une VM locale.

Vous pouvez par exemple configurer une box [Vagrant](https://www.vagrantup.com/docs/installation) comme suit :

```ruby
# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Configure VM
  config.vm.box = "debian/bullseye64"
  config.vm.network "private_network", ip: "192.168.56.10"
  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
    v.cpus = 1
  end

  # Share host SSH public key with VM, so Ansible can execute commands over SSH.
  config.ssh.insert_key = false
  config.vm.provision "shell" do |s|
    ssh_pub_key = File.readlines("#{Dir.home}/.ssh/id_rsa.pub").first.strip
    s.inline = <<-SHELL
    echo #{ssh_pub_key} >> /home/vagrant/.ssh/authorized_keys
    echo #{ssh_pub_key} >> /root/.ssh/authorized_keys
    SHELL
  end
end
```

Démarrez la VM :

```bash
vagrant up
```

Accédez-y en SSH, en transmettant le port où se trouve votre base de données (BDD) de développement (ici 5432 sur l'hôte est transmis vers 5432 dans l'invité) ainsi que le port du serveur Nginx (ici 80 dans l'invité est transmis sur 3080 sur l'hôte) ([crédit pour cette astuce](https://stackoverflow.com/a/28506841)) :

```bash
vagrant ssh -- -R 5432:localhost:5432 -L 3080:localhost:80
```

Sur l'hôte, [ajoutez un environnement](#ajouter-un-nouvel-environnement) nommé `test` :

- `hosts` :

    ```
    [web]
    web-test ansible_host=192.168.56.10 ansible_user=vagrant
    ```

- `secrets` :
    ```yaml
    {}  # Rien de secret
    ```

- `group_vars/web.yml` :

    _(Modifiez `database_url` au besoin)_

    ```yaml
    git_version: master
    database_url: database_url: postgresql+asyncpg://user:pass@localhost:5432/catalogage
    ```

Vérifiez la bonne configuration avec un `ping` :

```
cd ops
make ping env=test
```

```
web-test | SUCCESS => { ... }
```

Lancez le _provisioning_ :

```
make provision env=test
```

Vérifier la bonne exécution en inspectant dans la VM les différents outils et services attendus :

```console
$ pyenv --version
pyenv 2.2.3
```

```console
$ python -V
Python 3.8.9
```

```console
$ nvm --version
0.39.1
```

```console
$ node -v
v16.13.2
```

```console
$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy serv>
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor >
     Active: active (running) since Wed 2022-01-26 10:48:11 UTC; 48s ago
...
```

```console
$ systemctl status supervisor
● supervisor.service - Supervisor process control system for UNIX
     Loaded: loaded (/lib/systemd/system/supervisor.service; enabled; ve>
     Active: active (running) since Wed 2022-01-26 10:48:15 UTC; 59s ago
...
```

Puis déployez :

```
make deploy env=test
```

Vérifiez le bon déploiement en accédant au site sur http://localhost:3080.

## Débogage

### Les migrations ont échoué

Pour l'instant, les déploiements ne sont pas _atomiques_. Si les migrations échouent, les fichiers de code auront déjà été mis à jour. Si un _reload_ de l'application survient (par Supervisor), le nouveau code sera pris en compte et il y a risque de plantage (désynchronisation entre le schéma de BDD attendu par le code et le schéma réel).

Il faut donc corriger les migrations, puis redéployer.

Une bonne pratique pour limiter les risques : déployer la migration d'abord, puis déployer le changement de code, avec éventuellement une migration de finalisation (ex : application de contraintes NULL), _c.f._ : https://gist.github.com/majackson/493c3d6d4476914ca9da63f84247407b

### Nginx renvoie une "502 Bad Gateway"

Il y a probablement soit un problème de configuration de la connexion entre Nginx et Node / Uvicorn (ex : mauvais port), soit le serveur Node / Uvicorn n'est pas _up_ (ex : il crashe ou ne démarre pas pour une raison à déterminer).

* Vérifier l'état de Nginx :

```
~/catalogage $ systemctl status nginx
```

* Vérifier l'état de Supervisor :

```
~/catalogage $ systemctl status supervisor
```

* Vérifier l'état du processus serveur (`server` pour Uvicorn, `client` pour le frontend Node) au sein de Supervisor :

```
~/catalogage $ sudo supervisorctl status server
```

* Inspecter la version du code, par exemple en inspectant le dépôt git :

```
~/catalogage $ git log
```

## Versions

## OS

**Version** : debian/bullseye64

## PostgreSQL

**Version** : PostgreSQL 12

### Python

**Version** : Python 3.8.x

On utilise [pyenv](https://github.com/pyenv/pyenv) pour installer Python sur les serveurs distants.

La configuration est aussi gérée par Ansible (rôle `pyenv`), notamment au moyen de la variable `pyenv_python_version`. En la modifiant, on peut ainsi mettre Python à jour. Il sera bien sûr préférable de s'assurer de retirer toute ancienne version de Python après une telle opération.

### Node

**Version** : Node v16.x

De la même façon, on utilise [nvm](https://github.com/nvm-sh/nvm) pour installer Node.

La version est paramétrée par la variable `nvm_node_version`.
