# ノードポート

## 準備
注意点として、Apple M2 mac, Windows 11 の場合、利用できないことがある様です。

```
$ minikube start
$ kubectl create deployment mypods --image=ghcr.io/takara9/ex1:1.5
$ kubectl expose deployment mypods --type=NodePort --port=9100
$ kubectl get svc mypods
NAME     TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
mypods   NodePort   10.104.42.127   <none>        9100:32429/TCP   8s
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


## 失敗ケース

チップが Apple M2 で minikube version: v1.32.0　のケースでは、以下のエラーが NodePortが使えませんでした。
```
$ minikube service mypods --url

❌  MK_UNIMPLEMENTED が原因で終了します: minikube service is not currently implemented with the builtin network on QEMU, try starting minikube with '--network=socket_vmnet'

```

Windows11 の minikube でも実装以下のエラーにより ノードポートへトンネルできませんでした。
```
PS C:\Users\tkr99\docker_and_k8s> minikube service mypods --url
W0609 14:06:34.730347    2580 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\tkr99\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.

❌  Exiting due to SVC_UNREACHABLE: service not available: no running pod for service mypods found

╭───────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                           │
│    😿  If the above advice does not help, please let us know:                                             │
│    👉  https://github.com/kubernetes/minikube/issues/new/choose                                           │
│                                                                                                           │
│    Please run `minikube logs --file=logs.txt` and attach logs.txt to the GitHub issue.                    │
│    Please also attach the following file to the GitHub issue:                                             │
│    - C:\Users\tkr99\AppData\Local\Temp\minikube_service_d7bb74d21a24a432745e209c18039dda67202648_0.log    │
│                                                                                                           │
╰───────────────────────────────────────────────────────────────────────────────────────────────────────────╯

PS C:\Users\tkr99\docker_and_k8s> minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff
```






## クリーンナップ
```
minikube delete
```

## 参照資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
- https://minikube.sigs.k8s.io/docs/handbook/accessing/


