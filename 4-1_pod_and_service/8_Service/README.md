# サービスの役割
サービスは、ポッドにリクエストを届けるためのオブジェクトです。ポッドは揮発性の性質を補うものとして、IPアドレスの永続化やDNSへの登録を担う役目もあります。


## 準備

```
$ minikube start --nodes=3
$ minikube status
$ kubectl get no
```

## 実行例

サービスのIPアドレス
```
$ kubectl run my-pod --image=ghcr.io/takara9/ex1:1.0
pod/my-pod created
$ kubectl expose pod my-pod --port=9100 --target-port=9100 --name=my-service
service/my-service exposed
$ kubectl get svc my-service
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
my-service   ClusterIP   10.100.2.115   <none>        9100/TCP   9s
```

別ポッドからサービスの存在を環境変数で知る
```
$ kubectl run -it mypod2 --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash
If you don't see a command prompt, try pressing enter.
root@mypod2:/# env |grep MY_SERVICE
MY_SERVICE_SERVICE_HOST=10.100.2.115
MY_SERVICE_PORT=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP_PROTO=tcp
MY_SERVICE_PORT_9100_TCP_ADDR=10.100.2.115
MY_SERVICE_SERVICE_PORT=9100
MY_SERVICE_PORT_9100_TCP_PORT=9100
```

別ポッドからサービスのIPアドレスをDNSで知る方法
```
root@mypod2:/# dig my-service.default.svc.cluster.local +short
10.100.2.115
```

ヘッドレスのサービスのデプロイ
```
## 最初にポッドをデプロイしておくため、前述のClusteIPタイプのマニフェストを適用します
$ kubectl apply -f service-clusterip.yaml 
service/ex1 created
pod/ex1-pod created

## ヘッドレスのサービスをデプロイします
$ kubectl apply -f service-headless.yaml 
service/ex1-hl created

## ポッドのIPアドレスを確認しておきます
$ kubectl get po -o wide
NAME      READY   STATUS    RESTARTS   AGE   IP           NODE
ex1-pod   1/1     Running   0          82s   10.244.0.3   minikube

## サービスは、ClusterIPとヘッドレスがリストされています
$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
ex1          ClusterIP   10.107.63.174   <none>        80/TCP     96s
ex1-hl       ClusterIP   None            <none>        9100/TCP   89s
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    2m25s

## ヘッドレスのサービスへポートフォワードして、パソコンからアクセスできる様にセットします
$ kubectl port-forward service/ex1-hl 9100:9100
Forwarding from 127.0.0.1:9100 -> 9100
Forwarding from [::1]:9100 -> 9100
Handling connection for 9100
```

ヘッドレスのサービスの動作確認
```
## 対話型でポッドを起動
$ kubectl run -it mypod --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash

## サービス名が内部DNSへ登録されたこと、ポッドのIPアドレスがセットされていることを確認
root@mypod:/# nslookup         
> ex1-hl
Server:		10.96.0.10
Address:	10.96.0.10#53

Name:	ex1-hl.default.svc.cluster.local
Address: 10.244.0.3

## ヘッドレスのサービス名が、環境変数にセットされていないこと確認
root@mypod:/# env |grep EX1
EX1_PORT_80_TCP_PORT=80
EX1_PORT_80_TCP_ADDR=10.107.63.174
EX1_PORT=tcp://10.107.63.174:80
EX1_SERVICE_PORT=80
EX1_SERVICE_HOST=10.107.63.174
EX1_PORT_80_TCP=tcp://10.107.63.174:80
EX1_PORT_80_TCP_PROTO=tcp

## 最後にcurlで、ヘッドレスなサービスへ、アクセスして応答を確認
PONG!root@mypod:/# curl ex1-hl:9100/ping;echo
PONG!
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/