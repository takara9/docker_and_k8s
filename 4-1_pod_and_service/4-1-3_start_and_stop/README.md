## 4.1.3. コンテナの起動と停止のインタフェース
ポッドでコンテナを起動と終了処理に必要な以下３点について学ぶ
  - 引数
  - 環境変数
  - シグナル処理


## 準備
最小構成のKubernetesクラスタを起動する
```
minikube start
```


## 実行例
コマンドライン引数を指定したポッドの実行結果
```
$ kubectl create -f pod-cmd-args.yaml  (1) ポッドの起動
pod/pod-cmd-args created

$ kubectl get pod pod-cmd-args  (2) 実行状態の確認
NAME           READY   STATUS      RESTARTS   AGE
pod-cmd-args   0/1     Completed   0          21s

$ kubectl logs pod-cmd-args   (3) 実行結果の確認（ログの表示）
pod-cmd-args
tcp://10.96.0.1:443
```


ポッドのデプロイとコマンド実行結果
```
$ kubectl apply -f pod-env.yaml   (1) ポッドのデプロイ（起動）
pod/pod-env created

$ kubectl get po pod-env  (2) 実行状態の確認
NAME      READY   STATUS    RESTARTS   AGE
pod-env   1/1     Running   0          24s

$ kubectl exec -it pod-env -- bash (3) 実行結果の確認（コンテナで環境変数を表示)
nobody@pod-env:/app$ echo $DEMO_GREETING
Hello from the environment
```


ポッドのデプロイと環境変数の確認
```
$ kubectl apply -f pod-cm.yaml # (1) YAMLをデプロイ
configmap/my-config created
pod/my-pod-cm created

$ kubectl get po my-pod-cm  # (2) ポッドのリスト表示
NAME        READY   STATUS    RESTARTS   AGE
my-pod-cm   1/1     Running   0          5s

$ kubectl get cm my-config  # (3) コンフィグマップの表示
NAME               DATA   AGE
my-config          1      9s

$ kubectl get po my-pod-cm  # (4) ポッドの実行状態確認
NAME           READY   STATUS    RESTARTS   AGE
my-pod-cm      1/1     Running   0          4s

$ kubectl exec -it my-pod-cm -- bash  # (5) ポッドに入って環境変数の確認
nobody@my-pod-cm:/app$ echo $SPECIAL_LEVEL_KEY
very
```


ポッドのデプロイと環境変数の確認
```
kubectl apply -f pod-secret.yaml
kubectl get secret my-secret
kubectl get po my-pod-secret
kubectl exec -it my-pod-secret -- bash 
nobody@my-pod-secret:/app$ echo $MY_PASSWORD
5emitj
```


ポッド内のログ表示
```
$ kubectl apply -f pod-hook.yaml   # (1) ポッドをデプロイ
pod/my-pod-hook created

$ kubectl get pod my-pod-hook      # (2) ポッドの起動を確認
NAME          READY   STATUS    RESTARTS   AGE
my-pod-hook   1/1     Running   0          14s

$ kubectl exec -it my-pod-hook -- bash  # (3) ポッドに入って、app.logを表示
nobody@my-pod-hook:/app$ tail -f app.log
postStart            (4) コンテナの実行開始で表示
Start Web service.   (5) コンテナのアプリ実行で表示
preStop              (6) 別ターミナルから「kubectl delete pod my-pod-hook」投入で表示
Accept SIGNAL        (7) SIGTERMを受けて表示、その後、終了

command terminated with exit code 137
$
```


ghcr.io/takara9/ex1:1.4のビルドとリポジトリへの登録
```
ls Dockerfile app.py app.log 
docker build -t ex1:1.4 .
export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag ex1:1.4 ghcr.io/takara9/ex1:1.4
docker push ghcr.io/takara9/ex1:1.4
```


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://kubernetes.io/docs/tasks/inject-data-application/define-command-argument-container/
- https://kubernetes.io/docs/tasks/inject-data-application/define-environment-variable-container/
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#pod-termination
