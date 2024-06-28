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

別ポッドで、DNSでサービス名から、IPアドレスを引く
```
$ kubectl run -it mypod2 --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.

nobody@mypod2:/$ nslookup my-service
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   my-service.default.svc.cluster.local
Address: 10.109.31.118

root@mypod2:/$ dig my-service.default.svc.cluster.local +short
10.100.2.115
```

ポッドの環境変数で、サービスの存在やIPアドレスなどがセットされる
```
root@mypod2:/$ env |grep MY_SERVICE
MY_SERVICE_SERVICE_HOST=10.100.2.115
MY_SERVICE_PORT=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP=tcp://10.100.2.115:9100
MY_SERVICE_PORT_9100_TCP_PROTO=tcp
MY_SERVICE_PORT_9100_TCP_ADDR=10.100.2.115
MY_SERVICE_SERVICE_PORT=9100
MY_SERVICE_PORT_9100_TCP_PORT=9100
```

同じネームスペースから、サービス名でポッドをアクセス
```
nobody@mypod2:/$ curl http://my-service:9100/ping;echo
<p>pong</p>
```

サービスは、ポッドのラベルで、転送先を決定
```
mini:2_ClusterIP takara$ kubectl get pod my-pod --show-labels
NAME     READY   STATUS    RESTARTS   AGE     LABELS
my-pod   1/1     Running   0          7m32s   run=my-pod
```


サービスのYAMLを表示、セレクターに対象ポッドのラベル名がセットされている
```
$ kubectl get svc my-service -o yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2024-06-24T21:06:32Z"
  labels:
    run: my-pod
  name: my-service
  namespace: default
  resourceVersion: "486"
  uid: fdf74e53-32d9-432e-ad5e-a93f0e7c8f2b
spec:
  clusterIP: 10.109.31.118
  clusterIPs:
  - 10.109.31.118
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 9100
    protocol: TCP
    targetPort: 9100
  selector:
    run: my-pod             # セレクターのラベル
  sessionAffinity: None
  type: ClusterIP
```

## クリーンナップ

```
root@mypod2:/$ exit
$ kubectl delete pod my-pod
$ kubectl delete svc my-service
```

```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-clusterip
