# ノードポート

## 準備
注意点として、Apple Sillicon のプロセッサーの場合、実装が遅れていて利用できないことがある様です。

```
$ minikube start
$ kubectl create deployment mypods --image=ghcr.io/takara9/ex1:1.5
$ kubectl expose deployment mypods --type=NodePort --port=9100
$ kubectl get svc mypods
NAME     TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
mypods   NodePort   10.104.42.127   <none>        9100:32429/TCP   8s
```


チップが Apple M2 で minikube version: v1.32.0　のケースでは、以下のエラーが NodePortが使えませんでした。
```
$ minikube service mypods --url

❌  MK_UNIMPLEMENTED が原因で終了します: minikube service is not currently implemented with the builtin network on QEMU, try starting minikube with '--network=socket_vmnet'

```

Intelプロセッサーを使用する MacBook Proでは、以下のとおり、ノードポートへトンネルすることができました。
```
$  minikube service mypods --url
http://192.168.101.2:32429

$ curl http://192.168.101.2:32429/ping;echo
PONG!

$ curl http://192.168.101.2:32429/info
Host Name: mypods-5766dfdb7f-4wj6q
Host IP: 10.244.0.2
Client IP : 10.244.0.1
```

## クリーンナップ
```
minikube delete
```

## 参照資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
- https://minikube.sigs.k8s.io/docs/handbook/accessing/


