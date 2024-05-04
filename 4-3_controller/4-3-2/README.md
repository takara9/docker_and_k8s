# Deployments


https://kubernetes.io/ja/docs/concepts/workloads/controllers/deployment/




~~~
apiVersion: apps/v1
kind: Deployment               #(1) デプロイメントのAPIを指定
metadata:
  name: my-pods                #(2) 名前（必須）
 spec:                         #(3) デプロイメントのスペック
  progressDeadlineSeconds: 600 #(3) デプロイメントが失敗したと判定すまでの最大時間 (秒)
  replicas: 2                  #(4) ポッド数（必須）
  revisionHistoryLimit: 10     #(5) ロールバックできる世代数
  selector:                    #(6) 管理対象のポッド選別するためのセレクター（必須） 
    matchLabels:
      app: my-pod
  strategy:                 #(7) 既存のポッドを新しいポッドに置き換える戦略
    type: RollingUpdate     #(8) "Recreate" または "RollingUpdate"
    rollingUpdate:          #(9) ローリングアップデートのパラメータ
      maxSurge: 25%         #(10) デフォルトは25%、新旧ポッドの合計が要求数の100%+30%(端数は四捨五入)を超えない様に制御   
      maxUnavailable: 25%   #(11) 更新中に使用できない最大ポッド数、デフォルトは25%、要求数10では20%
  template:            #(12) ポッドのテンプレート、ここから下はポッドのAPIを記述（必須）
    metadata:　　　　　　#(13) メタデータはラベルなどを記述、名前はコントローラーから与えられる
      labels:          #(14) コントローラーとポッドを関連づけるラベル、他と重複しない様に注意（必須）
        app: my-pod
    spec:              #(15) ポッドスペック（必須）
      containers:
      <以下省略>
~~~

~~~
minikube start
~~~

~~~
$ kubectl apply -f deployment.yaml 
deployment.apps/my-pods created
~~~

~~~
$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-bp224   1/1     Running   0          7s
my-pods-cc78567c8-bvh6p   1/1     Running   0          7s
my-pods-cc78567c8-r59dz   1/1     Running   0          7s
~~~

~~~
$ kubectl apply -f service.yaml 
service/my-pods created
~~~

~~~
$ kubectl get svc
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP    18m
my-pods      ClusterIP   10.106.8.142   <none>        9100/TCP   6s
~~~


~~~
$ kubectl run -it --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash
If you don't see a command prompt, try pressing enter.
root@bash:/# curl http://my-pods:9100/ping;echo
<p>pong</p>
~~~

kubectl apply -f deployment.yaml 
kubectl get deployment
kubectl get rs
kubectl get pod
kubectl delete pod 
kubectl get pod



~~~
$ kubectl apply -f deployment.yaml 
deployment.apps/my-pods created

#(1)デプロイメントで起動するポッド数を確認
$ kubectl get deploy
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   3/3     3            3           17s

#(2)レプリカセットで起動するポッド数を確認
$ kubectl get rs
NAME                DESIRED   CURRENT   READY   AGE
my-pods-cc78567c8   3         3         3       27s

#(3)ポッドの起動状態を確認
$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-6xf79   1/1     Running   0          37s
my-pods-cc78567c8-8ndmt   1/1     Running   0          37s
my-pods-cc78567c8-nw7rp   1/1     Running   0          37s
~~~


~~~
#(4)ポッドの一つを削除
$ kubectl delete po my-pods-cc78567c8-6xf79
pod "my-pods-cc78567c8-6xf79" deleted

#(5)ポッド数の回復を確認
$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-8ndmt   1/1     Running   0          87s
my-pods-cc78567c8-l85kc   1/1     Running   0          35s
my-pods-cc78567c8-nw7rp   1/1     Running   0          87s
~~~


kubectl apply -f deployment-10.yaml 
kubectl get deployment -o wide
kubectl get po
kubectl apply -f deployment-10-ex3.yaml 
kubectl get po
kubectl get deployment -o wide
kubectl rollout history deployment/my-pods
kubectl rollout undo deployment/my-pods

kubectl apply -f deployment-2-ex3.yaml 


~~~
$ kubectl apply -f deployment-10.yaml 
deployment.apps/my-pods configured

$ kubectl get po
NAME                      READY   STATUS    RESTARTS        AGE
my-pods-cc78567c8-7s8sc   1/1     Running   0               2s
my-pods-cc78567c8-bvh6p   1/1     Running   0               6m20s
my-pods-cc78567c8-cftlq   1/1     Running   0               2s
my-pods-cc78567c8-h5lk6   1/1     Running   0               2s
my-pods-cc78567c8-h6f59   1/1     Running   0               2skubectl get po
my-pods-cc78567c8-jl4xf   1/1     Running   0               2s
my-pods-cc78567c8-lnjgx   1/1     Running   0               2s
my-pods-cc78567c8-r59dz   1/1     Running   0               6m20s
my-pods-cc78567c8-vb777   1/1     Running   0               2m40s
my-pods-cc78567c8-zflbf   1/1     Running   0               2s
~~~



~~~
$ kubectl apply -f deployment-10-ex2.yaml 
deployment.apps/my-pods configured

$ kubectl get po
NAME                       READY   STATUS              RESTARTS      AGE
my-pods-58fdf5c854-46hsk   0/1     ContainerCreating   0             2s
my-pods-58fdf5c854-fzdnc   0/1     ContainerCreating   0             2s
my-pods-58fdf5c854-hwksb   0/1     ContainerCreating   0             2s
my-pods-58fdf5c854-qhbjg   0/1     ContainerCreating   0             2s
my-pods-58fdf5c854-xd8hv   0/1     ContainerCreating   0             2s
my-pods-cc78567c8-bvh6p    1/1     Running             0             33m
my-pods-cc78567c8-cftlq    1/1     Running             0             27m
my-pods-cc78567c8-h5lk6    1/1     Running             0             27m
my-pods-cc78567c8-jl4xf    1/1     Running             0             27m
my-pods-cc78567c8-lnjgx    1/1     Running             0             27m
my-pods-cc78567c8-r59dz    1/1     Running             0             33m
my-pods-cc78567c8-vb777    1/1     Running             0             29m
my-pods-cc78567c8-zflbf    1/1     Running             0             27m

$ kubectl get po
NAME                       READY   STATUS              RESTARTS      AGE
my-pods-58fdf5c854-26dnm   1/1     Running             0             1s
my-pods-58fdf5c854-46hsk   1/1     Running             0             9s
my-pods-58fdf5c854-fzdnc   0/1     ContainerCreating   0             9s
my-pods-58fdf5c854-hwksb   1/1     Running             0             9s
my-pods-58fdf5c854-l5d9m   0/1     ContainerCreating   0             0s
my-pods-58fdf5c854-ml9qn   1/1     Running             0             1s
my-pods-58fdf5c854-qhbjg   1/1     Running             0             9s
my-pods-58fdf5c854-qvv4c   1/1     Running             0             2s
my-pods-58fdf5c854-scwq2   0/1     ContainerCreating   0             0s
my-pods-58fdf5c854-xd8hv   1/1     Running             0             9s
my-pods-cc78567c8-bvh6p    1/1     Terminating         0             33m
my-pods-cc78567c8-cftlq    1/1     Terminating         0             27m
my-pods-cc78567c8-h5lk6    1/1     Terminating         0             27m
my-pods-cc78567c8-jl4xf    1/1     Running             0             27m
my-pods-cc78567c8-lnjgx    1/1     Terminating         0             27m
my-pods-cc78567c8-r59dz    1/1     Terminating         0             33m
my-pods-cc78567c8-vb777    1/1     Terminating         0             29m
my-pods-cc78567c8-zflbf    1/1     Terminating         0             27m

$ kubectl get po
NAME                       READY   STATUS    RESTARTS      AGE
my-pods-58fdf5c854-26dnm   1/1     Running   0             89s
my-pods-58fdf5c854-46hsk   1/1     Running   0             97s
my-pods-58fdf5c854-fzdnc   1/1     Running   0             97s
my-pods-58fdf5c854-hwksb   1/1     Running   0             97s
my-pods-58fdf5c854-l5d9m   1/1     Running   0             88s
my-pods-58fdf5c854-ml9qn   1/1     Running   0             89s
my-pods-58fdf5c854-qhbjg   1/1     Running   0             97s
my-pods-58fdf5c854-qvv4c   1/1     Running   0             90s
my-pods-58fdf5c854-scwq2   1/1     Running   0             88s
my-pods-58fdf5c854-xd8hv   1/1     Running   0             97s
~~~


