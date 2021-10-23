PKG=validator

.PHONY: all clean version init flake8 pylint lint test coverage

init: clean
	pipenv --python 3.7
	pipenv install

dev: init
	pipenv install --dev

run:
	pipenv run python3 ${PKG}/app.py

lint: flake8 pylint mypy

flake8:
	pipenv run flake8

pylint:
	pipenv run pylint $(PKG) --rcfile=setup.cfg

mypy:
	pipenv run mypy $(PKG)/

reformat: isort black

isort:
	pipenv run isort .

black:
	pipenv run black $(PKG) --skip-string-normalization -l 120

analysis: bandit

bandit:
	pipenv run bandit -r ${PKG}/

ci-bundle: reformat lint analysis

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
