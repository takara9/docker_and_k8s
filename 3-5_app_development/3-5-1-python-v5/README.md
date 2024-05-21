## イメージのビルドと実行

docker build -t ex1:1.4 .
docker run --name ex1 --rm --publish 9100:9100 --detach ex1:1.4


## アクセス

curl http://localhost:9100/ping;echo
curl http://localhost:9100/info;echo


## コンテナへ入る

docker exec -it ex1 bash


## イメージをレジストリへ登録

export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex1:1.4 ghcr.io/takara9/ex1:1.4
docker push ghcr.io/takara9/ex1:1.4


## クリーンナップ

docker stop ex1
docker rm ex1
docker rmi ghcr.io/takara9/ex1:1.4
docker rmi ex1:1.4



