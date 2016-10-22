set -e

cd ./backend
sh ./scripts/install.sh
sh ./scripts/test.sh
coveralls
