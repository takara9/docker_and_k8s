# サービス ロードバランサー
K8sクラスタの外部のロードバランサーと連携して、リクエストをサービスと連携するポッドへ転送します。


## 準備

```
$ minikube start
$ minikube tunnel
```

## ロードバランサーの実行例
別のターミナルを開いて、以下を実行

```
kubectl create deployment hello-minikube1 --image=kicbase/echo-server:1.0
kubectl expose deployment hello-minikube1 --type=LoadBalancer --port=8080
kubectl get svc
curl http://REPLACE_WITH_EXTERNAL_IP:8080
```

サービスを確認して、EXTERNAL-IP:8080 へアクセスする
```
$ kubectl get svc hello-minikube1
NAME              TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
hello-minikube1   LoadBalancer   10.107.149.167   127.0.0.1     8080:30616/TCP   8s

$ curl http://127.0.0.1:8080/
Request served by hello-minikube1-67bf99b564-2hb68

HTTP/1.1 GET /

Host: 127.0.0.1:8080
Accept: */*
User-Agent: curl/8.6.0
```

## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer
