# ポッド・デイスラプション・バジェット
ポッドの停止可能数を設定して、非自発的中断を防止する。ただし、自発的中断はポッド・デイスラプション・バジェットの設定の対象にならない。


## 準備
簡単にするため、１ノードでk8sクラスタを起動する

```console
minikube start -n 3
kubectl get no
kubectl taint nodes minikube key1=value1:NoSchedule
```

ポッドの停止できる数を規定する

my-pdb.yaml 
```
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: my-pdb
spec:
  maxUnavailable: 0
  selector:
    matchLabels:
      app: my-pod
```

PDBをネームスペースに適用する。
```
$ kubectl apply -f my-pdb.yaml 
```


## 非自発的中断を防止
デプロイされたノードを調べてドレインする。
しかし、PDBが設定があるので、エラーが発生してドレインできない。

```
$ kubectl apply -f deployment-pdb-1.yaml
$ NODE=$(kubectl get pods -o=jsonpath='{range .items[*]}{.spec.nodeName}{" "}{end}')
$ kubectl drain $NODE --ignore-daemonsets 
node/minikube-m03 already cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-sd9xp, kube-system/kube-proxy-b72rl
evicting pod default/my-pods-744958c68c-ldl24
error when evicting pods/"my-pods-744958c68c-ldl24" -n "default" (will retry after 5s): Cannot evict pod as it would violate the pod's disruption budget.
＜以下コマンドを中断＞
```

自発的中断はPDBが効かない事に注意

    Caution:
    Not all voluntary disruptions are constrained by Pod Disruption Budgets. For example, deleting deployments or pods bypasses Pod Disruption Budgets.

https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#pod-disruption-budgets



ポッドをアップデートするためのポッドの中断、すなわち、自発的中断に対しては、制限されない。
そのため、ポッドの停止と更新が進行する。
```
$ kubectl get pods -o=jsonpath='{.items[].spec.containers[].image}';echo
ghcr.io/takara9/ex1:1.0
$ kubectl apply -f deployment-pdb-2.yaml
$ kubectl get pods -o=jsonpath='{.items[].spec.containers[].image}';echo
ghcr.io/takara9/ex1:1.1
```

## クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/tasks/run-application/configure-pdb/
- https://kubernetes.io/docs/concepts/workloads/pods/disruptions/#pod-disruption-budgets
 

