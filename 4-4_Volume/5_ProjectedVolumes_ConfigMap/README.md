# プロジェクテッドボリューム（コンフィグマップ）
コンフィグマップをボリュームとして、ポッドからマウントします。


## 準備
```
$ minikube start
```


## 実行例
コンフィグマップにするディレクトリconfigを確認する。
ディレクトリconfigの中には、二つのテキストファイル
```
$ tree config
config
├── default.config
└── test.conf

```

コマンドで、ディレクトリをコンフィグマップにする
```
$ kubectl create cm app-conf --from-file=config
configmap/app-conf created
```

コンフィグマップが出来た事を確認
```
$ kubectl get cm app-conf
NAME               DATA   AGE
app-conf           1      15s

$ kubectl get cm app-conf -o yaml
$ kubectl describe cm app-conf
```

コンフィグマップをマウントするポッドをデプロイする。
ポッドに入って、マウントしたコンフィグマップのファイルを確認

```
$ kubectl apply -f pod-cm-dir.yaml 
$ kubectl exec -it pod-cm-vol -- bash -c 'ls /conf'
default.config  test.conf
```


キーとバリューを登録したコンフィグマップをデプロイ
```
$ kubectl apply -f cm-kv.yaml 
$ kubectl get cm game-params
NAME          DATA   AGE
game-params   4      12s
$ kubectl get cm game-params -o yaml
$ kubectl describe cm game-params
```


コンフィグマップをマウントするポッドをデプロイ
ポッドに入って、マウントしたコンフィグマップを確認する。マウントしたコンフィグマップを確認、二つのファイルが見える。
ファイルを表示すると、コンフィグマップに設定したキーとバリューのリストが確認できる。
```
$ kubectl apply -f pod-cm-kv.yaml 
$ kubectl exec -it pod-cm-kv -- bash -c 'ls /config'
$ kubectl exec -it pod-cm-kv -- bash -c 'cat /config/game.properties'
$ kubectl exec -it pod-cm-kv -- bash -c 'cat /config/user-interface.properties'
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/projected-volumes/
- https://kubernetes.io/docs/concepts/configuration/configmap/
