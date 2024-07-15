# デプロイメント　(Deployment)
Webアプリケーションサーバーなど、永続的なデータを持たない、ワークロードのポッドの管理に適します。


## 準備

```
$ minikube start
```


## デプロイメントの配置とポッドの起動

```
$ kubectl apply -f deployment-1.yaml 
$ kubectl get deployment
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   3/3     3            3           69s
$ kubectl get po
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-86d8b964d7-5gj9l   1/1     Running   0          79s
my-pods-86d8b964d7-nfsj4   1/1     Running   0          79s
my-pods-86d8b964d7-vhx4c   1/1     Running   0          79s
```

サービスの配置
```
$ kubectl apply -f service.yaml 
$ kubectl get svc my-pods
NAME      TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
my-pods   ClusterIP   10.96.248.147   <none>        9100/TCP   9s
```

DNS名でアクセス
```
$ kubectl run -it mypod --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
root@bash:/# curl http://my-pods:9100/ping;echo
<p>pong</p>
```


## 自己回復機能

ポッドの一つを削除しても、すぐに自己回復して、ポッド数を維持する
```
$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-86d8b964d7-lt7p4   1/1     Running   0          107s
my-pods-86d8b964d7-xpc8h   1/1     Running   0          107s
my-pods-86d8b964d7-zgpdq   1/1     Running   0          107s

$ kubectl get deploy 
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   3/3     3            3           109s

$ kubectl delete pod my-pods-86d8b964d7-lt7p4
pod "my-pods-86d8b964d7-lt7p4" deleted

$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-86d8b964d7-5wxnz   1/1     Running   0          37s
my-pods-86d8b964d7-xpc8h   1/1     Running   0          2m43s
my-pods-86d8b964d7-zgpdq   1/1     Running   0          2m43s
```


## ローリングアップデート

初期状態
```
$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-86d8b964d7-gwchs   1/1     Running   0          21s
my-pods-86d8b964d7-pkxrk   1/1     Running   0          21s
my-pods-86d8b964d7-t6bwk   1/1     Running   0          21s

$ kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
my-pods-86d8b964d7-gwchs        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-pkxrk        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-t6bwk        ghcr.io/takara9/ex1:1.0
```

コンテナのバージョンを変えたYAMLを適用
```
$ kubectl apply -f deployment-2.yaml 
$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-5757fc766f-84s78   1/1     Running       0          14s
my-pods-5757fc766f-gqz8r   1/1     Running       0          13s
my-pods-5757fc766f-lj9h7   1/1     Running       0          26s
my-pods-86d8b964d7-gwchs   1/1     Terminating   0          78s
my-pods-86d8b964d7-pkxrk   1/1     Terminating   0          78s
my-pods-86d8b964d7-t6bwk   1/1     Terminating   0          78s

$ kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
my-pods-5757fc766f-84s78        ghcr.io/takara9/ex1:1.5
my-pods-5757fc766f-gqz8r        ghcr.io/takara9/ex1:1.5
my-pods-5757fc766f-lj9h7        ghcr.io/takara9/ex1:1.5
my-pods-86d8b964d7-gwchs        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-pkxrk        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-t6bwk        ghcr.io/takara9/ex1:1.0
```

最終到達した状態
```
$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-5757fc766f-84s78   1/1     Running   0          42s
my-pods-5757fc766f-gqz8r   1/1     Running   0          41s
my-pods-5757fc766f-lj9h7   1/1     Running   0          54s
$ kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
my-pods-5757fc766f-84s78        ghcr.io/takara9/ex1:1.5
my-pods-5757fc766f-gqz8r        ghcr.io/takara9/ex1:1.5
my-pods-5757fc766f-lj9h7        ghcr.io/takara9/ex1:1.5
```


## ロールバック

