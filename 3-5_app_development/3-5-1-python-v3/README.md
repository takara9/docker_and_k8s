## イメージのビルドと実行

docker build -t ex1:1.3 .
docker run --name ex1 --publish 9103:9100 --detach ex1:1.3


## アクセス

curl http://localhost:9102/ping;echo


## コンテナへ入る

docker exec -it ex1 bash


## イメージをレジストリへ登録

export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex1:1.1 ghcr.io/takara9/ex1:1.1
docker push ghcr.io/takara9/ex1:1.1


## クリーンナップ

docker stop ex1
docker rm ex1
docker rmi ghcr.io/takara9/ex1:1.1
docker rmi ex1:1.1



