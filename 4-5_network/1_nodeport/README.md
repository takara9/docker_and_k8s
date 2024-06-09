# ノードポート

## 準備

失敗例 
```
$ minikube start
$ kubectl create deployment mypods --image=ghcr.io/takara9/ex1:1.5
$ kubectl expose deployment mypods --type=NodePort --port=9100
$ kubectl get svc mypods


チップが Apple M2 で minikube version: v1.32.0　のケースでは、以下のエラーが NodePortが使えませんでした。
```
$ minikube service mypods --url

❌  MK_UNIMPLEMENTED が原因で終了します: minikube service is not currently implemented with the builtin network on QEMU, try starting minikube with '--network=socket_vmnet'

```




```
$ kubectl apply -f deployment.yaml 
$ kubectl apply -f sevice-np.yaml 
$ kubectl get svc
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          61s
rest-service-np   NodePort    10.109.193.255   <none>        9100:31256/TCP   15s
```


```
$ minikube service rest-service-np --url
http://127.0.0.1:59566
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。
```



```
http://127.0.0.1:59566/info
Host Name: my-pods-7dc8dfd5c9-9g45b Host IP: 10.244.0.4 Client IP : 10.244.0.1

mini:docker_and_k8s takara$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-7dc8dfd5c9-9g45b   1/1     Running   0          2m23s
my-pods-7dc8dfd5c9-9pvk2   1/1     Running   0          2m23s
my-pods-7dc8dfd5c9-z4qqv   1/1     Running   0          2m23s

際読み込みで、複数のポッドが出てくるので、分散されている事がわかる。
```



## クリーンナップ
```
minikube delete
```


## 参照資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
- https://minikube.sigs.k8s.io/docs/handbook/accessing/


