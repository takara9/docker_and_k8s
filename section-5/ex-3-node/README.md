## ローカルでの実行

npm init
npm install express
node app.js


## イメージのビルド

docker build -t ex3:1.0 .
docker run -d -p 9300:3000 --name ex3 ex3:1.0


## アクセス

curl http://localhost:9300/ping;echo


## コンテナへ入る

docker exec -it ex3 bash


## クリーンナップ

docker stop ex3
docker rm ex3
docker rmi ex3:1.0


