help: # Magic trick to gather command comments into a handy help message.
	@grep -E '^[a-zA-Z_-]+:.*?#- .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?#- "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv = venv
bin = ${venv}/bin/
python = ${bin}python
pip = ${bin}pip
pysources = server/ tests/

install: #- Install dependencies
	python3 -m venv ${venv}
	${pip} install -U pip wheel setuptools
	${pip} install -r requirements.txt

serve: #- Run API server
	${bin}uvicorn server.main:app --port 3579 --reload

migrate: #- Apply pending migrations
	${bin}alembic upgrade head

migration: #- Create a migration
	${bin}alembic revision --autogenerate -m $(name)

currentmigration: #- Show current migraiton
	${bin}alembic show current

test: #- Run the test suite
	${bin}pytest

format: #- Run code formatting
	${bin}black ${pysources}
	${bin}isort ${pysources}

check: #- Run code checks
	${bin}black --check ${pysources}
	${bin}flake8 ${pysources}
	${bin}mypy ${pysources}
	${bin}isort --check --diff ${pysources}
