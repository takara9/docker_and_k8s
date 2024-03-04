
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

docker build -t ex5:1.1 -f Dockerfile.maven .
docker run -d --name ex5-maven -p 9510:8080 ex5:1.1



## アクセス

curl http://localhost:9500/ping;echo
curl http://localhost:9510/ping;echo


## コンテナへ入る

docker exec -it ex5 bash


## サイズの比較と脆弱性

~~~
3-5-5-java$ docker images
REPOSITORY                        TAG       IMAGE ID       CREATED              SIZE
ex5                               1.1       b79788ea23da   18 seconds ago       450MB
ex5                               1.0       24f504d912b2   About a minute ago   450MB

:3-5-5-java$ docker scout quickview ex5:1.0
    i New version 1.4.1 available (installed version is 1.2.0) at https://github.com/docker/scout-cli
    ✓ Image stored for indexing
    ✓ Indexed 215 packages

  Target     │  ex5:1.0             │    0C     2H     5M    21L   
    digest   │  24f504d912b2        │                              
  Base image │  eclipse-temurin:21  │    0C     0H     5M    21L   

What's Next?
  View vulnerabilities → docker scout cves ex5:1.0
  Include policy results in your quickview by supplying an organization → docker scout quickview ex5:1.0 --org <organization>

3-5-5-java$ docker scout quickview ex5:1.1
    i New version 1.4.1 available (installed version is 1.2.0) at https://github.com/docker/scout-cli
    ✓ Image stored for indexing
    ✓ Indexed 216 packages

  Target     │  ex5:1.1             │    0C     2H     5M    21L   
    digest   │  b79788ea23da        │                              
  Base image │  eclipse-temurin:21  │    0C     0H     5M    21L   

What's Next?
  View vulnerabilities → docker scout cves ex5:1.1
  Include policy results in your quickview by supplying an organization → docker scout quickview ex5:1.1 --org <organization>
~~~



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
