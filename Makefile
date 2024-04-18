init:
	pip install -r requirements.txt
devel:
	pip install -r requirements_dev.txt
	pre-commit install --hook-type pre-commit --hook-type pre-push --install-hooks -t post-checkout -t post-merge
	curl -sSL https://install.python-poetry.org | python3 -
	pip install poetry-plugin-export
test:
	tox
analysis: # Lint, format, import optimizer, etc.
	poetry run pre-commit run --all-files
install:
	pip install --upgrade .
dist:
	python setup.py sdist
clean:
	$(RM) -fr .tox/
	find . -iname *.pyc -exec rm -f {} +
	pip uninstall -y pyetrade
