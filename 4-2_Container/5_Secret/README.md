# コンテナの起動のインタフェース シークレット
シークレットからデータを読み込んで環境変数にセットします。


## 準備
```
$ minikube start
$ kubectl get no
```

secret.yaml
```
apiVersion: v1
kind: Secret  # シークレット
metadata:
  name: my-secret
stringData:
  my-token: "5%miYj"  # キーと値
```

pod-secret.yaml（抜粋）
```
  containers:
    - name: m-container
      image: ghcr.io/takara9/ex1:1.0
      env:                # 環境変数設定API
      - name: MY_PASSWORD # セットする環境変数名
        valueFrom:
          secretKeyRef:   # シークレットから取得
            name: my-secret  # シークレット名
            key: my-token    # 値を取得するキー
```

ポッドを起動して、STATUSが Running になったら、
ポッドのコンテナで対話型シェルを起動して、環境変数を表示します。
```
$ kubectl apply -f secret.yaml
$ kubectl apply -f pod-secret.yaml 
$ kubectl get po 
$ kubectl exec -it my-pod-secret -- bash -c 'echo $MY_PASSWORD'
5%miYj
```


## クリーンナップ
```
$ kubectl delete pod my-pod-secret
$ kubectl delete cm my-secret
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/configuration/secret/#using-secrets-as-environment-variables
- https://kubernetes.io/docs/concepts/configuration/secret/
