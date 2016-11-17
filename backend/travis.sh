set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter
coveralls
