RUN_IN_ENV = pipenv run
PYTHON = $(RUN_IN_ENV) python

test:
	pytest --pep8

check_git_dirty:
	git status --porcelain
	test -z "$$(git status --porcelain)"

deploy: check_git_dirty test build
	$(RUN_IN_ENV) twine upload dist/*

deploy-test: check_git_dirty test build
	$(RUN_IN_ENV) twine --repository testpypi upload dist/*

dist: clean
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist_wheel

build:
	pipenv lock
	$(MAKE) dist

clean:
	rm -rf dist

.PHONY: test acceptance unit clean update pipenv compile build publish doc
