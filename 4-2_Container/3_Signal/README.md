# コンテナの起動と停止のインタフェース　 シグナル処理
ポッドでコンテナを起動と終了処理に必要な以下３点から、シグナル処理を取り上げます。
  - 引数
  - 環境変数
  - シグナル処理


## 準備

Dockerのレジストリをminikubeからアクセスできるようにします。 

```
$ minikube start
$ kubectl get no
$ eval $(minikube -p minikube docker-env)
```

## シグナル受信時の実行例
container-signal/app.py(抜粋)
```
# シグナルを受けた時の処理
def handler(signum, frame):
    # ここにアプリケーションの終了処理を書く
    logger("Accept SIGNAL\n")
    logger("\n")
    time.sleep(5)
    # コンテナ終了
    sys.exit()

# シグナルSIGTERMを受けた時の処理先関数を定義
signal.signal(signal.SIGTERM, handler)
```

```
$ cd container-signal
$ docker build -t signal-handler:dev .
$ docker images signal-handler:dev
REPOSITORY       TAG       IMAGE ID       CREATED              SIZE
signal-handler   dev       c4cea75c1209   About a minute ago   676MB
```


ポッドを起動します。
```
$ cd ..
$ kubectl apply -f pod.yaml 
$ kubectl get pod
```

二つのターミナルを使って、シグナルを受けた後の動作を確認します。

１番目のポッドを起動したターミナルで、コンテナに入って、ログを表示します。
```
$ kubectl exec -it pod-signal -- bash
nobody@pod-signal:/app$ tail -f  /app/app.log 
Start Web service
```

後から起動したターミナルでポッドを削除します。
```
$ kubectl delete pod pod-signal
pod "pod-signal" deleted
```

１番目のターミナルで、ログに以下のように表示され、ポッドは削除されました。
```
Accept SIGNAL

command terminated with exit code 137
```



## クリーンナップ
```
$ kubectl delete pod pod-env
$ minikube delete
```
docker desktopもリスタートしておく。



## 参考リンク
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/


