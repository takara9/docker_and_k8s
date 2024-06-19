# サービス　NodePort

K8sクラスタのノードに、クラスタ外部からサービスへアクセスするためのポードを開きます。


## 準備

```
$ minikube start
$ kubectl get no
```


## 実行例

ポッドとサービス(タイプ=NodePort)をデプロイして、サービスを確認する。
```
$ kubectl create deployment hello-minikube1 --image=kicbase/echo-server:1.0
$ kubectl expose deployment hello-minikube1 --type=NodePort --port=8080
$ kubectl get svc hello-minikube1
NAME              TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
hello-minikube1   NodePort    10.100.94.31   <none>        8080:31017/TCP   5s
```

ノードのIPアドレスで 30017 をアクセスすることで、サービスが連携するポッドへアクセスできる。
```
$ curl http://ノードのIPアドレス:31017/
```

Minikubeは、Dockerネットワーク内にノードのIPアドレスがあるので、直接アクセスできない。
次のコマンドで、NodePortのサービスへ繋げることできる。

```
$ minikube service hello-minikube1 --url
http://127.0.0.1:50966
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。
```

アクセステスト
```
$ curl http://127.0.0.1:50966/
Request served by hello-minikube1-67bf99b564-pm5nn

HTTP/1.1 GET /

Host: 127.0.0.1:50966
Accept: */*
User-Agent: curl/8.6.0
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

