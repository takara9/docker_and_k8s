# ノードポート
Kubernetesクラスタのノードにポットへアクセスするためのポートを開きます。
このノードのポートを通じて、ポッドのサービスへアクセスできます。
ノードに開くポートへアクセスすると、サービスのラベルにマッチする全ポッドへランダムに割り振られます。

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

## 実行例
ノードポートへ minikube service を介して接続する。
```
$ minikube version
minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff

$ minikube service mypods --url
http://127.0.0.1:56402
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。
```

ターミナルをもう一つ開いて、ノードポートで開いたポッドへアクセスする。
```
$ curl http://127.0.0.1:56402/ping;echo
PONG!

$ curl http://127.0.0.1:56402/info
Host Name: mypods-5766dfdb7f-wjzkb
Host IP: 10.244.0.3
Client IP : 10.244.0.1
```


## 失敗ケース

チップが Apple M2 で minikube version: v1.32.0　のケースでは、以下のエラーが NodePortが使えませんでした。
```
mini:docker_and_k8s takara$ minikube version
minikube version: v1.32.0
commit: 8220a6eb95f0a4d75f7f2d7b14cef975f050512d
$ minikube service mypods --url

❌  MK_UNIMPLEMENTED が原因で終了します: minikube service is not currently implemented with the builtin network on QEMU, try starting minikube with '--network=socket_vmnet'
```

Windows11 の minikube でも実装以下のエラーにより ノードポートへトンネルできませんでした。
```
PS C:\Users\tkr99\docker_and_k8s> minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff
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

```



## クリーンナップ
```
minikube delete
```


## 参照資料
- https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
- https://minikube.sigs.k8s.io/docs/handbook/accessing/
- https://minikube.sigs.k8s.io/docs/commands/service/

