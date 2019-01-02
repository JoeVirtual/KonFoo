docs:
	@cd docs; make html

test:
	@cd tests; pytest

build:
	python setup.py sdist bdist_wheel

release:
	python setup.py sdist bdist_wheel upload
