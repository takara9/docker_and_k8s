# ポッドの実行開始と起動確認
Kubernetesでのコンテナの実行単位であるポッドをKubernetes上で起動します。


## 準備
最小構成のKubernetesクラスタを起動します。
```
$ minikube start
```


## 実行例
ポッドの実行開始
```
$ kubectl apply -f pod.yaml 
pod/my-pod created
```

ポッド起動の確認
```
$ kubectl get pod
NAME     READY   STATUS              RESTARTS   AGE
my-pod   0/1     ContainerCreating   0          48s

$ kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          56s
```

K8sクラスタのネームスペース kube-system で起動しているポッド
```
$ kubectl get pod -n kube-system
NAME                               READY   STATUS    RESTARTS        AGE
coredns-5dd5756b68-tqpv4           1/1     Running   0               4m17s
etcd-minikube                      1/1     Running   0               4m31s
kube-apiserver-minikube            1/1     Running   0               4m31s
kube-controller-manager-minikube   1/1     Running   0               4m30s
kube-proxy-27jp6                   1/1     Running   0               4m17s
kube-scheduler-minikube            1/1     Running   0               4m30s
storage-provisioner                1/1     Running   1 (3m47s ago)   4m30s
```

K8sクラスタで実行する全ポッドのリスト
```
$ kubectl get po -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
default       my-pod                             1/1     Running   0               7m40s
kube-system   coredns-5dd5756b68-tqpv4           1/1     Running   0               7m59s
kube-system   etcd-minikube                      1/1     Running   0               8m13s
kube-system   kube-apiserver-minikube            1/1     Running   0               8m13s
kube-system   kube-controller-manager-minikube   1/1     Running   0               8m12s
kube-system   kube-proxy-27jp6                   1/1     Running   0               7m59s
kube-system   kube-scheduler-minikube            1/1     Running   0               8m12s
kube-system   storage-provisioner                1/1     Running   1 (7m29s ago)   8m12s
```

コントロールプレーンのetcdからPodのリストを表示
```
$ kubectl exec -it -n kube-system etcd-minikube -- sh -c "ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cert /var/lib/minikube/certs/etcd/server.crt --key /var/lib/minikube/certs/etcd/server.key --cacert /var/lib/minikube/certs/etcd/ca.crt get / --prefix --keys-only" | awk 'length($0)>1'|grep pods
/registry/pods/default/my-pod
/registry/pods/kube-system/coredns-5dd5756b68-tqpv4
/registry/pods/kube-system/etcd-minikube
/registry/pods/kube-system/kube-apiserver-minikube
/registry/pods/kube-system/kube-controller-manager-minikube
/registry/pods/kube-system/kube-proxy-27jp6
/registry/pods/kube-system/kube-scheduler-minikube
/registry/pods/kube-system/storage-provisioner
```


## クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/workloads/pods/
- https://kubernetes.io/docs/reference/kubectl/quick-reference/

