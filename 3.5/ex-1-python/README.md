## イメージのビルドと実行

docker build -t ex1:1.0 .
docker run --name ex1 --publish 9100:9100 --detach ex1:1.0


## アクセス

curl http://localhost:9100/ping;echo


## コンテナへ入る

docker exec -it ex1 bash


## クリーンナップ

docker stop ex1
docker rm ex1
docker rmi ex1:1.0
