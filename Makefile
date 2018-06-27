.PHONY: init test clean-pyc lint

clean-pyc:
	find . -name '*.pyc' || rm --force {} +
	find . -name '*.pyo' || rm --force {} +
	find . -name '*.p~' || rm --force {} +

init:
	conda env create --file environment.yml --force

test: clean-pyc
	nosetests src

lint:
	pylint src --disable=too-few-public-methods,too-many-instance-attributes


help:
	@echo "clean-pyc"
	@echo "    Remove python artifacts"
	@echo "test"
	@echo "    Run all python tests"
	@echo "lint"
	@echo "    Check style with pylint"