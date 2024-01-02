
## WordPressの起動

```
# 専用ネットワークの作成
docker network create my-word-net
# 永続データを保存する領域の作成
docker volume create my-mysql
docker volume create my-wordpress-web
# MySQLの起動と確認
docker run -d --name my-mysql --network my-word-net --mount source=my-mysql,target=/var/lib/mysql \
-e MYSQL_DATABASE=wp \
-e MYSQL_USER=user \
-e MYSQL_PASSWORD=password \
-e MYSQL_RANDOM_ROOT_PASSWORD='1' mysql:8.0
docker logs my-mysql
# WordPressの起動と確認
docker run --name my-wordpress --network my-word-net --mount source=my-wordpress-web,target=/var/www/html \
-p 8200:80 -d wordpress
docker logs my-wordpress
# 起動の再確認
docker ps
```

## アクセス WordPress

http://localhost:8200/


## クリーンナップ

```
# コンテナの停止と削除
docker stop my-wordpress
docker rm my-wordpress
docker stop my-mysql
docker rm my-mysql
# 永続ボリュームの削除
docker volume rm my-mysql
docker volume rm my-wordpress-web
# ネットワークの削除
docker network rm my-word-net
```



## Compose を使った起動
cd wp
docker compose up -d

## 起動の確認
docker compose ps
docker compose ls


## Composeの停止と再スタート
docker compose stop
docker compose start


## 停止とコンテナの削除
docker compose down
docker compose down --rmi all
