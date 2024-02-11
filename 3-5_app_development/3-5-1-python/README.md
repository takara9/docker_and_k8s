
## イメージのビルド

~~~
$ ls
Dockerfile      README.md       app.py

$ docker build -t ex1:1.0 .
~~~

## イメージの実行


~~~
docker run --name ex1 --publish 9100:9100 --detach ex1:1.0
~~~

## アクセス

~~~
curl http://localhost:9100/ping;echo
~~~

## コンテナへ入る

~~~
docker exec -it ex1 bash
~~~

## イメージをレジストリへ登録

~~~
export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID 
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex1:1.0 ghcr.io/takara9/ex1:1.0
docker push ghcr.io/takara9/ex1:1.0
~~~

## クリーンナップ

~~~
docker stop ex1
docker rm ex1
docker rmi ghcr.io/takara9/ex1:1.0
docker rmi ex1:1.0
~~~


