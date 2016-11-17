set -e

cd ./frontend
curl -sL https://deb.nodesource.com/setup_7.x | sudo -E bash -
sudo apt-get install -y nodejs
npm i
npm run build
npm run test
npm run lint
