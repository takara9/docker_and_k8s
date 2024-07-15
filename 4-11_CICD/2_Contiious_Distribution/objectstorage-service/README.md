# バックアップのためのオブジェクトストレージデプロイ方法


## Minikubeの起動

既に起動されていればスキップする。

```
minikube start
minikube addons enable csi-hostpath-driver

```
--network=socket_vmnet

## MinIO オブジェクトストレージ　の起動


```
cd docker_and_k8s/4-3_controller/4-3-5-System_Integration/objectstorage-service
kubectl apply -k .
```

## 起動の確認法

```
kubectl get po -n storage
kubectl get svc -n storage
```

## MinIOコンソールへのアクセス

ターミナルから下記のコマンドを実行します。ターミナルを閉じてはいけません。

```
kubectl port-forward -n storage service/minio 9001 9000
```

次のURLをパソコンのブラウザでアクセス

http://localhost:9001/login


ユーザーID minioadmin、パスワード　minioadmin でログインする。


### バケットを作成

バックアップデータの格納先を作成します。

![](images/create-backet.png)


### アクセスキーとシークレットを生成

アクセスキーを作成するには、右上の「Create access key +」をクリックする
![](images/create-access-key1.png)

画面下の「Create」をクリックする。表示されたアクセスキーとシークレットキーをローカルPCに保存しておく。

![](images/create-access-key2.png)

