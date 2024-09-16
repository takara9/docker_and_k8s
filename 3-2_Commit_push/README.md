
## ubuntuのコンテナを起動　（ターミナルで実行）
```
docker run -it --name my-ubuntu ubuntu:22.04
```

## 近くのルーターにpingを実行　（コンテナで実行）
```
ping 192.168.1.1
```

## コンテナへpingコマンドをインストール　（コンテナで実行）
```
apt-get update -y
apt-get install iputils-ping
exit
```


## コマンドを追加したコンテナを、イメージとして保存 （別ターミナルで実行）
```
docker commit my-ubuntu my-ubuntu:0.2
```

## 動作確認 （別ターミナルで実行）
```
docker run -it --name my-ubuntu2 my-ubuntu:0.2
ping 192.168.1.1
exit
```

## レジストリへアップロード
```
docker tag my-ubuntu:0.2 ghcr.io/takara9/my-ubuntu:0.2
docker images
export USERNAME=YOUR_USER_ID
export CR_PAT=YOUR_TOKEN
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker push ghcr.io/takara9/my-ubuntu:0.2
```

## クリーンナップ
```
docker stop my-ubuntu2 
docker rm my-ubuntu2
docker rm my-ubuntu
docker rmi my-ubuntu:0.2
docker rmi ghcr.io/takara9/my-ubuntu:0.2
docker rmi ubuntu:22.04
```


## コンテナは起動が早くサイズが小さい
```
# 初回起動時の所要時間
$ time docker run -it python python --version
Unable to find image 'python:latest' locally
latest: Pulling from library/python
238a68c3d761: Download complete 
56c9b9253ff9: Download complete 
364d19f59f69: Download complete 
843b1d832182: Download complete 
a348c2a8d946: Download complete 
799b63efcab5: Download complete 
353de11681b2: Download complete 
Digest: sha256:7859853e7607927aa1d1b1a5a2f9e580ac90c2b66feeb1b77da97fed03b1ccbe
Status: Downloaded newer image for python:latest
Python 3.12.6

real    0m11.180s
user    0m0.043s
sys     0m0.039s

# ２回目以降の起動所要時間
$ time docker run -it python python --version
Python 3.12.6

real    0m0.237s
user    0m0.021s
sys     0m0.018s

# Python イメージのサイズ
$ docker images python:latest
REPOSITORY   TAG       IMAGE ID       CREATED      SIZE
python       latest    7859853e7607   6 days ago   1.46GB
```


## コンテナをホストOSから覗く

ターミナル2からコンテナ実行環境を観察
```
ubuntu@server0:~$ docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
ubuntu@server0:~$ ps -ax |grep -E 'containerd|dockerd'
    853 ?        Ssl    0:00 /usr/bin/containerd
   1106 ?        Ssl    0:00 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
   5643 pts/2    S+     0:00 grep --color=auto -E containerd|dockerd
```

ターミナル2からコンテナを起動
```
$ docker run -it ghcr.io/takara9/my-ubuntu:0.1 sleep 1234
Unable to find image 'ghcr.io/takara9/my-ubuntu:0.1' locally
0.1: Pulling from takara9/my-ubuntu
32802c0cfa4d: Pull complete 
da1315cffa03: Pull complete 
fa83472a3562: Pull complete 
f85999a86bef: Pull complete 
b7c86423aba8: Pull complete 
Digest: sha256:a69a4082f080abc3975261ea983e6ff3b34051ed9edc9d507079d2a67ef9e017
Status: Downloaded newer image for ghcr.io/takara9/my-ubuntu:0.1
```

ターミナル1からコンテナを観察
```
$ ps -ax |grep -E 'containerd|dockerd|sleep'
    853 ?        Ssl    0:00 /usr/bin/containerd
   1106 ?        Ssl    0:09 /usr/bin/dockerd -H fd:// --containerd=/run/containerd/containerd.sock
   5816 pts/3    Sl+    0:00 docker run -it ghcr.io/takara9/my-ubuntu:0.1 sleep 1234
   5901 ?        Sl     0:00 /usr/bin/containerd-shim-runc-v2 -namespace moby -id 0983916aa5d81d8b0b12bec2a804df37c587500f0eae86b58a10382f914949a4 -address /run/containerd/containerd.sock
   5920 pts/0    Ss+    0:00 sleep 1234
   5950 pts/2    S+     0:00 grep --color=auto -E containerd|dockerd|sleep
```

ターミナル１から、コンテナ内のプロセスを強制的停止
```
$ sudo kill -9 5920
```

ターミナル3を開いて、プロセスの状況を確認
```
$ docker run -it ubuntu
# ps -ax
```

## コンテナはホストのカーネルを共有

```
uname -a
docker run -it --rm ubuntu
docker run -it --rm debian
docker run -it --rm fedora
```

