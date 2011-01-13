all: bootstrap buildout test coverage

bootstrap:
	python bootstrap.py

buildout:
	bin/buildout

test:
	bin/coverage run bin/django test masher

coverage:
	bin/coverage xml --source=src