SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.DELETE_ON_ERROR:
.DEFAULT_GOAL := help
MAKEFLAGS += --warn-undefined-variables
MAKEFLAGS += --no-builtin-rules

PYTHON := python3
WHEEL := dist/rbldap-*.whl

build: $(WHEEL)  ## Build Wheel
$(WHEEL): pyproject.toml
	flit build

.PHONY: install
install: pyproject.toml .venv/bin/activate ## Install Dependencies for testing
	flit install --python .venv/bin/python

.venv/bin/activate:
	$(PYTHON) -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	. .venv/bin/activate;

test: install  ## Run tests
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
	rm -rf .venv dist build __pycache__ **/*.egg-info/ **/__pycache__
	find . -name '*.py[c|o]' -delete

.PHONY: help
help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| sort \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-10s\033[0m %s\n", $$1, $$2}'