~~~
$ kubectl apply -f deployment-2-ex3.yaml 
deployment.apps/my-pods configured

$ kubectl get po
NAME                       READY   STATUS        RESTARTS      AGE
my-pods-58fdf5c854-26dnm   1/1     Terminating   0             101s
my-pods-58fdf5c854-46hsk   1/1     Terminating   0             109s
my-pods-58fdf5c854-fzdnc   1/1     Terminating   0             109s
my-pods-58fdf5c854-hwksb   1/1     Terminating   0             109s
my-pods-58fdf5c854-l5d9m   1/1     Running       0             100s
my-pods-58fdf5c854-ml9qn   1/1     Terminating   0             101s
my-pods-58fdf5c854-qhbjg   1/1     Terminating   0             109s
my-pods-58fdf5c854-qvv4c   1/1     Terminating   0             102s
my-pods-58fdf5c854-scwq2   1/1     Running       0             100s
my-pods-58fdf5c854-xd8hv   1/1     Terminating   0             109s

$ kubectl get po
NAME                       READY   STATUS    RESTARTS      AGE
bash                       1/1     Running   1 (32m ago)   34m
my-pods-58fdf5c854-l5d9m   1/1     Running   0             2m43s
my-pods-58fdf5c854-scwq2   1/1     Running   0             2m43s
~~~




$ minikube delete
🔥  docker の「minikube」を削除しています...
🔥  コンテナー「minikube」を削除しています...
🔥  /Users/takara/.minikube/machines/minikube を削除しています...
💀  クラスター「minikube」の全てのトレースを削除しました。

$ minikube start
😄  Darwin 14.2.1 (arm64) 上の minikube v1.32.0
✨  docker ドライバーが自動的に選択されました。他の選択肢: qemu2, ssh
❗  docker is currently using the overlayfs storage driver, setting preload=false
📌  root 権限を持つ Docker Desktop ドライバーを使用
👍  minikube クラスター中のコントロールプレーンの minikube ノードを起動しています
🚜  ベースイメージを取得しています...
🔥  Creating docker container (CPUs=2, Memory=4000MB) ...
🐳  Docker 24.0.7 で Kubernetes v1.28.3 を準備しています...
    ▪ 証明書と鍵を作成しています...
    ▪ コントロールプレーンを起動しています...
    ▪ RBAC のルールを設定中です...
🔗  bridge CNI (コンテナーネットワークインターフェース) を設定中です...
🔎  Kubernetes コンポーネントを検証しています...
    ▪ gcr.io/k8s-minikube/storage-provisioner:v5 イメージを使用しています
🌟  有効なアドオン: storage-provisioner, default-storageclass
🏄  終了しました！kubectl がデフォルトで「minikube」クラスターと「default」ネームスペースを使用するよう設定されました


$ kubectl apply -f deployment.yaml 
deployment.apps/my-pods created

$ kubectl get deployment
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   0/3     3            0           8s

$ kubectl get pod
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-bfz9w   1/1     Running   0          22s
my-pods-cc78567c8-m4d4v   1/1     Running   0          22s
my-pods-cc78567c8-wwj6w   1/1     Running   0          22s

$ kubectl get deployment
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   3/3     3            3           38s

$ kubectl get rs
NAME                DESIRED   CURRENT   READY   AGE
my-pods-cc78567c8   3         3         3       46s

$ kubectl get pod
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-bfz9w   1/1     Running   0          55s
my-pods-cc78567c8-m4d4v   1/1     Running   0          55s
my-pods-cc78567c8-wwj6w   1/1     Running   0          55s

$ kubectl delete pod my-pods-cc78567c8-bfz9w
pod "my-pods-cc78567c8-bfz9w" deleted

$ kubectl get pod
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-d69cx   1/1     Running   0          35s
my-pods-cc78567c8-m4d4v   1/1     Running   0          106s
my-pods-cc78567c8-wwj6w   1/1     Running   0          106s

$ kubectl apply -f deployment-10.yaml 
deployment.apps/my-pods configured

