clean:
	.venv/bin/pre-commit uninstall
	rm -rf .venv/
coverage:
	.venv/bin/py.test -s --verbose --cov-report term-missing --cov-report xml --cov=pytile tests
init:
	python3 -m venv .venv
	.venv/bin/pip3 install poetry
	.venv/bin/poetry lock
	.venv/bin/poetry install
	.venv/bin/pre-commit install
