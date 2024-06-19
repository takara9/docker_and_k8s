# サイドカーコンテナ（ポッドに複数のコンテナを内包する）
ポッド内に複数のコンテナを起動する方法です。


## 準備
```
$ minikube start
$ kubectl get no
```


## サイドカーコンテナ
spec.containersの下に、配列として、複数のコンテナを書くことができます。

sidecar-container.yaml(抜粋)
```
spec:
  containers:
   - name: my-container-1  # メインコンテナと呼ばれる事もある
     image: ghcr.io/takara9/ex1:1.0
     ports:
      - name: ex1-port
        containerPort: 9100
   - name: my-container-2  # サポートコンテナやサイドカーコンテナと呼ばれる事がある
     image: ghcr.io/takara9/ex3:1.0
     ports:
      - name: ex3-port
        containerPort: 3000
```

ポッド内で複数のコンテナを起動
```
$ kubectl apply -f sidecar-container.yaml 
$ kubectl get pod my-pod-mc -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pod-mc  2/2     Running   0          28m   10.244.0.8   minikube
```

ポッド内で実行する二つのコンテナを表示
```
$ kubectl get pod my-pod-mc -o jsonpath='{.spec.containers}' |jq -r '.[]| [.name, .image]'
[
  "my-container-1",
  "ghcr.io/takara9/ex1:1.0"
]
[
  " my-container-2",
  "ghcr.io/takara9/ex3:1.0"
]
```


## ポッド間のストレージ共有
spec.volumesに複数のボリュームを記述
各コンテナで、volumeMountsで、ボリューム名とマウントパスを指定して、コンテナのファイルシステムにマウント

pod-vol-share.yaml(抜粋)
```
spec:
  containers:
   - name: my-container-1  # コンテナ-１
     image: ghcr.io/takara9/ex1:1.0
     ports:
      - name: ex1-port
        containerPort: 9100
     volumeMounts: 
      - mountPath: /cache  # マウント位置
        name: cache-volume # 共有ボリューム名

   - name: my-container-2  # コンテナ-２
     image: ghcr.io/takara9/ex3:1.0
     ports:
      - name: ex3-port
        containerPort: 3000
     volumeMounts:
      - mountPath: /cache  # マウント位置
        name: cache-volume # 共有ボリューム名

  volumes: # 共有ボリューム
  - name: cache-volume
    emptyDir:  # ボリュームの種類
      sizeLimit: 500Mi # サイズ
```


ボリュームを共有するコンテナを内包するポッドの起動と確認
```
$ kubectl apply -f pod-vol-share.yaml 
$ kubectl get pod my-pod-vol-share
NAME               READY   STATUS    RESTARTS   AGE
my-pod-vol-share   2/2     Running   0          5m49s
```

コンテナ１から共有ボリュームへの書き込み
```
$ kubectl exec -it my-pod-vol-share -c my-container-1 -- bash
nobody@my-pod-vol-share:/app$ ps -ax > /cache/test.dat
nobody@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
nobody@my-pod-vol-share:/app$ exit 
exit
```

コンテナ２で、コンテナ１で書き込んだデータの表示
```
$ kubectl exec -it my-pod-vol-share -c my-container-2 -- bash
node@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
node@my-pod-vol-share:/app$ ps -ax
bash: ps: command not found
```


## 初期化専用コンテナの実行例

init-container.yaml(抜粋)
```
spec:
  initContainers:        ### 初期化専用コンテナ
  - name: init-data
    image: ubuntu:22.04
    # 共有ぼリュームへ、メッセージファイルを書き込んで、20秒待って、終了
    command: ['sh', '-c', "echo 'initialize data' > /vol/data; sleep 20"]
    volumeMounts:
      - mountPath: /vol
        name: share-volume
  containers:            ### メインのコンテナ
  - name: myapp
    image: ubuntu:22.04
    # 共有ボリュームのファイルをcatで表示して、１時間後の終了
    command: ['sh', '-c', 'cat /vol/data && sleep 3600']
    volumeMounts:
      - mountPath: /vol
        name: share-volume
  volumes:               ### 共有ボリューム
  - name: share-volume
    emptyDir:
      sizeLimit: 10Mi
```


```
$ kubectl apply -f init-container.yaml 
$ kubectl get po myapp-pod
NAME        READY   STATUS            RESTARTS   AGE
myapp-pod   0/1     PodInitializing   0          28s　　　← 初期化専用コンテナが実行中

$ kubectl get po myapp-pod
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          32s　　← メインコンテナが実行中

$ kubectl logs -c myapp myapp-pod
initialize data
```


# クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
- https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
- https://kubernetes.io/docs/concepts/workloads/pods/ephemeral-containers/

