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


## バックアップ

docker run --rm \
      --mount source=my-vol,target=/backup-volume \
      -v "$(pwd)":/backup \
      busybox \
      tar -zcvf /backup/my-vol.tar.gz /backup-volume


mini:~ takara$ cd backup-vol/
mini:backup-vol takara$ docker run --rm \
>       --mount source=my-vol,target=/backup-volume \
>       -v "$(pwd)":/backup \
>       busybox \
>       tar -zcvf /backup/my-vol.tar.gz /backup-volume
tar: removing leading '/' from member names
backup-volume/
backup-volume/check.txt
backup-volume/ls-lR.txt
mini:backup-vol takara$ 


## リストア
docker volume rm my-vol
docker volume create my-vol
docker run --rm \
      --mount source=my-vol,target=/backup-volume \
      -v "$(pwd)":/backup \
      busybox \
      tar -zxvf /backup/my-vol.tar.gz --strip-components 1 -C /backup-volume
docker run -it --rm --name voltest --mount source=my-vol,target=/app ubuntu:latest
root@640715d2f3df:/# sha1sum -c /app/check.txt
/app/ls-lR.txt: OK


$ docker volume rm my-vol
$ docker volume create my-vol
my-vol
$ docker run --rm \
>       --mount source=my-vol,target=/backup-volume \
>       -v "$(pwd)":/backup \
>       busybox \
>       tar -zxvf /backup/my-vol.tar.gz --strip-components 1 -C /backup-volume
backup-volume/
backup-volume/check.txt
backup-volume/ls-lR.txt
$ docker run -it --rm --name voltest --mount source=my-vol,target=/app ubuntu:latest
root@640715d2f3df:/# sha1sum -c /app/check.txt
/app/ls-lR.txt: OK



## コンテナの構造

ベースイメージを「

~~~
$ docker history ubuntu:latest
IMAGE          CREATED       CREATED BY                                       SIZE      COMMENT
e2e172ecd069   2 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/bash"]             0B        
<missing>      2 weeks ago   /bin/sh -c #(nop) ADD file:5703a6689620ec495…   69.3MB    
<missing>      2 weeks ago   /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B        
<missing>      2 weeks ago   /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B        
<missing>      2 weeks ago   /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH      0B        
<missing>      2 weeks ago   /bin/sh -c #(nop)  ARG RELEASE                   0B        
~~~


~~~
mini:~ takara$ docker run -it --name ubuntu-add ubuntu:latest 
root@2c29d2fe2612:/# apt update -y
<中略>
root@2c29d2fe2612:/# apt install iputils-ping -y
<中略>
Setting up iputils-ping (3:20211215-1) ...
root@2c29d2fe2612:/# exit
exit
~~~

~~~
$ docker commit ubuntu-add my-ubuntu:0.3
sha256:d9184c797c857b33a7b6cb8724e87c2f15649cad66ac6ca5a87cbf877092e168

$ docker history my-ubuntu:0.3
IMAGE          CREATED          CREATED BY                                       SIZE      COMMENT
d9184c797c85   15 seconds ago   /bin/bash                                        45.3MB    
e2e172ecd069   2 weeks ago      /bin/sh -c #(nop)  CMD ["/bin/bash"]             0B        
<missing>      2 weeks ago      /bin/sh -c #(nop) ADD file:5703a6689620ec495…   69.3MB    
<missing>      2 weeks ago      /bin/s$h -c #(nop)  LABEL org.opencontainers.…   0B        
<missing>      2 weeks ago      /bin/sh -c #(nop)  LABEL org.opencontainers.…   0B        
<missing>      2 weeks ago      /bin/sh -c #(nop)  ARG LAUNCHPAD_BUILD_ARCH      0B        
<missing>      2 weeks ago      /bin/sh -c #(nop)  ARG RELEASE                   0B    
~~~