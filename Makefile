init:
	pip3 install -r requirements.txt
devel:
	pip3 install -r requirements_dev.txt
test:
	tox
lint:
	pylint pyetrade tests
install:
	pip3 install .
dist:
	python3 setup.py sdist
clean:
	find . -iname *.pyc -exec rm -f {} +
	pip3 uninstall -y pyetrade
