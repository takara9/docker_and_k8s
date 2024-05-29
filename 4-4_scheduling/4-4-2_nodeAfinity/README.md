# ノードアフィニティ

条件に一致するノードへ、ポッドを配置する。




minikube start -n 4
kubectl label nodes minikube-m02 disktype=ssd
kubectl label nodes minikube topology.kubernetes.io/zone=tokyo-east1
kubectl label nodes minikube-m02 topology.kubernetes.io/zone=tokyo-west1
kubectl label nodes minikube-m03 topology.kubernetes.io/zone=tokyo-north1
kubectl label nodes minikube-m04 topology.kubernetes.io/zone=tokyo-south1


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

