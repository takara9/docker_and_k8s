# サービスの役割
サービスは、ポッドにリクエストを届けるためのオブジェクトです。
ポッドは揮発性の性質を補うものとして、IPアドレスの永続化やDNSへの登録を担う役目もあります。


## 準備
minikube は、明示的に指定しなければ、dockerコンテナでkubernetesノードを再現します。そのため、docker desktopが起動していなければ、minikube をスタートできません。
起動に失敗する場合は、一度、「minikube delete --all=true」を実行してから、「minikube start --nodes=3」を実行してみてください。
```
$ minikube start --nodes=3
$ minikube status
$ kubectl get no
```


## ポッドとサービスの起動
対話型ポッドを作成する。
```
$ kubectl run -it my-pod --image=ubuntu:latest -- bash
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


簡単なアプリケーションを、マニフェストを使って起動する。
```
$ tree .
.
├── README.md
└── manifest
    ├── pod.yaml
    └── service.yaml

$ kubectl apply -f manifest-1
pod/my-pod created
service/my-service created

$ kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          5h40m
my-service   NodePort    10.111.174.215   <none>        9100:30386/TCP   17s

$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          22s
```

```
$ minikube ip
192.168.66.18

$ curl http://192.168.66.18:30386/ping;echo
<p>pong</p>
```


## ラベル　の使い方1

ラベルを指定しなければ、全てのオブジェクトが表示される。
```
maho-2:4.1 maho$ kubectl get all
NAME         READY   STATUS    RESTARTS   AGE
pod/my-pod   1/1     Running   0          59s

NAME                 TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP        3h42m
service/my-service   NodePort    10.102.238.213   <none>        80:30864/TCP   59s
```

ラベル「app=my-app-1」を指定して、該当するものだけをリストする。
```
maho-2:4.1 maho$ kubectl get all -l app=my-app-1
NAME         READY   STATUS    RESTARTS   AGE
pod/my-pod   1/1     Running   0          63s

NAME                 TYPE       CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
service/my-service   NodePort   10.102.238.213   <none>        80:30864/TCP   63s
```


## パッチを当てて、サービスを切り替え

```
$ kubectl apply -f pod.yaml
```



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






複数コンテナをポッドで動かす
リソース確保と制限

