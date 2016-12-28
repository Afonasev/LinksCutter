# LinksCutter - Backend
[![Coverage Status](https://coveralls.io/repos/github/Afonasev/LinksCutter/badge.svg?branch=master)](https://coveralls.io/github/Afonasev/LinksCutter?branch=master)

### Installing deps

    pip install -r requirements.txt

### Migrations applying
    python -m migrator apply

### Running debug server

    python wsgi.py

### Running the testsuite

    py.test --cov=./linkscutter

### Code linting

    flake8
    pylint linkscutter

### Code Style

* [PEP8](https://www.python.org/dev/peps/pep-0008/)
