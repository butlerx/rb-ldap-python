SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYTHON := python3

.PHONY: install
install: requirements.txt setup.py ## Install rb-ldap locally
	$(PYTHON) -m pip install --user .

run: .dep_installed
	.venv/bin/python -m src --help

.venv/bin/activate:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	. .venv/bin/activate;

.dep_installed: requirements.txt .venv/bin/activate
	.venv/bin/python -m pip install -Ur requirements.txt
	@touch $^

test: .dep_installed  ## Run tests
	. .venv/bin/activate
	py.test -s \
		--cache-clear \
		--pep8 \
		--flakes \
		--cov=src \
		--cov-fail-under=80 \
		--no-cov-on-fail \
		--cov-report=term \
		--ignore="test/*" \
		.

.PHONY: clean
clean:  ##  Delete all environment files
	rm -rf .venv
	find -iname "*.pyc" -delete

.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
