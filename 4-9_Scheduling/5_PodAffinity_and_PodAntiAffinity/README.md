# ポッドアフィニティ　と ポッドアンチアフィニティ

「ポッドアフィニティ」は、既に配置されたポッドのラベルを調べて、同じノードにポッドを配置します。
反対に「ポッドアンチアフィニティ」は、既存ポッドのラベルを調べて、共存を避ける様にポッドを配置します。


## 準備
クラスタを起動した後、コントロールプレーンにスケジュールされない様にテイントを設定します。
```console
$ minikube start -n 3
$ kubectl get no
$ kubectl taint nodes minikube controller:NoSchedule
```

## ポッドアフィニティ実行例

deployment-pa.yaml(抜粋)
```
<前略>
      affinity:
        podAffinity:  # ポッドアフィニティ
          requiredDuringSchedulingIgnoredDuringExecution:   # スケジュール時必要、実行時無視
          - labelSelector: # ラベルセレクター
              matchExpressions: # 選択条件
              - key: database   # ラベルのキー
                operator: In    # 含む
                values:
                - exist         # ラベルの値
            topologyKey: "kubernetes.io/hostname" # 同じホストに配置
<以下省略>
```


'affinity.podAffinity' により、ラベル 'database: exist' のポッドが存在するホストホスト名（ノード）へポッドが配置される。
 この設定によりデータベースが存在するノードへ選択的にポッドが配置される。

```console
$ kubectl apply -f statefulsets-mariadb-single.yaml 
$ kubectl apply -f deployment-pa.yaml 
$ kubectl get po -o wide
NAME                       READY   STATUS    AGE   IP           NODE
db-0                       1/1     Running   88s   10.244.1.4   minikube-m02
my-pods-5b87cf78f7-bpqrd   1/1     Running   22s   10.244.1.5   minikube-m02
my-pods-5b87cf78f7-lwjdj   1/1     Running   22s   10.244.1.7   minikube-m02
my-pods-5b87cf78f7-pzjqq   1/1     Running   22s   10.244.1.6   minikube-m02
```



## ポッドアンチアフィニティ実行例


deployment-aa.yaml(抜粋)
```
<前略>
      affinity:
        podAntiAffinity:　# ポッドアンチアフィニティ
          requiredDuringSchedulingIgnoredDuringExecution:  # スケジュール時必要、実行時無効
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
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/