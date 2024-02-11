
##

~~~
$ ls
Dockerfile      README.md       app.js
~~~

~~~
3-5-3-node$ ls
Dockerfile      README.md       app.js
~~~

## ローカルでの実行

~~~
npm init
npm install express
node app.js
~~~

## イメージのビルド

~~~
docker build -t ex3:1.0 .
docker run -d -p 9300:3000 --name ex3 ex3:1.0
~~~

## アクセス

~~~
curl http://localhost:9300/ping;echo
~~~

## コンテナへ入る

~~~
docker exec -it ex3 bash
~~~


## イメージをレジストリへ登録

~~~
export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID 
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex3:1.0 ghcr.io/takara9/ex3:1.0
docker push ghcr.io/takara9/ex3:1.0
~~~


## クリーンナップ

~~~
docker stop ex3
docker rm ex3
docker rmi ex3:1.0
docker rmi ghcr.io/takara9/ex3:1.0
~~~
