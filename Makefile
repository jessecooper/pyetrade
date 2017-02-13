init:
	pip3 install -r requirements.txt
devel:
	pip3 install -r requirements_dev.txt
test:
	#python3 -m unittest -v
	coverage run --source pyetrade -m unittest -v
	coverage report -m
lint:
	pylint pyetrade
install:
	pip3 install .
clean:
	find . -iname *.pyc -exec rm -f {} +
	pip3 uninstall -y pyetrade
