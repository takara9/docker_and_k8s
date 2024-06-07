# デーモンセット

起動状態では、最初からデーモンセットがデプロイされている。
```
$ minikube start -n 2

$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   54s   v1.28.3
minikube-m02   Ready    <none>          34s   v1.28.3

$ kubectl get ds -n kube-system
NAME         DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR            AGE
kindnet      2         2         2       2            2           <none>                   63s
kube-proxy   2         2         2       2            2           kubernetes.io/os=linux   64s
```


全てのノードにポッドが作成される
```
$ kubectl apply -f daemonset.yaml
$ kubectl get ds -n kube-system my-daemonset
NAME           DESIRED   CURRENT   READY   UP-TO-DATE   AVAILABLE   NODE SELECTOR   AGE
my-daemonset   2         2         2       2            2           <none>          30s

$ kubectl get po -n kube-system -o wide -l name=my-daemonset
NAME                 READY   STATUS    RESTARTS   AGE   IP           NODE
my-daemonset-8nrgq   1/1     Running   0          54s   10.244.0.3   minikube
my-daemonset-stp6s   1/1     Running   0          54s   10.244.1.2   minikube-m02
```

ノードを追加すると、自動的にポッドも配置される
```
$ minikube node add --worker
$ kubectl get po -n kube-system -o wide -l name=my-daemonset
NAME                 READY   STATUS    RESTARTS      AGE     IP           NODE
my-daemonset-8nrgq   1/1     Running   0             2m39s   10.244.0.3   minikube
my-daemonset-stp6s   1/1     Running   0             2m39s   10.244.1.2   minikube-m02
my-daemonset-x8xvj   1/1     Running   3 (28s ago)   45s     10.244.2.2   minikube-m03
```

デーモンセットを消しと、全てのノードから、管理下のポッドが削除される
```
$ kubectl delete ds -n kube-system my-daemonset
$ kubectl get po -n kube-system -o wide -l name=my-daemonset
No resources found in kube-system namespace.
```


 
## 参考資料
- https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
