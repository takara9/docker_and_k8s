# 3.3


## === フィボナッチの数列を表示 ===

docker run -it -v ${PWD}/src:/mnt python:latest python3 /mnt/fibo.py

docker container prune


## === 永続ボリュームの作成 ===

docker volume ls
docker volume create my-vol
docker volume inspect my-vol


## 永続ボリュームをマウントしたコンテナを起動

docker run -it --name devtest --mount source=my-vol,target=/app ubuntu:latest


### 以下は、上記で起動したコンテナ上で実行

df -h
ps -ax
ps -ax > /app/data.txt
cat /app/data.txt 
exit


## 永続ボリュームをマウントしたコンテナの削除

docker kill devtest <-- 不要
docker rm devtest


## 新しいコンテナを起動して、既存の永続ボリュームをマウントする。

docker run -it --name devtest2 --mount source=my-vol,target=/app ubuntu:latest


### 以下は、上記で起動したコンテナ上で実行

cd /app/
ls -al
cat data.txt
exit

## クリーンナップ
docker rm devtest2
docker volume rm my-vol



## === tmpfsをマウントする ===
 
docker run -it --name tmptest --tmpfs /app ubuntu:latest


### 以下は、上記で起動したコンテナ上で実行

df -h
dd if=/dev/urandom of=/app/test.dat bs=80 count=10
ls -al /app
exit


## コンテナの再スタート

docker ps -a
docker start tmptest
docker exec -it tmptest bash
ls -al /app
exit

## クリーンナップ

docker kill tmptest
docker rm tmptest
