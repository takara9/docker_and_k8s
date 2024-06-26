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
$ kubectl create deployment my-pods --image=ghcr.io/takara9/ex1:1.5
$ kubectl expose deployment my-pods --type=NodePort --port=9100
$ kubectl get svc my-pods
NAME      TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
my-pods   NodePort   10.107.15.170   <none>        9100:30900/TCP   8s
```

Minikubeは、Dockerネットワーク内にノードのIPアドレスがあるので、直接アクセスできない。
次のコマンドで、NodePortのサービスへ繋げることできる。
```
$ minikube service my-pods --url
http://192.168.49.2:30900
```

上記表示されたURLへアクセスすることで、ノードポートで開いたと同じ様に、クラスタ内のポッドにアクセスできる
```
$ curl http://192.168.49.2:30900/info
Host Name: my-pods-66dbbd8bd4-l42fq
Host IP: 10.244.0.3
Client IP : 10.244.0.1
```




## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport

