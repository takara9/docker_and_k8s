# 永続ボリュームのスナップショット
永続ボリュームは、ドライバーがあれば、スナップショットを取得できます。

## 準備
minikubeをセットアップします。今回はボリューム・スナップショットを有効化します。
```
$ minikube start
$ minikube addons disable storage-provisioner
$ minikube addons disable default-storageclass
$ minikube addons enable csi-hostpath-driver
$ minikube addons enable volumesnapshots
```

ストレージクラスのデフォルトを変更します。
```
$ kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
$ kubectl get sc
NAME                        PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE
csi-hostpath-sc (default)   hostpath.csi.k8s.io   Delete          Immediate
```

スナップを取得する対象の永続ボリュームをセットアップします。
永続ボリュームのファイルシステムに、現在時刻を書き込んでおきます。
```
$ kubectl apply -f pvc.yaml 
$ kubectl get pvc  # STATUS が Bound になったら次へ進む
$ kubectl apply -f pod-pvc.yaml 
$ kubectl get po   # STATUS が Running になったら次へ進む
$ kubectl exec -it pod-pvc -- bash -c 'date > /mnt/test.dat'
```

## 実行例
### 永続ボリュームからスナップショットを取得

スナップショットクラスがセットアップされていることを確認します。
```
$ kubectl get volumesnapshotclasses
NAME                     DRIVER                DELETIONPOLICY   AGE
csi-hostpath-snapclass   hostpath.csi.k8s.io   Delete           112s
```


snapshot.yaml
```
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata:
  name: my-snapshot # スナップショットのオブジェクト名
spec:
  volumeSnapshotClassName: csi-hostpath-snapclass
  source:
    persistentVolumeClaimName: my-vol  # 元の永続ボリューム名を指定
```


スナップショットの取得を実行します。
```
$ kubectl apply -f snapshot.yaml 
volumesnapshot.snapshot.storage.k8s.io/my-snapshot created

$ kubectl get volumesnapshot
NAME         READYTOUSE  SOURCEPVC  RESTORESIZE  SNAPSHOTCLASS           SNAPSHOTCONTENT       AGE
my-snapshot  true        my-vol     1Gi          csi-hostpath-snapclass  snapcontent-2868f860  26s
```


### スナップショットから永続ボリュームを復元する

restore.yaml 
```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-vol-snapshot  # リストアの永続ボリューム名
spec:
  storageClassName: csi-hostpath-sc
  dataSource:
    name: my-snapshot    # スナップショットの名前
    kind: VolumeSnapshot
    apiGroup: snapshot.storage.k8s.io
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```


リストアの実行
```
$ kubectl apply -f restore.yaml 
persistentvolumeclaim/my-vol-snapshot created

$ kubectl get pvc
NAME             STATUS  VOLUME       CAPACITY  ACCESS MODES  STORAGECLASS     AGE
my-vol           Bound   pvc-d4ae742d 1Gi       RWO           csi-hostpath-sc  2m47s
my-vol-snapshot  Bound   pvc-f9fbfdcd 1Gi       RWO           csi-hostpath-sc  3s
```

ポッドからマウントして、書き込まれたデータを確認する
```
$ kubectl apply -f pod-pvc-from-snapshot.yaml
pod/pod-pvc2 created

$ kubectl exec -it pod-pvc2 -- bash -c 'ls -al /mnt'
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/volume-snapshot-classes/

