ACTIVATE_VENV = pipenv run
PLATFORM := $(shell uname -s)

.PHONY:
	black-format \
	black-format-check \
	bootstrap \
	cheeseshop \
	flake8 \
	install-precommit \
	isort \
	isort-check \
	nuke-venv \
	run-tests \

black-format:
	@$(ACTIVATE_VENV) black .

black-format-check:
	@$(ACTIVATE_VENV) black . --check -q

bootstrap: nuke-venv cheeseshop install-precommit

cheeseshop:
	@if [ $(PLATFORM) = 'Darwin' ]; then\
		export CFLAGS='-Wno-implicit-function-declaration' && export LANG='en_US.UTF-8' && pipenv install --dev;\
	else\
		pipenv install --dev;\
	fi

flake8:
	@$(ACTIVATE_VENV) flake8 .

install-precommit:
	@$(ACTIVATE_VENV) pre-commit install

isort:
	@$(ACTIVATE_VENV) isort . --tc

isort-check:
	@$(ACTIVATE_VENV) isort . --check-only --tc -q

nuke-venv:
	@pipenv --rm;\
	EXIT_CODE=$$?;\
	if [ $$EXIT_CODE -eq 1 ]; then\
		echo Skipping virtualenv removal;\
	fi

run-tests:
	@$(ACTIVATE_VENV) coverage run -m pytest -s $(EXTRA_ARGS)
	@$(ACTIVATE_VENV) coverage report
