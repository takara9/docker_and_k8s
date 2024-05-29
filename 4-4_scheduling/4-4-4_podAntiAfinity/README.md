# ポッドアンチアフィニティ

全て異なるノードに、ポッドを配置する。

```console
$ minikube start -n 4
$ minikube addons enable csi-hostpath-driver
$ kubectl get no
$ kubectl taint nodes minikube controller:NoSchedule
```

```file:deployment-aa.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-pods
spec:
  <中略>
  template:
    <中略>
    spec:
      containers:
      <中略>
      affinity:
        podAntiAffinity:　# ポッドアンチアフィニティ
          requiredDuringSchedulingIgnoredDuringExecution: #スケジュール時有効
          - labelSelector:  # ラベルセレクター
              matchExpressions:  # 選択条件
              - key: app     # ラベルのキー
                operator: In # 含む
                values:      # ラベルの値
                - store
            topologyKey: "kubernetes.io/hostname"
<以下省略>
```


```console
$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   6m38s   v1.28.3
minikube-m02   Ready    <none>          6m16s   v1.28.3
minikube-m03   Ready    <none>          6m3s    v1.28.3
minikube-m04   Ready    <none>          5m48s   v1.28.3

$ kubectl taint nodes minikube controller:NoSchedule
node/minikube tainted

$ kubectl apply -f deployment-aa.yaml 
deployment.apps/redis-cache created

$ kubectl get po -o wide
NAME                           READY   STATUS    AGE   IP           NODE
redis-cache-8478cbdc86-ln6wt   1/1     Running   39s   10.244.2.4   minikube-m03
redis-cache-8478cbdc86-n8887   1/1     Running   39s   10.244.3.4   minikube-m04
redis-cache-8478cbdc86-rnlsv   1/1     Running   39s   10.244.1.3   minikube-m02
```
