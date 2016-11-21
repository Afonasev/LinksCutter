set -e

cd ./backend
pip install -r requirements.txt
py.test --cov=./linkscutter
flake8
pylint linkscutter

push="push"

if [ "$TRAVIS_EVENT_TYPE" == "$push" ]; then
    coveralls
    apt-get install sshpass
    sshpass -e ssh root@138.68.65.124 -t supervisorctl restart linkscutter
fi