$ kubectl get deployment -o wide
NAME      READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                    SELECTOR
my-pods   10/10   10           10          2m12s   ex1-pod      ghcr.io/takara9/ex1:1.0   app=my-pod

$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-c85nw   1/1     Running   0          20s
my-pods-cc78567c8-d69cx   1/1     Running   0          73s
my-pods-cc78567c8-gsbkd   1/1     Running   0          20s
my-pods-cc78567c8-hbc76   1/1     Running   0          20s
my-pods-cc78567c8-jqmz4   1/1     Running   0          20s
my-pods-cc78567c8-m4d4v   1/1     Running   0          2m24s
my-pods-cc78567c8-r5lpd   1/1     Running   0          20s
my-pods-cc78567c8-v9qvs   1/1     Running   0          20s
my-pods-cc78567c8-wktl4   1/1     Running   0          20s
my-pods-cc78567c8-wwj6w   1/1     Running   0          2m24s

$ kubectl apply -f deployment-10-ex3.yaml 
deployment.apps/my-pods configured

$ kubectl get po
NAME                       READY   STATUS              RESTARTS   AGE
my-pods-58fdf5c854-7tkt2   0/1     ContainerCreating   0          1s
my-pods-58fdf5c854-chvc5   0/1     ContainerCreating   0          1s
my-pods-58fdf5c854-dspfc   0/1     ContainerCreating   0          1s
my-pods-58fdf5c854-q975f   0/1     ContainerCreating   0          1s
my-pods-58fdf5c854-xfz7s   0/1     ContainerCreating   0          1s
my-pods-cc78567c8-c85nw    1/1     Running             0          30s
my-pods-cc78567c8-d69cx    1/1     Running             0          83s
my-pods-cc78567c8-gsbkd    1/1     Running             0          30s
my-pods-cc78567c8-hbc76    1/1     Running             0          30s
my-pods-cc78567c8-jqmz4    1/1     Running             0          30s
my-pods-cc78567c8-m4d4v    1/1     Running             0          2m34s
my-pods-cc78567c8-r5lpd    1/1     Running             0          30s
my-pods-cc78567c8-v9qvs    1/1     Terminating         0          30s
my-pods-cc78567c8-wktl4    1/1     Terminating         0          30s
my-pods-cc78567c8-wwj6w    1/1     Running             0          2m34s

