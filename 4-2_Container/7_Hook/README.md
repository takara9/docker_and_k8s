# コンテナの起動と停止のインタフェース　 フック

コンテナの起動時と終了要求を受けた時に１回だけコマンドを実行できます。


## 準備

Dockerのレジストリをminikubeからアクセスできるようにします。 
```
$ minikube start
$ kubectl get no
$ eval $(minikube -p minikube docker-env)
```

コンテナをビルド
```
$ cd container-hook
$ docker build -t hook-test:dev .
$ docker images hook-test:dev
```

pod-hook.yaml (抜粋)
```
  containers:
  - name: container-1
    image: hook-test:dev
    lifecycle:
      postStart:  # ポッドのコンテナ開始時に実行
        exec:
          command: ["/bin/sh","-c", "echo postStart >> /app/app.log"]
      preStop:    # ポッドの終了要求で実行
        exec:
          command: ["/bin/sh","-c", "echo preStop >> /app/app.log; sleep 10"]
```


ビルドしたコンテナをポッドとして起動
```
$ cd ..
$ kubectl apply -f pod-hook.yaml 
$ kubectl get pod
```

ポッドを起動したターミナルで、コンテナに入って、ログを表示
```
$ kubectl exec -it my-pod-hook -- bash
nobody@my-pod-hook:/app$ tail -f  /app/app.log 
postStart
Start Web service
```

もう一つターミナルを立ち上げて、ポッドを削除
```
$ kubectl delete pod my-pod-hook
```

ログを表示するターミナルで、ログに以下のように、フックが実行され、ポッドが削除
```
nobody@my-pod-hook:/app$ tail -f  /app/app.log 
postStart
Start Web service
preStop
Accept SIGNAL
```


## クリーンナップ
```
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://github.com/takara9/ex1/tree/1.4

