# プロジェクテッドボリューム（シークレット）
シークレットをボリュームとして、ポッドからマウントします。

## 準備
```
$ minikube start
```

## 実行例

シークレットをデプロイして、ポッドからマウントします。
```
$ kubectl apply -f secret.yaml 
$ kubectl apply -f pod-secret.yaml 
```

ポッドのシークレットファイルを表示して確認します。
```
$ kubectl exec -it pod-secret -- bash -c 'cat /etc/secret-volume/.secret-file'
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/projected-volumes/
- https://kubernetes.io/docs/concepts/configuration/secret/



