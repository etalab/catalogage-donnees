venv = ../venv
bin = ${venv}/bin/

staging-opts = -e @ansible/secrets/staging.enc --vault-password-file ansible/secrets/staging.vault-password

ansible = ${bin}ansible
ansible-vault = ${bin}ansible-vault
ansible-staging = ${ansible} -i ansible/hosts_staging ${staging-opts}
ansible-playbook = ${bin}ansible-playbook
ansible-playbook-test = ${ansible-playbook} -i ansible/hosts_test
ansible-playbook-staging = ${ansible-playbook} -i ansible/hosts_staging ${staging-opts}

export ANSIBLE_CONFIG = ansible/ansible.cfg

install:
	${bin}pip install -U pip wheel
	${bin}pip install ansible
	${ansible} --version

run-staging:
	${ansible-staging} web -m "$(m)" -a "$(a)"

ping-test:
	${ansible} -i ansible/hosts_test web -m ping

ping-staging:
	make run-staging m=ping

secrets-edit-staging:
	${ansible-vault} edit ansible/secrets/staging.enc --vault-password-file ansible/secrets/staging.vault-password

provision-test:
	${ansible-playbook-test} -t provision ansible/playbook.yml $(EXTRA_OPTS)

provision-staging:
	${ansible-playbook-staging} -t provision ansible/playbook.yml $(EXTRA_OPTS)

deploy-test:
	${ansible-playbook-test} -t deploy ansible/playbook.yml $(EXTRA_OPTS)

deploy-staging:
	${ansible-playbook-staging} -t deploy ansible/playbook.yml $(EXTRA_OPTS)
