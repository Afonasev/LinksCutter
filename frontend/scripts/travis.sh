set -e

cd ./frontend
npm i
npm run build
npm run test
