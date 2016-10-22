set -e

py.test --cov=./linkscutter
flake8
pylint linkscutter
