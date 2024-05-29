$ minikube start -n 3
$ minikube addons enable csi-hostpath-driver
$ kubectl get no
$ kubectl taint nodes minikube controller:NoSchedule
$ kubectl apply -f statefulsets-mariadb-single.yaml 
$ kubectl get po -o wide


クラスタを起動した後、コントロールプレーンにスケジュールされない様にテイントを設定します。

```console
$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   79s   v1.28.3
minikube-m02   Ready    <none>          58s   v1.28.3
minikube-m03   Ready    <none>          46s   v1.28.3

$ kubectl taint nodes minikube controller:NoSchedule
node/minikube tainted
```


```deployment-pa.yaml
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
        podAffinity:  # ポッドアフィニティ
          requiredDuringSchedulingIgnoredDuringExecution: # スケジュール時が対象
          - labelSelector: # ラベルセレクター
              matchExpressions: # 選択条件
              - key: database   # ラベルのキー
                operator: In    # 含む
                values:
                - exist         # ラベルの値
            topologyKey: "kubernetes.io/hostname" # 同じホストに配置
```

この 'affinity.podAffinity' により、ラベル 'database: exist' のポッドが存在するホストホスト名（ノード）へポッドが配置される。


実行例
```
$ kubectl apply -f statefulsets-mariadb-single.yaml 
$ kubectl apply -f deployment-pa.yaml 
$ kubectl get po -o wide
NAME                       READY   STATUS    AGE   IP           NODE
db-0                       1/1     Running   88s   10.244.1.4   minikube-m02
my-pods-5b87cf78f7-bpqrd   1/1     Running   22s   10.244.1.5   minikube-m02
my-pods-5b87cf78f7-lwjdj   1/1     Running   22s   10.244.1.7   minikube-m02
my-pods-5b87cf78f7-pzjqq   1/1     Running   22s   10.244.1.6   minikube-m02
```
