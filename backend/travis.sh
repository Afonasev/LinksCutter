set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter

echo $TRAVIS_EVENT_TYPE
if ["$TRAVIS_EVENT_TYPE" = "push"]; then
    coveralls
fi
