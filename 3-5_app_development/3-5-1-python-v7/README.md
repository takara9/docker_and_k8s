## イメージのビルドと実行

docker build -t ex1:1.7 .
docker run --name ex1 --rm --publish 9107:9100 --detach ex1:1.7


## アクセス

curl http://localhost:9107/ping;echo
curl http://localhost:9107/info;echo


## コンテナへ入る

docker exec -it ex1 bash


## イメージをレジストリへ登録

export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex1:1.7 ghcr.io/takara9/ex1:1.7
docker push ghcr.io/takara9/ex1:1.7


## クリーンナップ

docker stop ex1
docker rm ex1
docker rmi ghcr.io/takara9/ex1:1.7
docker rmi ex1:1.7


# テスト



## DBのコンテナを起動

docker run -d --name mydb -p 3306:3306 \
--env MARIADB_USER=user1 \
--env MARIADB_PASSWORD=secret1 \
--env MARIADB_DATABASE=mydb \
--env MARIADB_ROOT_PASSWORD=secret0 \
mariadb:latest


docker exec -it mydb bash
mariadb --user user1 --password=secret1 mydb


## テーブルを作成

CREATE TABLE Persons (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));




## アクセステスト


mysql --host 127.0.0.1 --port 3306 --user user1 --password=secret1 mydb


curl -X POST -H "Content-Type: application/json" -d '{"fname" : "maihei" , "lname" : "isono"}' http://localhost:9107/person/
{"fname":"maihei","lname":"isono"}

curl -X GET -H "Content-Type: application/json" http://localhost:9107/persons