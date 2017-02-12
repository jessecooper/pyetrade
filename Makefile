init:
	pip3 install -r requirements.txt
devel:
	pip3 install -r requirements_dev.txt
test:
	python -m unittest -v tests
lint:
	pylint pyetrade
install:
	pip install .
clean:
	find . -iname *.pyc -exec rm -f {} +
	pip uninstall -y pyetrade
