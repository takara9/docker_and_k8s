# ポッドアンチアフィニティ
ごdSpeed＄5050全て異なるノードに、ポッドを配置する。

## 準備
４ノードのK8sクラスタを起動、す
```console
$ minikube start -n 4
$ minikube addons enable csi-hostpath-driver
$ kubectl get no
$ kubectl taint nodes minikube controller:NoSchedule
```


## 実行例
deployment-aa.yaml(抜粋)
```
<前略>
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

ノードに一つのポッドが配置される
```console
$ kubectl apply -f deployment-aa.yaml 
$ kubectl get po -o wide
NAME                           READY   STATUS    AGE   IP           NODE
redis-cache-8478cbdc86-ln6wt   1/1     Running   39s   10.244.2.4   minikube-m03
redis-cache-8478cbdc86-n8887   1/1     Running   39s   10.244.3.4   minikube-m04
redis-cache-8478cbdc86-rnlsv   1/1     Running   39s   10.244.1.3   minikube-m02
```
ポッドのレプリカ数を増やしても、ノードの数以上に配置されない。


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#inter-pod-affinity-and-anti-affinity