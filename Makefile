all: bootstrap buildout test coverage pylint

bootstrap:
	python bootstrap.py

buildout:
	bin/buildout

test:
	bin/coverage run bin/django test masher

coverage:
	bin/coverage xml --source=src

pylint:
	bin/pylint > pylint.txt