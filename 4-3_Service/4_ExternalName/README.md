# サービス ロードバランサー

K8sクラスタの外部のDNS名を、K8sクラスタ内部のDNSへ登録します。

## 準備

```
$ minikube start
$ kubectl get no
```

## 実行例

```
$ kubectl apply -f service-externalname.yaml 
$ kubectl get -f service-externalname.yaml 
NAME         TYPE           CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
my-service   ExternalName   <none>       ifconfig.io   <none>    15s
```

```
$ curl -H 'Host:ifconfig.io'  http://my-service
60.132.118.230
```

## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/service/#externalname



