PKG=validator

.PHONY: all clean version init flake8 pylint lint test coverage

init: clean
	@echo Install Environment
	pipenv --python 3.7
	pipenv install

dev: init
	@echo Install Develop Environment
	pipenv install --dev

run:
	@echo Run Project
	pipenv run python3 -m ${PKG}.app

lint: flake8 pylint mypy

flake8:
	@echo [Linter] Style Check
	pipenv run flake8

pylint:
	@echo [Linter] Style Check
	pipenv run pylint $(PKG) --rcfile=setup.cfg

mypy:
	@echo [Linter] Type Check
	pipenv run mypy $(PKG)/

reformat: isort black

isort:
	@echo [Reformat] Sort Imports
	pipenv run isort .

black:
	@echo [Reformat] Code Format
	pipenv run black $(PKG) --skip-string-normalization -l 120

analysis: bandit ochrona

bandit:
	@echo [Analysis] Statuc Analysis
	pipenv run bandit -r ${PKG}/

ochrona:
	@echo [Analysis] Software Composition Analysis
	pipenv run ochrona

test:
	pipenv run pytest -vv --cov-report=term-missing --cov=${PKG} tests/

ci-bundle: reformat lint analysis test

clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -type d -name '*.egg-info' -delete
	find . -type f -name '*.egg' -delete

clean-pyc:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.pyo' -delete
	find . -type f -name '*~' -delete
	find . -type d -name '__pycache__' -delete