$ kubectl get po
NAME                       READY   STATUS              RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Running             0          2s
my-pods-58fdf5c854-7tkt2   1/1     Running             0          9s
my-pods-58fdf5c854-btw6f   1/1     Running             0          3s
my-pods-58fdf5c854-chvc5   1/1     Running             0          9s
my-pods-58fdf5c854-dspfc   1/1     Running             0          9s
my-pods-58fdf5c854-q975f   1/1     Running             0          9s
my-pods-58fdf5c854-sr4d4   0/1     ContainerCreating   0          1s
my-pods-58fdf5c854-xfz7s   0/1     ContainerCreating   0          9s
my-pods-58fdf5c854-xhzm2   1/1     Running             0          2s
my-pods-58fdf5c854-zqf7f   1/1     Running             0          2s
my-pods-cc78567c8-c85nw    1/1     Terminating         0          38s
my-pods-cc78567c8-d69cx    1/1     Terminating         0          91s
my-pods-cc78567c8-gsbkd    1/1     Terminating         0          38s
my-pods-cc78567c8-hbc76    1/1     Terminating         0          38s
my-pods-cc78567c8-jqmz4    1/1     Terminating         0          38s
my-pods-cc78567c8-m4d4v    1/1     Terminating         0          2m42s
my-pods-cc78567c8-r5lpd    1/1     Terminating         0          38s
my-pods-cc78567c8-v9qvs    1/1     Terminating         0          38s
my-pods-cc78567c8-wktl4    1/1     Terminating         0          38s
my-pods-cc78567c8-wwj6w    1/1     Terminating         0          2m42s

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Running       0          7s
my-pods-58fdf5c854-7tkt2   1/1     Running       0          14s
my-pods-58fdf5c854-btw6f   1/1     Running       0          8s
my-pods-58fdf5c854-chvc5   1/1     Running       0          14s
my-pods-58fdf5c854-dspfc   1/1     Running       0          14s
my-pods-58fdf5c854-q975f   1/1     Running       0          14s
my-pods-58fdf5c854-sr4d4   1/1     Running       0          6s
my-pods-58fdf5c854-xfz7s   1/1     Running       0          14s
my-pods-58fdf5c854-xhzm2   1/1     Running       0          7s
my-pods-58fdf5c854-zqf7f   1/1     Running       0          7s
my-pods-cc78567c8-c85nw    1/1     Terminating   0          43s
my-pods-cc78567c8-d69cx    1/1     Terminating   0          96s
my-pods-cc78567c8-gsbkd    1/1     Terminating   0          43s
my-pods-cc78567c8-hbc76    1/1     Terminating   0          43s
my-pods-cc78567c8-jqmz4    1/1     Terminating   0          43s
my-pods-cc78567c8-m4d4v    1/1     Terminating   0          2m47s
my-pods-cc78567c8-r5lpd    1/1     Terminating   0          43s
my-pods-cc78567c8-v9qvs    1/1     Terminating   0          43s
my-pods-cc78567c8-wktl4    1/1     Terminating   0          43s
my-pods-cc78567c8-wwj6w    1/1     Terminating   0          2m47s

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Running       0          17s
my-pods-58fdf5c854-7tkt2   1/1     Running       0          24s
my-pods-58fdf5c854-btw6f   1/1     Running       0          18s
my-pods-58fdf5c854-chvc5   1/1     Running       0          24s
my-pods-58fdf5c854-dspfc   1/1     Running       0          24s
my-pods-58fdf5c854-q975f   1/1     Running       0          24s
my-pods-58fdf5c854-sr4d4   1/1     Running       0          16s
my-pods-58fdf5c854-xfz7s   1/1     Running       0          24s
my-pods-58fdf5c854-xhzm2   1/1     Running       0          17s
my-pods-58fdf5c854-zqf7f   1/1     Running       0          17s
my-pods-cc78567c8-c85nw    1/1     Terminating   0          53s
my-pods-cc78567c8-d69cx    1/1     Terminating   0          106s
my-pods-cc78567c8-gsbkd    1/1     Terminating   0          53s
my-pods-cc78567c8-hbc76    1/1     Terminating   0          53s
my-pods-cc78567c8-jqmz4    1/1     Terminating   0          53s
my-pods-cc78567c8-m4d4v    1/1     Terminating   0          2m57s
my-pods-cc78567c8-r5lpd    1/1     Terminating   0          53s
my-pods-cc78567c8-v9qvs    1/1     Terminating   0          53s
my-pods-cc78567c8-wktl4    1/1     Terminating   0          53s
my-pods-cc78567c8-wwj6w    1/1     Terminating   0          2m57s

$ kubectl get po
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Running   0          33s
my-pods-58fdf5c854-7tkt2   1/1     Running   0          40s
my-pods-58fdf5c854-btw6f   1/1     Running   0          34s
my-pods-58fdf5c854-chvc5   1/1     Running   0          40s
my-pods-58fdf5c854-dspfc   1/1     Running   0          40s
my-pods-58fdf5c854-q975f   1/1     Running   0          40s
my-pods-58fdf5c854-sr4d4   1/1     Running   0          32s
my-pods-58fdf5c854-xfz7s   1/1     Running   0          40s
my-pods-58fdf5c854-xhzm2   1/1     Running   0          33s
my-pods-58fdf5c854-zqf7f   1/1     Running   0          33s

$ kubectl get deployment -o wide
NAME      READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS   IMAGES                    SELECTOR
my-pods   10/10   10           10          3m24s   ex2-pod      ghcr.io/takara9/ex3:1.0   app=my-pod

$ kubectl rollout history deployment/my-pods
deployment.apps/my-pods 
REVISION  CHANGE-CAUSE
1         <none>
2         <none>

