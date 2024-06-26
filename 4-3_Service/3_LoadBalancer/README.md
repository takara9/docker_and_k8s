# サービス ロードバランサー
K8sクラスタの外部のロードバランサーと連携して、リクエストをサービスと連携するポッドへ転送します。


## 準備
minikubeを起動した後に、もう一つトンネルを起動します。
トンネルは実行中した状態で、もう一つターミナルを開いて、後続のコマンドを実行していきます。

```
$ minikube start
$ minikube tunnel
```



## ロードバランサーの実行例

デプロイメントで複数のポッドを起動、ロードバランサータイプのサービスをデプロイします。
```
$ kubectl create deployment my-pods --replicas=3 --image=ghcr.io/takara9/ex1:1.5 
$ kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66dbbd8bd4-kxksv   1/1     Running   0          91s   10.244.0.8   minikube
my-pods-66dbbd8bd4-lp6r5   1/1     Running   0          91s   10.244.0.6   minikube
my-pods-66dbbd8bd4-mlvzc   1/1     Running   0          91s   10.244.0.7   minikube

$ kubectl expose deployment my-pods --type=LoadBalancer --port=9100
$ kubectl get svc my-pods
NAME      TYPE           CLUSTER-IP      EXTERNAL-IP     PORT(S)          AGE
my-pods   LoadBalancer   10.104.46.104   10.104.46.104   9100:30700/TCP   8s
```

minikubeのトンネルにより、curlに以下のオプションをつけて、ポッドへアクセスできます。

`curl http://EXTERNAL-IP:PORT`


アクセス例では、ホスト名とIPアドレスから、複数のポッドから応答が来ていることが判ります。
```
$ curl http://10.104.46.104:9100/info
Host Name: my-pods-66dbbd8bd4-mlvzc
Host IP: 10.244.0.7
Client IP : 10.244.0.1

$ curl http://10.104.46.104:9100/info
Host Name: my-pods-66dbbd8bd4-lp6r5
Host IP: 10.244.0.6
Client IP : 10.244.0.1

$ curl http://10.104.46.104:9100/info
Host Name: my-pods-66dbbd8bd4-mlvzc
Host IP: 10.244.0.7
Client IP : 10.244.0.1

$ curl http://10.104.46.104:9100/info
Host Name: my-pods-66dbbd8bd4-kxksv
Host IP: 10.244.0.8
Client IP : 10.244.0.1
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#loadbalancer



