
## Minikubeの初期化

```
$ minikube delete
$ minikube start
$ minikube addons enable csi-hostpath-driver
```

## オブジェクトストレージ MinIOの起動

[MinIOの起動](../objectstorage-service/) に従って、オブジェクトストレージを準備する。

MinIOのアクセスキーとシークレットを webservice-system/bases/secret-backup.yaml へセットする。


## 各環境を起動

### ステージング環境
```
$ kubectl apply -k overlays/stage/
```

### 本番環境
```
$ kubectl apply -k overlays/prod/
```

## アクセステスト
```
$ kubectl run -it mypod --rm --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
```

### 環境に応じたURLをセットする

本番
```
URL=http://rest-service.prod.svc:9100/
```

ステージング
```
URL=http://rest-service.stage.svc:9100/
```

### ポッドへのアクセステスト

```
root@mypod:/# curl $URL/ping;echo
PONG!

root@mypod:/# curl $URL/info;echo
Host Name: rest-7478b84459-dd8jx
Host IP: 10.244.0.69
Client IP : 10.244.0.31
```

### アプリケーションのテスト

```
root@mypod:/# curl $URL/person/1/
{"first_name":"sazae","id":1,"last_name":"fuguta"}

root@mypod:/# curl $URL/person/2/
{"first_name":"masuo","id":2,"last_name":"fuguta"}

root@mypod:/# curl $URL/person/3/
{"first_name":"namihei","id":3,"last_name":"isono"}

root@mypod:/# curl -X POST -H "Content-Type: application/json" -d '{"fname" : "fune" , "lname" : "isono"}' $URL/person/

root@mypod:/# curl $URL/person/4/
{"first_name":"fune","id":4,"last_name":"isono"}

root@mypod:/# curl $URL/persons  
[{"first_name":"sazae","id":1,"last_name":"fuguta"},{"first_name":"masuo","id":2,"last_name":"fuguta"},{"first_name":"namihei","id":3,"last_name":"isono"}]
```

## おまけ

データベースのテーブル作成と初期データの設定は、自動的にジョブで実行していますが、クライアントから実施するケースの手順を記載しておきます。

```
kubectl exec -it db-0 -n stage -- bash
mariadb --user user1 --password=passwd1 mydb
 
CREATE TABLE Persons (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50),
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC));

INSERT INTO Persons VALUES (1, "sazae","fuguta");
INSERT INTO Persons VALUES (2, "masuo","fuguta");
INSERT INTO Persons VALUES (3, "namihei","isono");
select * from Persons;
```
