
## ディレクトリ構造

```
$ tree
.
├── Dockerfile
├── Dockerfile.maven
├── README.md
├── mvnw
├── mvnw.cmd
├── pom.xml
└── src
    ├── main
    │   └── java
    │       └── com
    │           └── example
    │               └── restservice
    │                   ├── Greeting.java
    │                   ├── GreetingController.java
    │                   └── RestServiceApplication.java
    └── test
        └── java
            └── com
                └── example
                    └── restservice
                        └── GreetingControllerTests.java
```
MacOS M2で動かないかもしれない。JavaだからIntel/AMD64だけでOKかもしれない。


## 1 パソコン上での動かし方

./mvnw install
java -jar target/rest-service-0.0.1.jar

停止はコントロールとcを同時におします。

クリーンアップ

./mvnw clean



## 2 パソコン上でjarを作成して、コンテナ化する方法

./mvnw install
docker build -t ex5:1.0 .
docker run -d --name ex5 -p 9500:8080 ex5:1.0



## 3 コンテナ上でjarをビルドしてコンテナで実行

docker build -t ex5:1.0 -f Dockerfile.maven .
docker run -d --name ex5 -p 9500:8080 ex5:1.0



## アクセス

curl http://localhost:9500/ping;echo


## コンテナへ入る

docker exec -it ex5 bash


## イメージをレジストリへ登録

export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID 
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex5:1.0 ghcr.io/takara9/ex5:1.0
docker push ghcr.io/takara9/ex5:1.0

## クリーンナップ

docker stop ex5
docker rm ex5
docker rmi ex5:1.0
./mvnw clean
