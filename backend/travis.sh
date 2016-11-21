set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter

echo $TRAVIS_EVENT_TYPE
if ["$TRAVIS_EVENT_TYPE" != "pull_request"]; then
    coveralls
    apt-get install sshpass
    sshpass -e ssh root@138.68.65.124 -t supervisorctl restart linkscutter
fi

echo "$TRAVIS_EVENT_TYPE";
