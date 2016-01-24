test:
	@cd tests; py.test

release:
	python setup.py sdist bdist_wheel upload
