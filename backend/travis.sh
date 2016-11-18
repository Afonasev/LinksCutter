set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter

if ["$TRAVIS_PULL_REQUEST" = "false"] && ["$TRAVIS_BRANCH" = "master"]; then
    coveralls;
fi;
