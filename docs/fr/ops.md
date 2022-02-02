# Opérations

## Généralités

Le déploiement et la gestion des serveurs distants est gérée à l'aide de [Ansible](https://docs.ansible.com/ansible/latest/user_guide/index.html).

## Architecture

L'architecture du service déployé est la suivante :

```
        ┌---------------------------------┐
WWW ------- nginx (:80) ---- node (:3000) |
        |      |               |          |
        |      └-------- gunicorn (:3579) |
        └----------------------|----------┘
                               |
                         ┌ - - ┴ - - -┐
                           PostgreSQL 
                         └ - - - - - -┘
```

Autrement dit, un Nginx sert de frontale web et transmet les requêtes à un serveur applicatif Gunicorn qui communique avec la base de données (BDD) PosgreSQL (pour les requêtes d'API), ou à un serveur Node (pour les requêtes client).

Par ailleurs :

* Gunicorn et Node sont gérés par le _process manager_ `supervisor`, ce qui permet notamment d'assurer leur redémarrage en cas d'arrêt inopiné.
* Le lien entre Gunicorn et la base de données PostgreSQL est paramétrable (_database URL_). Cette dernier ne vit donc pas nécessairement sur la même machine que le serveur applicatif (voir [Environnements](#environnements)).

## Démarrage rapide

Avant toute chose, il y a quelques dépendances supplémentaires à installer pour interagir avec les outils d'infrastructure.

Lancez donc :

```
make install-ops
```

## Environnements

### staging

Cet environnement déploie la branche `master` sur une machine de _staging_ hébergée chez Scaleway.

**Spécifications attendues** :

- OS : debian/bullseye64
- Base de données : PostgreSQL 12, dont la _database URL_ est stockée dans `ops/ansible/secrets/staging.enc` (voir [Secrets](#secrets)).

**Démarrage rapide** :

- Procurez-vous le mot de passe de déploiement vers staging, puis placez-le dans le fichier suivant :

```
ops/ansible/secrets/staging.vault-password
```

- (Déploiement initial ou mises à jour système seulement) Lancez le _provisioning_ (installation de Python, Nginx, etc) avec :

```bash
make provision-staging
```

- Pour déployer, lancez alors :

```bash
make deploy-staging
```

- Pour déployer depuis une branche donnée, lancez :

```bash
EXTRA_OPTS="-e env_branch=mybranch" make deploy-staging
```

En cas de problème, se référer à [Débogage](#débogage).

### test

Cet environnement informel vous permet de tester la configuration Ansible sur une VM locale.

En pratique, vous pouvez par exemple utiliser [Vagrant](https://www.vagrantup.com/docs/installation) comme suit :

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

Accédez-y en SSH, en transmettant le port où se trouve votre base de données (BDD) de développement (ici 5435 sur l'hôte est transmis vers 5432 dans l'invité) ([crédit pour cette astuce](https://stackoverflow.com/a/28506841)) :

```bash
vagrant ssh -- -R 5432:localhost:5435
```

Sur l'hôte, ajoutez ensuite un fichier `ops/ansible/hosts_test` avec le contenu suivant (N.B. : modifiez `database_url` au besoin pour faire correspondre les identifiants et le nom de la BDD à votre BDD de développement) :

```ini
[web]
web1-test ansible_host=192.168.56.10 ansible_user=vagrant env_branch=master database_url=postgresql+asyncpg://user:pass@localhost:5432/catalogage
```

Vérifiez la bonne configuration avec un `ping` :

```bash
cd ops
make ping-test
```

```console
web1-test | SUCCESS => { ... }
```

Lancez le _provisioning_ :

```bash
cd ops
make provision-test
```

Vérifier la bonne exécution en inspectant dans la VM les différents outils et services attendus :

```console
$ pyenv --version
pyenv 2.2.3
$ python -V
Python 3.8.9
$ nvm --version
0.39.1
$ node -v
v16.13.2
$ systemctl status nginx
● nginx.service - A high performance web server and a reverse proxy serv>
     Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor >
     Active: active (running) since Wed 2022-01-26 10:48:11 UTC; 48s ago
...
$ systemctl status supervisor
● supervisor.service - Supervisor process control system for UNIX
     Loaded: loaded (/lib/systemd/system/supervisor.service; enabled; ve>
     Active: active (running) since Wed 2022-01-26 10:48:15 UTC; 59s ago
...
```

Et déployez :

```bash
cd ops
make deploy-test
```

Vérifiez le bon déploiement en accédant au site ou à l'API depuis la VM Vagrant :

```console
$ curl localhost
<!-- Du HTML ... -->
$ curl localhost/api/datasets/
[]
```

## Débogage

### Les migrations ont échoué

Pour l'instant, les déploiements ne sont pas _atomiques_. Si les migrations échouent, les fichiers de code auront déjà été mis à jour. Si un _reload_ de l'application survient (par Supervisor), le nouveau code sera pris en compte et il y a risque de plantage (désynchronisation entre le schéma de BDD attendu par le code et le schéma réel).

Il faut donc corriger les migrations, puis redéployer.

Une bonne pratique pour limiter les risques : déployer la migration d'abord, puis déployer le changement de code, avec éventuellement une migration de finalisation (ex : application de contraintes NULL), _c.f._ : https://gist.github.com/majackson/493c3d6d4476914ca9da63f84247407b

### Nginx renvoie une "502 Bad Gateway"

Il y a probablement soit un problème de configuration de la connexion entre Nginx et Node / Gunicorn (ex : mauvais port), soit le serveur Node / Gunicorn n'est pas _up_ (ex : il crashe ou ne démarre pas pour une raison à déterminer).

* Vérifier l'état de Nginx :

```
~/catalogage $ systemctl status nginx
```

* Vérifier l'état de Supervisor :

```
~/catalogage $ systemctl status supervisor
```

* Vérifier l'état du processus serveur (`server` pour Gunicorn, `client` pour le frontend Node) au sein de Supervisor :

```
~/catalogage $ sudo supervisorctl status server
```

* Inspecter la version du code, par exemple en inspectant le dépôt git :

```
~/catalogage $ git log
```

### Nginx pas mis à jour malgré un changement de configuration

Dans ce cas de figure, la configuration Nginx a été modifiée mais une fois le déploiement effectué, vous constatez qu'elle n'a pas pris effet. C'est peut-être que Nginx n'a pas réussi à charger la nouvelle configuration, car celle-ci contient des erreurs.

Sur le serveur, regardez les erreurs ou alertes de Nginx avec :

```
~/ $ sudo nginx -t
```

Exemple de résultat :

```
nginx: [warn] conflicting server name "web1-staging" on 0.0.0.0:80, ignored
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Rechercher ensuite d'où pourraient provenir les problèmes ainsi identifiés.

## Secrets

La gestion des secrets s'appuie sur Ansible Vault.

Voir aussi :

- [Encrypting content with Ansible Vault (Ansible docs)](https://docs.ansible.com/ansible/latest/user_guide/vault.html)
- [Handling secrets in your Ansible playbooks (RedHat)](https://www.redhat.com/sysadmin/ansible-playbooks-secrets)

Pour modifier un fichier de secrets d'un environnement donné, lancez par exemple :

```bash
cd ops && make secrets-edit-staging
```

N.B. : cette commande demandera le mot de passe Vault associé à l'environnement.

## Autres

### Version de Python

On utilise [pyenv](https://github.com/pyenv/pyenv) pour installer Python sur les serveurs distants.

La configuration est aussi gérée par Ansible (rôle `pyenv`), notamment au moyen de la variable `pyenv_python_version`. En la modifiant, on peut ainsi mettre Python à jour. Il sera bien sûr préférable de s'assurer de retirer toute ancienne version de Python après une telle opération.

### Version de Node

De la même façon, on utilise [nvm](https://github.com/nvm-sh/nvm) pour installer Node.

La version est paramétrée par la variable `nvm_node_version`.
