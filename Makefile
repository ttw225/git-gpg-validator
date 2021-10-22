PKG=validator

.PHONY: all clean version init flake8 pylint lint test coverage

init: clean
	pipenv --python 3.7
	pipenv install

dev: init
	pipenv install --dev

flake8:
	pipenv run flake8

pylint:
	pipenv run pylint $(PKG) --rcfile=setup.cfg

mypy:
	pipenv run mypy $(PKG)/

lint: flake8 pylint

black:
	pipenv run black $(PKG) --skip-string-normalization -l 120

isort:
	pipenv run isort .

reformat: isort black

run:
	pipenv run python3 ${PKG}/app.py

ci-bundle: reformat lint

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
