## Drupalの開始

docker network create my-net

docker volume create my-mariadb
docker volume create my-drupal-web

docker run -d --name my-mariadb --network my-net --mount source=my-mariadb,target=/var/lib/mysql -e MARIADB_ROOT_PASSWORD=drupal mariadb:10.3.39-focal
docker logs my-mariadb

docker run --name my-drupal --network my-net --mount source=my-drupal-web,target=/opt/drupal/web -p 8100:80 -d drupal


## Drupalへのアクセス

ブラウザで、次のアドレスをアクセスする。

http://localhost:8100


## クリーンナップ

### コンテナの停止と削除
docker stop my-drupal
docker rm my-drupal
docker stop my-mariadb
docker rm my-mariadb

docker rmi mariadb:10.3.39-focal
docker rmi drupal:latest


### 永続ボリュームの削除
docker volume rm my-mariadb
docker volume rm my-drupal-web
### ネットワークの削除
docker network rm my-net






