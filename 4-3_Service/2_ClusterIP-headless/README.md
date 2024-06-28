# ClusterIP Headless
代表IPアドレスを持たない「サービス」で、一度アクセスしたポッドへ継続的にアクセスするのに便利な「サービス」です。


## 準備
```
$ minikube start
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


ヘッドレスサービスのデプロイ
```
$ kubectl apply -f my-pod.yaml 
$ kubectl apply -f service-headless.yaml 
$ kubectl get po -o wide
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-pod   1/1     Running   0          18s   10.244.0.3   minikube   <none>           <none>

$ kubectl get svc my-service-hl
NAME            TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
my-service-hl   ClusterIP   None         <none>        9100/TCP   21s
```

ヘッドレスサービスのオブジェクトの動作確認
```
$ kubectl run -it my-pod3 --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.

nobody@my-pod3:/$ nslookup my-service-hl
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   my-service-hl.default.svc.cluster.local
Address: 10.244.0.3

nobody@my-pod3:/$ env |grep MY_SERVICE
nobody@my-pod3:/$ 

nobody@my-pod3:/$ curl my-service-hl:9100/ping;echo
PONG!
```



## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip
