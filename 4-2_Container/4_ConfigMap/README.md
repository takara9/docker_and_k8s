# コンテナの起動のインタフェース コンフィグマップ
コンフィグマップからデータを読み込んで環境変数にセットします。


## 準備
```
$ minikube start
$ kubectl get no
```

configmap.yaml
```
apiVersion: v1 
kind: ConfigMap     # コンフィグマップ
metadata:
  name: my-config   # コンフィグマップ名
data:
  special.how: very # キーと値
```

pod-cm.yaml（抜粋）
```
  containers:
    - name: m-container
      image: ghcr.io/takara9/ex1:1.0
      env: # 環境変数設定API
        - name: SPECIAL_LEVEL_KEY # 環境変数名
          valueFrom:
            configMapKeyRef:      # コンフィグマップから取得
              name: my-config     # コンフィグマップ名
              key: special.how    # 値を取り出すためのキー
```


ポッドを起動して、ポッドのコンテナで対話型シェルを起動して、環境変数を表示します。
```
$ kubectl apply -f configmap.yaml
$ kubectl apply -f pod-cm.yaml 
$ kubectl get po 
$ kubectl exec -it my-pod-cm -- bash -c 'echo $SPECIAL_LEVEL_KEY'
very
```


## クリーンナップ
```
$ kubectl delete pod my-pod-cm
$ kubectl delete cm my-config
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/#define-container-environment-variables-using-configmap-data
