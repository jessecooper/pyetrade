init:
	pip install -r requirements.txt
devel:
	pip install -r requirements_dev.txt
	pre-commit install
test:
	tox
lint:
	pylint pyetrade tests
install:
	pip install --upgrade .
dist:
	python setup.py sdist
clean:
	find . -iname *.pyc -exec rm -f {} +
	pip uninstall -y pyetrade
