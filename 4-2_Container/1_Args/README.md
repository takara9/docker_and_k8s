# コンテナの起動と停止のインタフェース　　引数（アーギュメント）

ポッドでコンテナを起動と終了処理に必要な以下３点の中から、引数（アーギュメント）を取り上げます。
  - 引数（アーギュメント）
  - 環境変数
  - シグナル処理


## 準備

```
$ minikube start
$ kubectl get no
```


## 実行例

pod-cmd-args.yamlの抜粋
```
spec:
  containers:
  - name: my-container
    image: ghcr.io/takara9/ex1:1.0
    command: ["printenv"]                  # コンテナ実行時のコマンド
    args: ["HOSTNAME", "KUBERNETES_PORT"]  # パラメータ
```


コマンドライン引数を指定したポッドの実行結果
```
$ kubectl create -f pod-cmd-args.yaml  (1) ポッドの起動
pod/pod-cmd-args created

$ kubectl get pod pod-cmd-args         (2) 実行状態の確認
NAME           READY   STATUS      RESTARTS   AGE
pod-cmd-args   0/1     Completed   0          21s

$ kubectl logs pod-cmd-args            (3) 実行結果の確認（ログの表示）
pod-cmd-args
tcp://10.96.0.1:443
```


## クリーンナップ
```
$ kubectl delete pod-cmd-args
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
