# コンテナの起動と停止のインタフェース　　環境変数
ポッドでコンテナを起動と終了処理に必要な以下３点から、環境変数を取り上げます。
  - 引数
  - 環境変数
  - シグナル処理


## 準備
```
$ minikube start
$ kubectl get no
```

pod-env.yaml（抜粋）
```
  containers:
  - name: my-container
    image: ghcr.io/takara9/ex1:1.0
    env:                                    # 環境変数API
    - name: DEMO_GREETING                   # 環境変数名
      value: "Hello from the environment"   # 環境変数の値
```


ポッドを起動して、ポッドのコンテナで対話型シェルを起動して、環境変数を表示します。
```
$ kubectl apply -f pod-env.yaml 
$ kubectl get pod
```

ポッドのステータスが Runningになったら、コンテナに入って環境変数を表示
```
$ kubectl exec -it pod-env -- bash
nobody@pod-env:/app$ echo $DEMO_GREETING 
Hello from the environment
```


## クリーンナップ
```
$ kubectl delete pod pod-env
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