$ kubectl rollout undo deployment/my-pods
deployment.apps/my-pods rolled back

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Terminating   0          73s
my-pods-58fdf5c854-7tkt2   1/1     Terminating   0          80s
my-pods-58fdf5c854-btw6f   1/1     Terminating   0          74s
my-pods-58fdf5c854-chvc5   1/1     Terminating   0          80s
my-pods-58fdf5c854-dspfc   1/1     Terminating   0          80s
my-pods-58fdf5c854-q975f   1/1     Terminating   0          80s
my-pods-58fdf5c854-sr4d4   1/1     Terminating   0          72s
my-pods-58fdf5c854-xfz7s   1/1     Terminating   0          80s
my-pods-58fdf5c854-xhzm2   1/1     Terminating   0          73s
my-pods-58fdf5c854-zqf7f   1/1     Terminating   0          73s
my-pods-cc78567c8-c2nl8    1/1     Running       0          3s
my-pods-cc78567c8-cwvkw    1/1     Running       0          1s
my-pods-cc78567c8-cxn69    1/1     Running       0          3s
my-pods-cc78567c8-kdfsz    1/1     Running       0          3s
my-pods-cc78567c8-q6dc5    1/1     Running       0          3s
my-pods-cc78567c8-rz6j6    1/1     Running       0          1s
my-pods-cc78567c8-vvtl4    1/1     Running       0          1s
my-pods-cc78567c8-w78rf    1/1     Running       0          1s
my-pods-cc78567c8-wbg22    1/1     Running       0          1s
my-pods-cc78567c8-wj7pq    1/1     Running       0          3s

$ kubectl get deployment -o wide
NAME      READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS   IMAGES                    SELECTOR
my-pods   10/10   10           10          4m    ex1-pod      ghcr.io/takara9/ex1:1.0   app=my-pod

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Terminating   0          88s
my-pods-58fdf5c854-7tkt2   1/1     Terminating   0          95s
my-pods-58fdf5c854-btw6f   1/1     Terminating   0          89s
my-pods-58fdf5c854-chvc5   1/1     Terminating   0          95s
my-pods-58fdf5c854-dspfc   1/1     Terminating   0          95s
my-pods-58fdf5c854-q975f   1/1     Terminating   0          95s
my-pods-58fdf5c854-sr4d4   1/1     Terminating   0          87s
my-pods-58fdf5c854-xfz7s   1/1     Terminating   0          95s
my-pods-58fdf5c854-xhzm2   1/1     Terminating   0          88s
my-pods-58fdf5c854-zqf7f   1/1     Terminating   0          88s
my-pods-cc78567c8-c2nl8    1/1     Running       0          18s
my-pods-cc78567c8-cwvkw    1/1     Running       0          16s
my-pods-cc78567c8-cxn69    1/1     Running       0          18s
my-pods-cc78567c8-kdfsz    1/1     Running       0          18s
my-pods-cc78567c8-q6dc5    1/1     Running       0          18s
my-pods-cc78567c8-rz6j6    1/1     Running       0          16s
my-pods-cc78567c8-vvtl4    1/1     Running       0          16s
my-pods-cc78567c8-w78rf    1/1     Running       0          16s
my-pods-cc78567c8-wbg22    1/1     Running       0          16s
my-pods-cc78567c8-wj7pq    1/1     Running       0          18s

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Terminating   0          92s
my-pods-58fdf5c854-7tkt2   1/1     Terminating   0          99s
my-pods-58fdf5c854-btw6f   1/1     Terminating   0          93s
my-pods-58fdf5c854-chvc5   1/1     Terminating   0          99s
my-pods-58fdf5c854-dspfc   1/1     Terminating   0          99s
my-pods-58fdf5c854-q975f   1/1     Terminating   0          99s
my-pods-58fdf5c854-sr4d4   1/1     Terminating   0          91s
my-pods-58fdf5c854-xfz7s   1/1     Terminating   0          99s
my-pods-58fdf5c854-xhzm2   1/1     Terminating   0          92s
my-pods-58fdf5c854-zqf7f   1/1     Terminating   0          92s
my-pods-cc78567c8-c2nl8    1/1     Running       0          22s
my-pods-cc78567c8-cwvkw    1/1     Running       0          20s
my-pods-cc78567c8-cxn69    1/1     Running       0          22s
my-pods-cc78567c8-kdfsz    1/1     Running       0          22s
my-pods-cc78567c8-q6dc5    1/1     Running       0          22s
my-pods-cc78567c8-rz6j6    1/1     Running       0          20s
my-pods-cc78567c8-vvtl4    1/1     Running       0          20s
my-pods-cc78567c8-w78rf    1/1     Running       0          20s
my-pods-cc78567c8-wbg22    1/1     Running       0          20s
my-pods-cc78567c8-wj7pq    1/1     Running       0          22s

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-58fdf5c854-2wrqz   1/1     Terminating   0          98s
my-pods-58fdf5c854-7tkt2   1/1     Terminating   0          105s
my-pods-58fdf5c854-btw6f   1/1     Terminating   0          99s
my-pods-58fdf5c854-chvc5   1/1     Terminating   0          105s
my-pods-58fdf5c854-dspfc   1/1     Terminating   0          105s
my-pods-58fdf5c854-q975f   1/1     Terminating   0          105s
my-pods-58fdf5c854-sr4d4   1/1     Terminating   0          97s
my-pods-58fdf5c854-xfz7s   1/1     Terminating   0          105s
my-pods-58fdf5c854-xhzm2   1/1     Terminating   0          98s
my-pods-58fdf5c854-zqf7f   1/1     Terminating   0          98s
my-pods-cc78567c8-c2nl8    1/1     Running       0          28s
my-pods-cc78567c8-cwvkw    1/1     Running       0          26s
my-pods-cc78567c8-cxn69    1/1     Running       0          28s
my-pods-cc78567c8-kdfsz    1/1     Running       0          28s
my-pods-cc78567c8-q6dc5    1/1     Running       0          28s
my-pods-cc78567c8-rz6j6    1/1     Running       0          26s
my-pods-cc78567c8-vvtl4    1/1     Running       0          26s
my-pods-cc78567c8-w78rf    1/1     Running       0          26s
my-pods-cc78567c8-wbg22    1/1     Running       0          26s
my-pods-cc78567c8-wj7pq    1/1     Running       0          28s

$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-cc78567c8-c2nl8   1/1     Running   0          51s
my-pods-cc78567c8-cwvkw   1/1     Running   0          49s
my-pods-cc78567c8-cxn69   1/1     Running   0          51s
my-pods-cc78567c8-kdfsz   1/1     Running   0          51s
my-pods-cc78567c8-q6dc5   1/1     Running   0          51s
my-pods-cc78567c8-rz6j6   1/1     Running   0          49s
my-pods-cc78567c8-vvtl4   1/1     Running   0          49s
my-pods-cc78567c8-w78rf   1/1     Running   0          49s
my-pods-cc78567c8-wbg22   1/1     Running   0          49s
my-pods-cc78567c8-wj7pq   1/1     Running   0          51s



$ kubectl apply -f deployment-2-ex3.yaml 
deployment.apps/my-pods configured

$ kubectl get po
NAME                       READY   STATUS              RESTARTS   AGE
my-pods-5857fbd978-lncrk   2/2     Running             0          2s
my-pods-5857fbd978-mfnlh   0/2     ContainerCreating   0          1s
my-pods-cc78567c8-c2nl8    1/1     Terminating         0          88s
my-pods-cc78567c8-cwvkw    1/1     Terminating         0          86s
my-pods-cc78567c8-cxn69    1/1     Terminating         0          88s
my-pods-cc78567c8-kdfsz    1/1     Terminating         0          88s
my-pods-cc78567c8-q6dc5    1/1     Terminating         0          88s
my-pods-cc78567c8-rz6j6    1/1     Terminating         0          86s
my-pods-cc78567c8-vvtl4    1/1     Terminating         0          86s
my-pods-cc78567c8-w78rf    1/1     Terminating         0          86s
my-pods-cc78567c8-wbg22    1/1     Running             0          86s
my-pods-cc78567c8-wj7pq    1/1     Terminating         0          88s

$ kubectl get po
NAME                       READY   STATUS        RESTARTS   AGE
my-pods-5857fbd978-lncrk   2/2     Running       0          7s
my-pods-5857fbd978-mfnlh   2/2     Running       0          6s
my-pods-cc78567c8-c2nl8    1/1     Terminating   0          93s
my-pods-cc78567c8-cwvkw    1/1     Terminating   0          91s
my-pods-cc78567c8-cxn69    1/1     Terminating   0          93s
my-pods-cc78567c8-kdfsz    1/1     Terminating   0          93s
my-pods-cc78567c8-q6dc5    1/1     Terminating   0          93s
my-pods-cc78567c8-rz6j6    1/1     Terminating   0          91s
my-pods-cc78567c8-vvtl4    1/1     Terminating   0          91s
my-pods-cc78567c8-w78rf    1/1     Terminating   0          91s
my-pods-cc78567c8-wbg22    1/1     Terminating   0          91s
my-pods-cc78567c8-wj7pq    1/1     Terminating   0          93s

$ kubectl get po
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-5857fbd978-lncrk   2/2     Running   0          36s
my-pods-5857fbd978-mfnlh   2/2     Running   0          35s


$ kubectl rollout restart deployment/my-pods
deployment.apps/my-pods restarted

$ kubectl get po
NAME                      READY   STATUS              RESTARTS   AGE
my-pods-754fc8bdb-284zg   0/1     ContainerCreating   0          2s
my-pods-754fc8bdb-d968g   1/1     Running             0          2s
my-pods-754fc8bdb-lfkjl   1/1     Running             0          2s
my-pods-754fc8bdb-rc9xq   1/1     Running             0          2s
my-pods-754fc8bdb-vj4zn   1/1     Running             0          2s
my-pods-865dc6865-9g8qk   1/1     Running             0          45s
my-pods-865dc6865-br8dr   1/1     Running             0          44s
my-pods-865dc6865-bx6z6   1/1     Running             0          11s
my-pods-865dc6865-cmh9n   1/1     Terminating         0          11s
my-pods-865dc6865-csw5q   1/1     Terminating         0          11s
my-pods-865dc6865-cwh9s   1/1     Running             0          11s
my-pods-865dc6865-kktbq   1/1     Running             0          11s
my-pods-865dc6865-nb45r   1/1     Running             0          11s
my-pods-865dc6865-nkz9x   1/1     Running             0          11s
my-pods-865dc6865-tzlw6   1/1     Terminating         0          11s

$ kubectl get po
NAME                      READY   STATUS        RESTARTS   AGE
my-pods-754fc8bdb-284zg   1/1     Running       0          8s
my-pods-754fc8bdb-d968g   1/1     Running       0          8s
my-pods-754fc8bdb-hgrg4   1/1     Running       0          6s
my-pods-754fc8bdb-kldmq   1/1     Running       0          6s
my-pods-754fc8bdb-lfkjl   1/1     Running       0          8s
my-pods-754fc8bdb-rc9xq   1/1     Running       0          8s
my-pods-754fc8bdb-s8rqq   1/1     Running       0          6s
my-pods-754fc8bdb-vj4zn   1/1     Running       0          8s
my-pods-754fc8bdb-vzwcw   1/1     Running       0          6s
my-pods-754fc8bdb-wmw7k   1/1     Running       0          6s
my-pods-865dc6865-9g8qk   1/1     Terminating   0          51s
my-pods-865dc6865-br8dr   1/1     Terminating   0          50s
my-pods-865dc6865-bx6z6   1/1     Terminating   0          17s
my-pods-865dc6865-cmh9n   1/1     Terminating   0          17s
my-pods-865dc6865-csw5q   1/1     Terminating   0          17s
my-pods-865dc6865-cwh9s   1/1     Terminating   0          17s
my-pods-865dc6865-kktbq   1/1     Terminating   0          17s
my-pods-865dc6865-nb45r   1/1     Terminating   0          17s
my-pods-865dc6865-nkz9x   1/1     Terminating   0          17s
my-pods-865dc6865-tzlw6   1/1     Terminating   0          17s

$ kubectl get po
NAME                      READY   STATUS    RESTARTS   AGE
my-pods-754fc8bdb-284zg   1/1     Running   0          83s
my-pods-754fc8bdb-d968g   1/1     Running   0          83s
my-pods-754fc8bdb-hgrg4   1/1     Running   0          81s
my-pods-754fc8bdb-kldmq   1/1     Running   0          81s
my-pods-754fc8bdb-lfkjl   1/1     Running   0          83s
my-pods-754fc8bdb-rc9xq   1/1     Running   0          83s
my-pods-754fc8bdb-s8rqq   1/1     Running   0          81s
my-pods-754fc8bdb-vj4zn   1/1     Running   0          83s
my-pods-754fc8bdb-vzwcw   1/1     Running   0          81s
my-pods-754fc8bdb-wmw7k   1/1     Running   0          81s
