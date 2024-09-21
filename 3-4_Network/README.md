# コンテナのネットワーク

## コンテナのブリッジ ネットワーク

Dockerエンジンが管理するコンテナ ネットワークのリスト
```
$ docker network ls
```

## コンテナ同士の通信

ターミナル１ コンテナ-1
```
$ docker run -it ubuntu
# apt-get update && apt install iputils-ping -y
```

ターミナル２ コンテナ-2
```
$ docker run -it ubuntu
/# apt-get update && apt install iputils-ping -y
```

ターミナル３ コンテナ-1とコンテナ-2のIPアドレスを調べる
```
$ docker ps
$ docker inspect b5e1fcb017f9 |jq -r '.[].NetworkSettings.Networks.bridge.IPAddress' 
$ docker inspect 9280eb2b78f7 |jq -r '.[].NetworkSettings.Networks.bridge.IPAddress' 
```

ターミナル１ コンテナ１からコンテナ２へのping
```
# ping コンテナ-2のIPアドレス -c 3
```

## コンテナのサービス公開

httpbinのコンテナ実行
```
$ docker run -p 1280:80 kennethreitz/httpbin
```

ブラウザで http://localhost:1280/ をアクセスする



## アプリケーション Drupalの構築

ブリッジ ネットワークの作成
```
$ docker network create my-net
$ docker network ls
```


## Drupalのデータベースの開始

DrupalとMariaDBのボリュームの作成
```
$ docker volume create my-mariadb
$ docker volume create my-drupal-web
$ docker volume ls
```

MariaDBの起動オプションと実行
```
$ docker run -d --name my-mariadb --network my-net --mount source=my-mariadb,target=/var/lib/mysql -e MARIADB_ROOT_PASSWORD=drupal mariadb:10.3.39-focal
```

MariaDBのログを確認
```
$ docker logs my-mariadb
$ docker ps
```

## Drupal本体の開始

Drupalの起動オプションと実行
```
$ docker run --name my-drupal --network my-net --mount source=my-drupal-web,target=/opt/drupal/web -p 18080:80 -d drupal
```

Drupalの実行状態の確認
```
$ docker logs my-drupal
$ docker ps
```


## Drupalの初期設定


## 後片付け（クリーンナップ）

コンテナ、永続ボリューム、ブリッジ・ネットワークのクリーンナップ手順
```
# コンテナの停止と削除
$ docker stop my-drupal
$ docker rm my-drupal
$ docker stop my-mariadb
$ docker rm my-mariadb

# 永続ボリュームの削除
$ docker volume rm my-mariadb
$ docker volume rm my-drupal-web

# ネットワークの削除
$ docker network rm my-net
```


## アプリケーション WordPressの構築

WordPress と MySQLの起動手順
```
# 専用ネットワークの作成
$ docker network create my-word-net

# 永続データを保存する領域の作成
$ docker volume create my-mysql
$ docker volume create my-wordpress-web

# MySQLの起動と確認
$ docker run -d --name my-mysql --network my-word-net --mount source=my-mysql,target=/var/lib/mysql \
-e MYSQL_DATABASE=wp \
-e MYSQL_USER=user \
-e MYSQL_PASSWORD=password \
-e MYSQL_RANDOM_ROOT_PASSWORD='1' mysql:8.0
$ docker logs my-mysql

# WordPressの起動と確認
$ docker run --name my-wordpress --network my-word-net --mount source=my-wordpress-web,target=/var/www/html \
-p 18090:80 -d wordpress
$ docker logs my-wordpress

# 起動の再確認
$ docker ps
```


コンテナ、永続ボリューム、ブリッジ・ネットワークのクリーンナップ
```
# クリーンナップ
# コンテナの停止と削除
$ docker stop my-wordpress
$ docker rm my-wordpress
$ docker stop my-mysql
$ docker rm my-mysql

# 永続ボリュームの削除
$ docker volume rm my-mysql
$ docker volume rm my-wordpress-web

# ネットワークの削除
$ docker network rm my-word-net
```

Docker Composeによる起動
```
$ cd wp
$ ls
compose.yml
$ docker compose up -d
maho-2:wp maho$ docker compose up -d
[+] Building 0.0s (0/0)                   docker:desktop-linux
[+] Running 3/3
 ✔ Network wp_my-word-net       Created                   0.0s 
 ✔ Container wp-my-mysql-1      Started                   0.0s 
 ✔ Container wp-my-wordpress-1  Started                   0.0s
```

Docker Compose 実行状態の確認
```
$ docker compose ps
NAME                IMAGE       SERVICE        STATUS         PORTS
wp-my-mysql-1       mysql:8.0   my-mysql       Up 5 seconds   3306/tcp, 33060/tcp
wp-my-wordpress-1   wordpress   my-wordpress   Up 5 seconds   0.0.0.0:18085->80/tcp
```

Docker Compose の再スタート
```
# コンテナの停止
$ docker compose stop
[+] Stopping 2/2
 ✔ Container wp-my-mysql-1      Stopped             1.2s 
 ✔ Container wp-my-wordpress-1  Stopped             1.2s 

# コンテナの開始
$ docker compose start
[+] Running 2/2
 ✔ Container wp-my-wordpress-1  Started             0.3s 
 ✔ Container wp-my-mysql-1      Started   
```


Docker Composeで起動したコンテナの削除
```
# コンテナの停止とコンテナの削除
$ docker compose down
[+] Running 3/3
 ✔ Container wp-my-mysql-1      Removed             1.2s 
 ✔ Container wp-my-wordpress-1  Removed             1.1s 
 ✔ Network wp_default           Removed             0.1s
```


## 参考リンク
- 日本語 dockerコマンド https://docs.docker.jp/engine/reference/commandline/#id6
- dockerコマンドリファレンス https://docs.docker.com/reference/cli/docker/volume/




