set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter

if ["$TRAVIS_EVENT_TYPE" = "push"] && ["$TRAVIS_BRANCH" = "master"]; then
    coveralls;
fi;
