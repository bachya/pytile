clean:
	pipenv --rm
coverage:
	pipenv run py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pytile tests
init:
	pip3 install --upgrade pip pipenv
	pipenv lock
	pipenv install --three --dev
lint:
	pipenv run flake8 pytile
	pipenv run pydocstyle pytile
	pipenv run pylint pytile
publish:
	pipenv run python setup.py sdist bdist_wheel
	pipenv run twine upload dist/*
	rm -rf dist/ build/ .egg pytile.egg-info/
test:
	pipenv run py.test
typing:
	pipenv run mypy --ignore-missing-imports pytile
