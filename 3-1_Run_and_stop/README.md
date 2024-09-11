# コンテナの起動と停止

## コンテナの実行と停止

```
PS C:\Users\tkr\docker_and_k8s> docker run --name hw hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
c1ec31eb5944: Pull complete
Digest: sha256:53cc4d415d839c98be39331c948609b659ed725170ad2ca8eb36951288f81b75
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/

PS C:\Users\tkr\docker_and_k8s> 
```

起動後のコンテナの確認
```
PS C:\Users\tkr\docker_and_k8s> docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

PS C:\Users\tkr\docker_and_k8s> docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                          PORTS     NAMES
68859fe27ebb   hello-world   "/hello"   About a minute ago   Exited (0) About a minute ago             hw
```

コンテナのログを確認
```
PS C:\Users\tkr\docker_and_k8s> docker logs hw      

Hello from Docker!
This message shows that your installation appears to be working correctly.
<以下省略>
```

コンテナの削除
```
$ docker rm hw
hw

$ docker ps   
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

イメージのリスト表示
```
$ docker images
REPOSITORY                    TAG       IMAGE ID       CREATED         SIZE
hello-world                   latest    d2c94e258dcb   16 months ago   13.3kB
```

イメージの削除
```
$ docker rmi hello-world
Untagged: hello-world:latest
Untagged: hello-world@sha256:53cc4d415d839c98be39331c948609b659ed725170ad2ca8eb36951288f81b75
Deleted: sha256:d2c94e258dcb3c5ac2798d32e1249e42ef01cba4841c2234249495f87264ac5a
Deleted: sha256:ac28800ec8bb38d5c35b49d45a6ac4777544941199075dff8c4eb63e093aa81e

$ docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
```



```
PS C:\Users\tkr99\docker_and_k8s> docker run -it --name my-ubuntu ubuntu bash 
Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
31e907dcc94a: Pull complete
Digest: sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab63ee
Status: Downloaded newer image for ubuntu:latest
root@2a391b3602db:/# pwd
/
root@2a391b3602db:/# ks
bash: ks: command not found
root@2a391b3602db:/# ls
bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
```



バックグランドでコンテナの起動
```
docker run -d --name web nginx
docker ps
docker stop web
docker ps
docker ps -a
docker rm web
```



```
PS C:\Users\tkr99\docker_and_k8s> docker run -d --name web -p 8080:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
a2318d6c47ec: Pull complete
095d327c79ae: Pull complete
bbfaa25db775: Pull complete
7bb6fb0cfb2b: Pull complete
0723edc10c17: Pull complete
24b3fdc4d1e3: Pull complete
3122471704d5: Pull complete
Digest: sha256:04ba374043ccd2fc5c593885c0eacddebabd5ca375f9323666f28dfd5a9710e3
Status: Downloaded newer image for nginx:latest
43cb34ac218d28afa072e8b9c3d4ec52fc47568fc19a5ce3aca871e4ee113572
```

```
PS C:\Users\tkr99\docker_and_k8s> docker ps
PS C:\Users\tkr99\docker_and_k8s> docker stop web
PS C:\Users\tkr99\docker_and_k8s> docker ps
```


```
PS C:\Users\tkr99\docker_and_k8s> docker ps -a
PS C:\Users\tkr99\docker_and_k8s> docker rm web
PS C:\Users\tkr99\docker_and_k8s> docker ps -a
```

```
PS C:\Users\tkr99\docker_and_k8s> docker images
PS C:\Users\tkr99\docker_and_k8s> docker rmi nginx
PS C:\Users\tkr99\docker_and_k8s> docker rmi -f nginx
PS C:\Users\tkr99\docker_and_k8s> docker images
```


Windows Webサーバー
```
docker run -d --name web -v C:\Users\tkr99\docker_and_k8s\3-1_Run_and_stop\contents_root:/usr/share/nginx/html -p 8080:80 nginx
```

Windows データベースサーバー
```
docker run --name my-db -v C:\Users\tkr99\docker_and_k8s\3-1_Run_and_stop\data_vol:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret -d mysql
```





```
docker stop my-db             
docker start my-db
docker exec -it my-db mysql -p
Enter password: 
```


docker run -d --name web -v $ $-p 8080:80 nginx

イメージの削除

```
docker images
docker rmi -f nginx
docker images
```

```
PS C:\Users\tkr99\docker_and_k8s> docker images
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    39286ab8a5e1   3 weeks ago   188MB

PS C:\Users\tkr99\docker_and_k8s> docker rmi -f nginx
Untagged: nginx:latest
Untagged: nginx@sha256:04ba374043ccd2fc5c593885c0eacddebabd5ca375f9323666f28dfd5a9710e3
Deleted: sha256:39286ab8a5e14aeaf5fdd6e2fac76e0c8d31a0c07224f0ee5e6be502f12e93f3
Deleted: sha256:d71f9b66dd3f9ef3164d7023cc99ce344d209decd5d6cd56166c0f7a2f812c06
Deleted: sha256:634d30adf8a2232256b2871e268c8f0fdb2c348374cd8510920a76db56868e16
Deleted: sha256:f230be3f4e104c7414b7ce9c8d301f37061b4e06afe010878ea55f858d89f7f3
Deleted: sha256:c5210c8480131b7dbc5ad8adc425d68cd7a8848ee2e07de3c69cb88a4b8fd662
Deleted: sha256:d4f588811a337e0b01da46772d02f7f82ee5f9baff6886365ffb912d455f4f53
Deleted: sha256:d73e21a1e27b0184b36f6578c8d0722a44da253bc74cd72e9788763f4a4de08f
Deleted: sha256:8e2ab394fabf557b00041a8f080b10b4e91c7027b7c174f095332c7ebb6501cb

PS C:\Users\tkr99\docker_and_k8s> docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
PS C:\Users\tkr99\docker_and_k8s> 
```



## イメージとレジストリ

```
$ export CR_PAT=YOUR_TOKEN
$ export USERNAME=YOUR_USERID 
$ echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
$ docker pull ghcr.io/takara9/my-ubuntu:0.3
0.1: Pulling from takara9/my-ubuntu
Digest: sha256:69761cfbffb581e1b53834f8d1ea52ca98ddd217efec857b906c12847112a405
Status: Downloaded newer image for ghcr.io/takara9/my-ubuntu:0.3
```


## Dockerの互換ソフトウェアPodman

```
$ podman run hello-world
$ podman run index.docker.io/hello-world
```


## クリーンナップ
docker rm hw
docker rmi hello-world:latest


## イメージの取得
docker pull ghcr.io/takara9/my-ubuntu:0.2 <-- 不要ではないか

## 対話型コンテナの実行
docker run -it --name mu ghcr.io/takara9/my-ubuntu:0.2
exit


## クリーンナップ
docker rm mu
docker rmi ghcr.io/takara9/my-ubuntu:0.2


## 参考資料
- Docker Hub https://hub.docker.com/
      Docker Hubは、Dockerコンテナの存在や利便性を、広く知らしめたサービスです。改めて解説する必要は無いかもしれません。インターネットで公開することも、アクセス制限を設定して特定のグループで共有することもできます。レジストリの機能に加えて、ブラウザを使ってイメージを検索、起動の方法や使い方の説明なども見ることができます。
- Distribution https://github.com/distribution/distribution
      Distributionは、もとはDocker社によって開発され、CNCFに寄贈されたソフトウェアです。シンプルなレジストリ サービスの実装で、多くのプロジェクトが参考にしています。
- Harbor  https://goharbor.io/
      VMware社がOSSとして開発しました。レジストリ機能に加えて、ブラウザでの参照機能や、脆弱性診断など、多彩な機能を持っています。
- Quay.io https://goharbor.io/
      現在はRed Hat社のサービスとして提供されるだけでなく、オンプレミスで動作させることができるソフトウェアとして使用権とサポートサービスを購入できます。
- https://docs.aws.amazon.com/ja_jp/AmazonECR/latest/userguide/what-is-ecr.html
      パブリッククラウドのAWS, Azure, Google Cloud, IBM Cloud などもレジストリ サービスを提供しています。自社のクラウドサービス利用者に有利なサービスを提供していますので、読者にとって最適なサービスを選択すると良いでしょう。リンクはAmazon ECRの解説ページです。
- GitHub https://ghcr.io/
      ソースコードを管理するサービスを提供するGitHubもコンテナのレジストリ サービスを提供しています。同社の継続的インテグレーション(CI)サービスのGitHub Actionsと連携できる便利なサービスです。

