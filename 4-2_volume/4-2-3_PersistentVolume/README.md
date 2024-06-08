#　永続ボリューム


## 準備
最小構成のKubernetesクラスタを起動して、デフォルトのストレージクラスを無効化します。そして、`csi-hostpath-driver`を有効化します。
これで永続ストレージのダイナミックプロビジョニングを利用できます。
```
$ minikube start
$ minikube addons disable storage-provisioner
$ minikube addons disable default-storageclass
$ minikube addons enable csi-hostpath-driver
```

ストレージクラスのデフォルトを設定する。
```
$ kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
$ kubectl get sc
NAME                        PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-hostpath-sc (default)   hostpath.csi.k8s.io   Delete          Immediate           false                  60s
```


## 実行例

pod-pvc.yaml（抜粋）
```
<前略>
spec:
<中略>
  containers:
    - name: ubuntu
      image: ghcr.io/takara9/ex1:1.0   # コンテナイメージ
      command: ["tail", "-f", "/dev/null"] 
      volumeMounts:
      - name: pv-data      # (5)ボリュームを選択
        mountPath: /mnt    #    マウントポイント
  volumes:
    - name: pv-data           # (6)ボリューム名
      persistentVolumeClaim:  #    永続ストレージクレームを指定
        claimName: my-vol     #    クレーム名
<以下省略>
```

永続ボリュームを作成して、ポッドからマウントする。
永続ボリュームの作成が完了するには、少し時間がかかる場合があります。
```
$ kubectl apply -f pvc.yaml 
persistentvolumeclaim/my-vol created

$ kubectl get pvc
NAME     STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS      AGE
my-vol   Pending                                      csi-hostpath-sc   5s

$ kubectl get pvc
NAME     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
my-vol   Bound    pvc-78e97a6c-0491-4f79-962e-21a9cea073b3   1Gi        RWO            csi-hostpath-sc   12s
```


ポッドの対話型シェルで、永続ボリュームに対して、書き込み読み取りを実施
```
$ kubectl apply -f pod-pvc.yaml
$ kubectl exec -it pod-pvc -- bash
nobody@pod-pvc:/app$ cd /mnt
nobody@pod-pvc:/mnt$ tar cf test.tar /usr
tar: Removing leading `/' from member names
tar: Removing leading `/' from hard link targets
nobody@pod-pvc:/mnt$ ls -lh
total 389M
-rw-r--r-- 1 nobody nogroup 389M Jun  8 09:28 test.tar
nobody@pod-pvc:/mnt$ exit
$
```

一旦ポッドを削除して、永続ボリュームが存在していることを確認する。
```
$ kubectl get pvc
NAME     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
my-vol   Bound    pvc-e7da2af2-2c9d-47d3-a219-61cd0e6ad45d   1Gi        RWO            csi-hostpath-sc   3m7s
```

ポッドを削除して、再度、ポッドを起動して、ボリュームがマウントされていることを確認する
```
$ kubectl delete po pod-pvc
$ kubectl apply -f pod-pvc.yaml 
```

ポッドに永続ボリュームが付いていることを確認
```
$ kubectl get pod pod-pvc -o=jsonpath='{.spec.volumes[0]}' |jq
{
  "name": "pv-data",
  "persistentVolumeClaim": {
    "claimName": "my-vol"
  }
}
```

ポッドの中から、データが保存されていることを確認する
```
$ kubectl exec -it pod-pvc -- bash
groups: cannot find name for group ID 1000
I have no name!@pod-pvc:/app$ cd /mnt
I have no name!@pod-pvc:/mnt$ ls -lh
total 389M
-rw-rw-r-- 1 1000 1000 389M Apr  8 06:34 test.tar
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/persistent-volumes/