ロールアウトの履歴を表示
```
$ kubectl rollout history deployment/my-pods
deployment.apps/my-pods 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

$ kubectl rollout history deployment/my-pods --revision=1
deployment.apps/my-pods with revision #1
Pod Template:
  Labels:       app=my-pod
        pod-template-hash=86d8b964d7
  Containers:
   ex1-pod:
    Image:      ghcr.io/takara9/ex1:1.0
    Port:       9100/TCP
    Host Port:  0/TCP
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>

$ kubectl rollout history deployment/my-pods --revision=2
deployment.apps/my-pods with revision #2
Pod Template:
  Labels:       app=my-pod
        pod-template-hash=5757fc766f
  Containers:
   ex2-pod:
    Image:      ghcr.io/takara9/ex1:1.5
    Port:       9100/TCP
    Host Port:  0/TCP
    Environment:        <none>
    Mounts:     <none>
  Volumes:      <none>
```

ロールバック実行
```
$ kubectl rollout undo deployment/my-pods
deployment.apps/my-pods rolled back

$ kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
my-pods-86d8b964d7-fmpdf        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-grh56        ghcr.io/takara9/ex1:1.0
my-pods-86d8b964d7-xkhjz        ghcr.io/takara9/ex1:1.0

$ kubectl rollout history deployment/my-pods
deployment.apps/my-pods 
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
```

指定レビジョンへ戻す
```
$ kubectl rollout history deployment/my-pods --to-revision=2
```


## デプロイメントのリスタート
デプロイメント管理下のポッドの再スタート

```
$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-5757fc766f-8nsqq   1/1     Running   0          61m
my-pods-5757fc766f-hhr66   1/1     Running   0          61m
my-pods-5757fc766f-jm84h   1/1     Running   0          61m

$ kubectl rollout restart deployment/my-pods
deployment.apps/my-pods restarted

$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS              RESTARTS   AGE
my-pods-5757fc766f-8nsqq   1/1     Running             0          62m
my-pods-5757fc766f-hhr66   1/1     Terminating         0          62m
my-pods-5757fc766f-jm84h   1/1     Terminating         0          62m
my-pods-5bfd65968d-4482v   0/1     ContainerCreating   0          0s
my-pods-5bfd65968d-nd6jm   1/1     Running             0          2s
my-pods-5bfd65968d-npr9x   1/1     Running             0          1s

$ kubectl get pod -l app=my-pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-5bfd65968d-4482v   1/1     Running   0          23s
my-pods-5bfd65968d-nd6jm   1/1     Running   0          25s
my-pods-5bfd65968d-npr9x   1/1     Running   0          24s
```



```
$ kubectl get deploy my-pods -o yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  ＜中略＞
spec:
  progressDeadlineSeconds: 600  # デプロイメントが失敗したと判定するまでの最大時間 (秒)
  replicas: 3                   # ポッド数（必須）
  revisionHistoryLimit: 10      # ロールバックできる世代数
  selector:                     # 管理対象のポッド選別するためのセレクター（必須）
    matchLabels:
      app: my-pod
  strategy:              # 既存のポッドを新しいポッドに置き換える戦略
    rollingUpdate:         # ローリングアップデートのパラメータ     
      maxSurge: 25%          # デフォルトは25%、新旧ポッドの合計が要求数の100%+30%
      maxUnavailable: 25%    # 更新中に使用できない最大ポッド数、デフォルトは25%、要求数10では20%
    type: RollingUpdate    # "Recreate" または "RollingUpdate"
  template:              # 起動するポッドのテンプレート
    metadata:
      labels:
        app: my-pod
    spec:                # ポッドのスペック
      containers:
　　＜中略＞
status:
　＜以下省略＞
```




## クリーンナップ
```
$ minikube delete
```


## 参考資料
- デプロイメント https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
- デプロイメントAPIリファレンス https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/
- 自動生成 APIリファレンス https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#deployment-v1-apps
- JSONPATH https://kubernetes.io/docs/reference/kubectl/jsonpath/
- kubectlコマンドリファレンス deployment https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-deployment-em-
- kubectlコマンドリファレンス rollout https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout
