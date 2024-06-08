# エフェメラル（一時）ボリューム
一時ボリューム（ストレージ）は、初期は空で作られ、ポッドの削除と共に消去されます。

## 準備
```
$ minikube start
```

## 実行例

pod-emptydir.yaml(抜粋)
```
  containers:          # コンテナセクション
   - name: my-container-1
     image: ghcr.io/takara9/ex1:1.0
     volumeMounts:     # ボリュームマウント
      - mountPath: /cache  # ファイルシステムのツリーの位置を指定してマウントする
        name: cache-volume # ボリュームセクションで宣言したボリューム名
  volumes:             # ボリュームセクション
  - name: cache-volume     # ボリューム名、複数設定でき、マウント時に名前の指定が必要
    emptyDir:              # このキーでemptyDirの使用が決まる。以下はAPIに実装されたパラメータ
      sizeLimit: 500Mi 
```

```
$ kubectl apply -f pod-emptydir.yaml 
$ kubectl get pod
$ kubectl exec -it pod-emptydir -- bash
nobody@pod-emptydir:/app$ df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G   22G   35G  38% /
tmpfs            64M     0   64M   0% /dev
/dev/vda1        59G   22G   35G  38% /cache
shm              64M     0   64M   0% /dev/shm
tmpfs           7.7G   12K  7.7G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs           3.9G     0  3.9G   0% /sys/firmware

nobody@pod-emptydir:/app$ tar cvf /cache/test.tar /usr 
tar: Removing leading `/' from member names
/usr/
/usr/games/
/usr/src/

nobody@pod-emptydir:/app$ ls -lh /cache/
total 389M
-rw-r--r-- 1 nobody nogroup 389M Apr  7 08:35 test.tar
nobody@pod-emptydir:/app$ exit
```

ポッドが起動している間は、一時ボリュームのデータが保持される
```
$ kubectl exec -it pod-emptydir -- bash
nobody@pod-emptydir:/app$ ls -lh /cache/
total 389M
-rw-r--r-- 1 nobody nogroup 389M Apr  7 08:35 test.tar
nobody@pod-emptydir:/app$ exit
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/ephemeral-volumes/