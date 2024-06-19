# ポッドアフィニティ
密接に連携するポッド同士を同じノードに配置する。

## 準備
クラスタを起動した後、コントロールプレーンにスケジュールされない様にテイントを設定します。
```console
$ minikube start -n 3
$ kubectl get no
$ kubectl taint nodes minikube controller:NoSchedule
```

## ポッドアフィニティの設定

deployment-pa.yaml(抜粋)
```
<前略>
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
<以下省略>
```

## 実行例
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


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/