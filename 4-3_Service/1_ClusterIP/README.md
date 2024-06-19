# ClusterIP
クラスタIPは、K8sクラスタ内部で、クライアントが、サーバーのポッドへアクセスするために使用します。


## 準備
```
$ minikube start
```


## タイプ　ClusterIP

ポッドとサービスを起動して、サービスのIPアドレスを調べる
```
$ kubectl run my-pod --image=ghcr.io/takara9/ex1:1.0
$ kubectl expose pod my-pod --port=9100 --target-port=9100 --name=my-service
$ kubectl get svc my-service
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
my-service   ClusterIP   10.100.2.115   <none>        9100/TCP   9s
```

別ポッドは、環境変数でサービスの存在を知る
```
$ kubectl run -it mypod2 --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
root@mypod2:/$ env |grep MY_SERVICE
MY_SERVICE_SERVICE_HOST=10.100.2.115
MY_SERVICE_PORT=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP_PROTO=tcp
MY_SERVICE_PORT_9100_TCP_ADDR=10.100.2.115
MY_SERVICE_SERVICE_PORT=9100
MY_SERVICE_PORT_9100_TCP_PORT=9100
```

別ポッドは、DNSでサービスのIPアドレスを知る
```
root@mypod2:/$ dig my-service.default.svc.cluster.local +short
10.100.2.115
```

```
root@mypod2:/$ exit
$ kubectl delete pod my-pod
$ kubectl delete svc my-service
```


## ヘッドレスのサービス
IPアドレス clusterIP=Noneをセットした サービスで、IPアドレスを持たない。
データを保持している特定のポッドだけにアクセスしたいケースで有用

service-headless.yaml (抜粋)
```
spec:
  clusterIP: None  # ヘッドレス（IPアドレスなしを指定）
  ports:
    - port: 9100
  selector:
    apg: my-grp1   # この2つのラベルと一致するポッドへ転送
    app: my-pod
```


最初にポッドをデプロイ
```
$ kubectl apply -f my-pod.yaml 
```

ヘッドレスのサービスをデプロイします
```
$ kubectl apply -f service-headless.yaml 
```

ポッドのIPアドレスを確認しておきます
```
$ kubectl get po -o wide
NAME    READY  STATUS   RESTARTS   AGE   IP           NODE
my-pod  1/1    Running  0          82s   10.244.0.5   minikube
```

サービスをリストする
```
$ kubectl get svc my-service-hl
NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
my-service-hl   ClusterIP   None         <none>        9100/TCP   22s
```

## ヘッドレスのサービスの動作確認

対話型でポッドを起動
```
$ kubectl run -it my-pod3 --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
```

サービス名が内部DNSへ登録されたこと、ポッドのIPアドレスがセットされていることを確認
```
nobody@my-pod3:/$ nslookup  
> my-service-hl
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   my-service-hl.default.svc.cluster.local
Address: 10.244.0.5
```

ヘッドレスのサービス名が、環境変数にセットされていないこと確認
```
nobody@my-pod3:/$ env |grep MY_SERVICE
nobody@my-pod3:/$ 
```

DNS名でアクセスできることを確認
```
nobody@my-pod3:/$ curl http://my-service-hl.default.svc.cluster.local:9100/ping;echo
PONG!

```

## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip
