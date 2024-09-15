# コンテナの起動と停止

## コンテナの実行と停止

```
PS > docker run --name hw hello-world
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
```


起動後のコンテナの確認
```
PS > docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES

PS > docker ps -a
CONTAINER ID   IMAGE         COMMAND    CREATED              STATUS                          PORTS     NAMES
68859fe27ebb   hello-world   "/hello"   About a minute ago   Exited (0) About a minute ago             hw
```

コンテナのログを確認
```
PS > docker logs hw      

Hello from Docker!
This message shows that your installation appears to be working correctly.
<以下省略>
```

コンテナの削除
```
PS > docker rm hw
hw

PS > docker ps   
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

イメージの削除
```
PS > docker images
REPOSITORY                    TAG       IMAGE ID       CREATED         SIZE
hello-world                   latest    d2c94e258dcb   16 months ago   13.3kB

PS > docker rmi hello-world
Untagged: hello-world:latest
Untagged: hello-world@sha256:53cc4d415d839c98be39331c948609b659ed725170ad2ca8eb36951288f81b75
Deleted: sha256:d2c94e258dcb3c5ac2798d32e1249e42ef01cba4841c2234249495f87264ac5a
Deleted: sha256:ac28800ec8bb38d5c35b49d45a6ac4777544941199075dff8c4eb63e093aa81e

PS > docker images
REPOSITORY   TAG       IMAGE ID   CREATED   SIZE
```


## Linuxコンテナの実行

Ubuntuコンテナの起動
```
PS > $path = (Get-Location).Path + "/my-home"
PS > docker run -it --name my-linux -v ${path}:/home/dev ubuntu bash
root@a18f63c51bf7:/# df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay        1007G  3.7G  952G   1% /
tmpfs            64M     0   64M   0% /dev
tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
shm              64M     0   64M   0% /dev/shm
C:\             477G   74G  403G  16% /home/dev
/dev/sdd       1007G  3.7G  952G   1% /etc/hosts
tmpfs           3.9G     0  3.9G   0% /proc/acpi
tmpfs           3.9G     0  3.9G   0% /sys/firmware
```

```
root@a18f63c51bf7:/# apt update -y && apt install golang
＜中略＞
root@a18f63c51bf7:/# go version
go version go1.22.2 linux/amd64

root@a18f63c51bf7:/ cd /home/dev
root@a18f63c51bf7:/home/dev# go mod init main
go: creating new go.mod: module main
go: to add module requirements and sums:
        go mod tidy
root@a18f63c51bf7:/home/dev# go mod tidy
root@a18f63c51bf7:/home/dev# go run main.go 
Hello container world!

root@a18f63c51bf7:/home/dev# exit
```

```
PS > docker ps -a 
CONTAINER ID   IMAGE     COMMAND   CREATED          STATUS                     PORTS     NAMES
a18f63c51bf7   ubuntu    "bash"    18 seconds ago   Exited (0) 5 seconds ago             my-linux

PS > docker rm my-linux
my-linuix
```



コンテナの削除オプション「--rm」付きの Ubuntuコンテナの起動
```
PS > docker run -it --name my-ubuntu --rm ubuntu bash
root@d3ee178e87fc:/# pwd
/
root@d3ee178e87fc:/# exit
exit

PS > docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

Ubuntuのイメージの削除
```
PS > docker images      
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
ubuntu       latest    edbfe74c41f8   6 weeks ago   78.1MB

PS > docker rmi ubuntu
Untagged: ubuntu:latest
Untagged: ubuntu@sha256:8a37d68f4f73ebf3d4efafbcf66379bf3728902a8038616808f04e34a9ab63ee
Deleted: sha256:edbfe74c41f8a3501ce542e137cf28ea04dd03e6df8c9d66519b6ad761c2598a
Deleted: sha256:f36fd4bb7334b7ae3321e3229d103c4a3e7c10a263379cc6a058b977edfb46de
```



## Webサーバーのコンテナ実行

Windowsで DockerDesktopを使用するケース
```
PS > docker run -d --name web -p 8080:80 nginx
```

macOS, Linuxで DockerDesktopを使用するケース
```
$ docker run -d --name web -p 8080:80 nginx
```


パソコンのフォルダをコンテンツを表示する

Windowsで DockerDesktopを使用するケース 
PowerShell のコマンドプロンプトを開いて以下を実行
```
PS > $path = (Get-Location).Path + "/contents_root"
PS > docker run -d --name web -v ${path}:/usr/share/nginx/html -p 8080:80 nginx
```

macOS, Linuxで DockerDesktopを使用するケース
ターミナルを開いて以下のコマンドを実行
```
$ docker run -d --name web -v $PWD/contents_root:/usr/share/nginx/html -p 8080:80 nginx
```

```
PS > docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED         STATUS         PORTS                  NAMES
922ebdecaede   nginx     "/docker-entrypoint.…"   3 minutes ago   Up 3 minutes   0.0.0.0:8080->80/tcp   web

PS > docker stop web 
web

PS > docker ps
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

停止中コンテナの開始
```
PS > docker start web
web

PS > docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED         STATUS         PORTS                  NAMES
922ebdecaede   nginx     "/docker-entrypoint.…"   4 minutes ago   Up 5 seconds   0.0.0.0:8080->80/tcp   web
```

停止したコンテナの削除
```
PS C:\Users\tkr99\docker_and_k8s> docker ps -a
PS C:\Users\tkr99\docker_and_k8s> docker rm web
PS C:\Users\tkr99\docker_and_k8s> docker ps -a
```

イメージの削除
```
PS C:\Users\tkr99\docker_and_k8s> docker images
PS C:\Users\tkr99\docker_and_k8s> docker rmi nginx
PS C:\Users\tkr99\docker_and_k8s> docker rmi -f nginx
PS C:\Users\tkr99\docker_and_k8s> docker images
```



## データベースのコンテナ実行


Windows データベースサーバー
PowerShell のコマンドプロンプトを開いて以下を実行
```
PS > $path = (Get-Location).Path + "/data_vol"
PS > docker run --name my-db -v ${path}:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret -d mysql
```

macOS データベースサーバー
ターミナルを開いて以下のコマンドを実行
```
$ docker run --name my-db -v $PWD/data_vol:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=secret -d mysql
```

コンテナ内のコマンド mysql を実行
```
PS > docker exec -it my-db mysql -p
Enter password: secret
Welcome to the MySQL monitor.  Commands end with ; or \g.
＜中略＞
mysql> create database mydb;
Query OK, 1 row affected (0.03 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.01 sec)

mysql> quit
Bye
```


データベースを一旦止めて、再スタート
```
PS > docker stop my-db
my-db
PS > docker ps -a      
CONTAINER ID   IMAGE     COMMAND                   CREATED         STATUS                      PORTS     NAMES
2a2856250523   mysql     "docker-entrypoint.s…"   2 minutes ago   Exited (0) 14 seconds ago             my-db
```

停止中のコンテナを実行開始
```
PS > docker start my-db
my-db

PS > docker exec -it my-db mysql -p
Enter password:
Welcome to the MySQL monitor.  Commands end with ; or \g.
＜中略＞
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.02 sec)

mysql>
```



## イメージとレジストリ

```
$ export CR_PAT=YOUR_TOKEN
$ export USERNAME=YOUR_USERID 
$ echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
PS > docker pull ghcr.io/takara9/my-ubuntu:0.2
0.2: Pulling from takara9/my-ubuntu
7734efb8b826: Pull complete
af04a071076c: Pull complete
Digest: sha256:69761cfbffb581e1b53834f8d1ea52ca98ddd217efec857b906c12847112a405
Status: Downloaded newer image for ghcr.io/takara9/my-ubuntu:0.2
ghcr.io/takara9/my-ubuntu:0.2
```


## Dockerの互換ソフトウェアPodman

```
$ podman run hello-world
$ podman run index.docker.io/hello-world
```




## 参考資料
- 日本語 dockerコマンド https://docs.docker.jp/engine/reference/commandline/
- dockerコマンドリファレンス https://docs.docker.com/reference/cli/docker/
- GitHubプロファイル https://github.com/settings/profile
- GHCRレジストリ https://github.com/takara9?tab=packages
- hello-world https://hub.docker.com/_/hello-world
- nginx https://hub.docker.com/_/nginx
- mysql https://hub.docker.com/_/mysql
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
- podmanホームページ https://podman.io/
- containerdホームページ https://containerd.io/

