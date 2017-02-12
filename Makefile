init:
	pip install -r requirements.txt
test:
	python -m unittest -v tests
lint:
	pylint pyetrade
install:
	pip install .
clean:
	find . -iname *.pyc -exec rm -f {} +
	pip uninstall -y pyetrade
