  
https://minikube.sigs.k8s.io/docs/tutorials/volume_snapshots_and_csi/


~~~
$ minikube start
$ minikube addons enable csi-hostpath-driver
~~~


~~~
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
~~~

~~~
$ minikube addons enable csi-hostpath-driver
💡  csi-hostpath-driver is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
❗  [警告] フル機能のために、'csi-hostpath-driver' アドオンが 'volumesnapshots' アドオンの有効化を要求しています。

'minikube addons enable volumesnapshots' を実行して 'volumesnapshots' を有効化できます

    ▪ registry.k8s.io/sig-storage/csi-attacher:v4.0.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-external-health-monitor-controller:v0.7.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.6.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/hostpathplugin:v1.9.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/livenessprobe:v2.8.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-resizer:v1.6.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-snapshotter:v6.1.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-provisioner:v3.3.0 イメージを使用しています
🔎  csi-hostpath-driver アドオンを検証しています...
🌟  'csi-hostpath-driver' アドオンが有効です
~~~


~~~
$ kubectl apply -f pvc.yaml 
persistentvolumeclaim/my-vol created
pod/pod-pvc created

$ kubectl get pvc
NAME     STATUS   VOLUME        CAPACITY   ACCESS MODES   STORAGECLASS      AGE
my-vol   Bound    pvc-e7da2af2  1Gi        RWO            csi-hostpath-sc   5s

$ kubectl get po
NAME      READY   STATUS    RESTARTS   AGE
pod-pvc   1/1     Running   0          9s
~~~


~~~
$ kubectl exec -it pod-pvc -- bash
groups: cannot find name for group ID 1000
I have no name!@pod-pvc:/app$ cd /mnt
I have no name!@pod-pvc:/mnt$ ls -la
total 8
drwxrwsr-x 2 root 1000 4096 Apr  8 06:32 .
drwxr-xr-x 1 root root 4096 Apr  8 06:32 ..
I have no name!@pod-pvc:/mnt$ tar cf test.tar /usr
tar: Removing leading `/' from member names
tar: Removing leading `/' from hard link targets
I have no name!@pod-pvc:/mnt$ ls -lh
total 389M
-rw-r--r-- 1 1000 1000 389M Apr  8 06:34 test.tar
I have no name!@pod-pvc:/mnt$ md5sum test.tar 
70c282f901c974c92f2126d01336ceab  test.tar
I have no name!@pod-pvc:/mnt$ exit
exit
~~~

~~~
$ kubectl get po
NAME      READY   STATUS    RESTARTS   AGE
pod-pvc   1/1     Running   0          2m21s
$ kubectl delete po
error: resource(s) were provided, but no name was specified
mini:ex-4_dynamic_pvc takara$ kubectl delete po pod-pvc
pod "pod-pvc" deleted
$ kubectl get pvc
NAME     STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
my-vol   Bound    pvc-e7da2af2-2c9d-47d3-a219-61cd0e6ad45d   1Gi        RWO            csi-hostpath-sc   3m7s
$ kubectl get po
No resources found in default namespace.
~~~

~~~
$ kubectl apply -f pod-pvc.yaml 
pod/pod-pvc created
$ kubectl get po
NAME      READY   STATUS    RESTARTS   AGE
pod-pvc   1/1     Running   0          5s
~~~


~~~
$ kubectl exec -it pod-pvc -- bash
groups: cannot find name for group ID 1000
I have no name!@pod-pvc:/app$ cd /mnt
I have no name!@pod-pvc:/mnt$ ls -lh
total 389M
-rw-rw-r-- 1 1000 1000 389M Apr  8 06:34 test.tar
I have no name!@pod-pvc:/mnt$ md5sum test.tar 
70c282f901c974c92f2126d01336ceab  test.tar
~~~


$ kubectl get pod pod-pvc -o=jsonpath='{.spec.volumes[0]}' |jq
{
  "name": "pv-data",
  "persistentVolumeClaim": {
    "claimName": "my-vol"
  }
}


$ kubectl exec -it pod-pvc -- bash
nobody@pod-pvc:/mnt$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
nobody@pod-pvc:/mnt$ cd /mnt
nobody@pod-pvc:/mnt$ date > test.dat
nobody@pod-pvc:/mnt$ ls -la
total 12
drwxrwsr-x 2 root   nogroup 4096 Apr  8 23:48 .
drwxr-xr-x 1 root   root    4096 Apr  8 23:48 ..
-rw-r--r-- 1 nobody nogroup   29 Apr  9 22:21 test.dat


mini:ex-4_dynamic_pvc takara$ ls
README.md	pod-pvc.yaml	pvc.yaml
mini:ex-4_dynamic_pvc takara$ kubectl apply -f pvc.yaml 
persistentvolumeclaim/my-vol created
mini:ex-4_dynamic_pvc takara$ kubectl apply -f pod-pvc.yaml 
pod/pod-pvc created
mini:ex-4_dynamic_pvc takara$ kubectl exec -it pod-pvc -- bash
error: unable to upgrade connection: container not found ("ubuntu")
mini:ex-4_dynamic_pvc takara$ kubectl exec -it pod-pvc -- bash
nobody@pod-pvc:/app$ cd /mnt
nobody@pod-pvc:/mnt$ date > test.dat
nobody@pod-pvc:/mnt$ ls
test.dat
nobody@pod-pvc:/mnt$ ls -al
total 12
drwxrwsr-x 2 root   nogroup 4096 Apr  9 22:53 .
drwxr-xr-x 1 root   root    4096 Apr  9 22:53 ..
-rw-r--r-- 1 nobody nogroup   29 Apr  9 22:53 test.dat
nobody@pod-pvc:/mnt$ cat test.dat 
Tue Apr  9 22:53:24 UTC 2024
nobody@pod-pvc:/mnt$ 

