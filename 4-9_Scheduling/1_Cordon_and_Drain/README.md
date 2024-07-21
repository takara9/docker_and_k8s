# コードンとドレイン
コードンは、ノードへのポッドのスケジュールを禁止します。
ドレインは、ノードへのスケジュールを禁止して、ポッドを退避させます。


## 準備
```
minikube delete
minikube start --nodes=3
kubectl taint nodes minikube workload:NoSchedule
```

ポッドの配置しておく
```
$ kubectl create deployment my-pods --image=ghcr.io/takara9/ex1:1.5 --replicas=2
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66dbbd8bd4-7xslp   1/1     Running   0          8s    10.244.2.4   minikube-m03
my-pods-66dbbd8bd4-bmsxq   1/1     Running   0          8s    10.244.1.3   minikube-m02
```


## 実行例

ノード2からポッドを退避する
```
$ kubectl drain minikube-m02 --delete-emptydir-data --ignore-daemonsets
node/minikube-m02 cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-tx2jl, kube-system/kube-proxy-2zszp
evicting pod default/my-pods-66dbbd8bd4-bmsxq
pod/my-pods-66dbbd8bd4-bmsxq evicted
node/minikube-m02 drained
```

これによりポッドは、ノード３に集約された
```
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66dbbd8bd4-6wx5f   1/1     Running   0          22s   10.244.2.5   minikube-m03
my-pods-66dbbd8bd4-7xslp   1/1     Running   0          69s   10.244.2.4   minikube-m03
```

ノード２はスケジュール禁止になった
```
$ kubectl get no
NAME           STATUS                     ROLES           AGE     VERSION
minikube       Ready                      control-plane   3m59s   v1.30.0
minikube-m02   Ready,SchedulingDisabled   <none>          3m41s   v1.30.0
minikube-m03   Ready                      <none>          3m30s   v1.30.0
```

ノード２のメンテナンス作業が完了した後、スケジュール可能に戻す
```
$ kubectl uncordon minikube-m02
node/minikube-m02 uncordoned
$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   4m30s   v1.30.0
minikube-m02   Ready    <none>          4m12s   v1.30.0
minikube-m03   Ready    <none>          4m1s    v1.30.0
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP           NODE
my-pods-66dbbd8bd4-6wx5f   1/1     Running   0          2m15s   10.244.2.5   minikube-m03
my-pods-66dbbd8bd4-7xslp   1/1     Running   0          3m2s    10.244.2.4   minikube-m03
```

偏ったポッドの配置を、均一に配置し直す
```
$ kubectl get deployment
NAME      READY   UP-TO-DATE   AVAILABLE   AGE
my-pods   2/2     2            2           4m9s

$ kubectl rollout restart deployment my-pods
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-654967c8f9-ctk2x   1/1     Running   0          8s    10.244.2.6   minikube-m03
my-pods-654967c8f9-rn7vk   1/1     Running   0          9s    10.244.1.4   minikube-m02
```


## クリーンナップ
```
minikube delete
```


## 参照資料
- https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_cordon/

