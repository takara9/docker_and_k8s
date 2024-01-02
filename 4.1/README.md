
# 4.1 ポッドとサービス

## minikubeの開始

```
maho-2:~ maho$ minikube start --nodes=3
😄  Darwin 14.0 上の minikube v1.32.0
✨  ユーザーの設定に基づいて hyperkit ドライバーを使用します
👍  minikube クラスター中のコントロールプレーンの minikube ノードを起動しています
🔥  hyperkit VM (CPUs=2, Memory=2700MB, Disk=20000MB) を作成しています...
🐳  Docker 24.0.7 で Kubernetes v1.28.3 を準備しています...
    ▪ 証明書と鍵を作成しています...
    ▪ コントロールプレーンを起動しています...
    ▪ RBAC のルールを設定中です...
🔗  CNI (コンテナーネットワークインターフェース) を設定中です...
🔎  Kubernetes コンポーネントを検証しています...
    ▪ gcr.io/k8s-minikube/storage-provisioner:v5 イメージを使用しています
🌟  有効なアドオン: default-storageclass, storage-provisioner

👍  minikube クラスター中の minikube-m02 ワーカーノードを起動しています
🔥  hyperkit VM (CPUs=2, Memory=2700MB, Disk=20000MB) を作成しています...
🌐  ネットワークオプションが見つかりました:
    ▪ NO_PROXY=192.168.66.18
🐳  Docker 24.0.7 で Kubernetes v1.28.3 を準備しています...
    ▪ env NO_PROXY=192.168.66.18
🔎  Kubernetes コンポーネントを検証しています...

👍  minikube クラスター中の minikube-m03 ワーカーノードを起動しています
🔥  hyperkit VM (CPUs=2, Memory=2700MB, Disk=20000MB) を作成しています...
🌐  ネットワークオプションが見つかりました:
    ▪ NO_PROXY=192.168.66.18,192.168.66.19
🐳  Docker 24.0.7 で Kubernetes v1.28.3 を準備しています...
    ▪ env NO_PROXY=192.168.66.18
    ▪ env NO_PROXY=192.168.66.18,192.168.66.19
🔎  Kubernetes コンポーネントを検証しています...
🏄  終了しました！kubectl がデフォルトで「minikube」クラスターと「default」ネームスペースを使用するよう設定されました
```


## クラスタの状態確認

```
maho-2:~ maho$ minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured

minikube-m02
type: Worker
host: Running
kubelet: Running

minikube-m03
type: Worker
host: Running
kubelet: Running
```

## Kubernetes Dashboradの開始

```
minikube addons enable metrics-server
maho-2:~ maho$ minikube dashboard
🤔  ダッシュボードの状態を検証しています...
🚀  プロキシーを起動しています...
🤔  プロキシーの状態を検証しています...
🎉  デフォルトブラウザーで http://127.0.0.1:65532/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/ を開いています...
```

ダッシュボードの準備

```
$ minikube addons enable metrics-server
💡  metrics-server is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ registry.k8s.io/metrics-server/metrics-server:v0.6.4 イメージを使用しています
🌟  'metrics-server' アドオンが有効です
```



## Kubernetesクラスタを構成するノードの様子

```
maho-2:~ maho$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   4m36s   v1.28.3
minikube-m02   Ready    <none>          4m10s   v1.28.3
minikube-m03   Ready    <none>          3m50s   v1.28.3
```



## ポッドとサービスの起動

対話型ポッドを作成する。

```
maho-2:~ maho$ kubectl run -it my-pod --image=ubuntu:latest -- bash
If you don't see a command prompt, try pressing enter.
root@my-pod:/# ps -ax
    PID TTY      STAT   TIME COMMAND
      1 pts/0    Ss     0:00 bash
      9 pts/0    R+     0:00 ps -ax
root@my-pod:/# whoami
root
```

もう一つのターミナルで様子を見る

```
maho-2:~ maho$ kubectl get po -o wide
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pod   1/1     Running   0          73s   10.244.2.2   minikube-m03   <none>           <none>
```


## 簡単なアプリケーションを、マニフェストを使って起動する。

$ tree .
.
├── README.md
└── manifest
    ├── pod.yaml
    └── service.yaml


maho-2:4.1 maho$ kubectl apply -f manifest-1
pod/my-pod created
service/my-service created


$ kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          5h40m
my-service   NodePort    10.111.174.215   <none>        9100:30386/TCP   17s

$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          22s

maho-2:4.1 maho$ minikube ip
192.168.66.18

$ curl http://192.168.66.18:30386/ping;echo
<p>pong</p>


## ラベル　の使い方1

ラベル指定なし

maho-2:4.1 maho$ kubectl get all
NAME         READY   STATUS    RESTARTS   AGE
pod/my-pod   1/1     Running   0          59s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        3h42m
service/my-service   NodePort    10.102.238.213   <none>        80:30864/TCP   59s



maho-2:4.1 maho$ kubectl get all -l app=my-app-1
NAME         READY   STATUS    RESTARTS   AGE
pod/my-pod   1/1     Running   0          63s

NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/my-service   NodePort   10.102.238.213   <none>        80:30864/TCP   63s


## パッチを当てて、サービスを切り替え

$ cd manifest-2
$ kubectl apply -f pod.yaml
pod/my-pod2 created

$ kubectl get po
NAME      READY   STATUS    RESTARTS   AGE
my-pod    1/1     Running   0          99m
my-pod2   1/1     Running   0          2m14s

$ kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        5h21m
my-service   NodePort    10.102.238.213   <none>        80:30864/TCP   100m


$ curl http://192.168.66.18:30864/ping;echo
<p>pong</p>




maho-2:4.1 maho$ kubectl apply -f pod.yaml 
pod/my-pod2 created
maho-2:4.1 maho$ kubectl get po -l app=my-app-1
NAME      READY   STATUS    RESTARTS   AGE
my-pod    1/1     Running   0          2m19s
my-pod2   1/1     Running   0          43s


## portford による確認

maho-2:~ maho$ kubectl port-forward my-pod2 9800:9100
Forwarding from 127.0.0.1:9800 -> 9100
Forwarding from [::1]:9800 -> 9100
Handling connection for 9800

maho-2:4.1 maho$ curl http://localhost:9800/ping;echo
PONG!


## パッチによる振り分け先変更

$ kubectl patch svc my-service --patch-file patch.yaml
service/my-service patched

$ curl http://192.168.66.18:30386/ping;echo
PONG!


## サービスアカウント
ポッドは、サービスアカウントの権限で実行する。サービスアカウントは、デフォルトを利用する。

## Pod Security Admission

ネームスペースに割り当てられるセキュリティ標準
自分の担当するアプリケーションのネームスペースに、設定がある時は、従わないとデプロイできない。
デプロイするコンテナが、特権を利用しているなど、違反するコンテナは動作できない。

psa/ns.yaml 違反したポッドは起動できないネームスペースを作成する
pod-1.yaml SecurityContext を細かく指定したポッド
pod-2.yaml 指定したが、内部で特権モードを利用するポッドは起動できない
pod-3.yaml ルート権限を使用しないNginx



## ライブネスプローブとレディネスプローブ


