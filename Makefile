all: bootstrap buildout test

bootstrap:
	python bootstrap.py

buildout:
	bin/buildout

test:
	bin/django test masher

coverage:
	bin/coverage xml --source=src

pylint:
	bin/pylint