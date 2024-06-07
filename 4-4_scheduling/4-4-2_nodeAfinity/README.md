# ノードアフィニティ
条件に一致するノードへ、ポッドを配置する。

## 準備
４つのノードを起動する
```
minikube start -n 3
```

アベイラビリティゾーンを想定したラベルを付与する
```
kubectl label nodes minikube-m02 topology.kubernetes.io/zone=tokyo-west1
kubectl label nodes minikube-m03 topology.kubernetes.io/zone=tokyo-east1
```


deployment-na.yaml(抜粋)
~~~
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-pods
spec:
  <中略>
  template:
    spec:
      affinity:        # アフィニティ(親和性)
        nodeAffinity:    # ノードアフィニティ（ノードへの親和性)
          requiredDuringSchedulingIgnoredDuringExecution:  # スケジュール時に限定
            nodeSelectorTerms:   # ノードを選択する条件
            - matchExpressions:    # 一致の式
              - key: topology.kubernetes.io/zone   # ゾーンを使用
                operator: In                       # （ゾーンに）存在する
                values:
                - tokyo-east1                      # ゾーンの名前
                - tokyo-west1                      # 同上
    <中略>
    containers:
<以下省略>
~~~


## 実行例
```
$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   48s   v1.28.3
minikube-m02   Ready    <none>          27s   v1.28.3
minikube-m03   Ready    <none>          15s   v1.28.3

$ kubectl label nodes minikube-m02 topology.kubernetes.io/zone=tokyo-west1
kubectl label nodes minikube-m03 topology.kubernetes.io/zone=tokyo-east1node/minikube-m02 labeled
$ kubectl label nodes minikube-m03 topology.kubernetes.io/zone=tokyo-east1
node/minikube-m03 labeled

$ kubectl get pod -o wide
NAME                       READY   STATUS    AGE   IP           NODE
my-pods-748d684849-47gz8   1/1     Running   23s   10.244.1.2   minikube-m02
my-pods-748d684849-688t4   1/1     Running   23s   10.244.1.3   minikube-m02
my-pods-748d684849-g4nk7   1/1     Running   23s   10.244.2.2   minikube-m03
my-pods-748d684849-mh5n7   1/1     Running   23s   10.244.2.3   minikube-m03
```


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/
