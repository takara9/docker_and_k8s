# ジョブ　(ジョブ)
開始と終了があるバッチ処理のコンテナに適したコントローラーです。


## 準備

```
$ minikube start
```


## ジョブのデプロイとポッドの起動

ポッドの完了状態を保持
```
$ kubectl apply -f job.yaml 
$ kubectl get job
NAME    STATUS     COMPLETIONS   DURATION   AGE
batch   Complete   1/1           3s         8s

$ kubectl get po
NAME          READY   STATUS      RESTARTS        AGE
batch-r9gf7   0/1     Completed   0               17s
```

ポッドのログから標準出力に出された結果を確認できる
```
$ kubectl logs batch-njm5v 
39486
54725
15376
28973
15319
```

終了コード 0以外では、異常終了と見做し、再実行
'backoffLimit: 2'では再試行２回を実施して、合計3回の失敗で、ジョブは失敗となる

```
$ kubectl apply -f job-failed.yaml 
$ kubectl get pod
NAME                 READY   STATUS   RESTARTS   AGE
batch-failed-wgz86   0/1     Error    0          103s
batch-failed-zgnk2   0/1     Error    0          92s
batch-failed-zltt7   0/1     Error    0          72s

$ kubectl get job
NAME           STATUS   COMPLETIONS   DURATION   AGE
batch-failed   Failed   0/1           117s       117s
```


```
$ kubectl apply -f job-failed-timeout.yaml 
$ kubectl get job
NAME       STATUS    COMPLETIONS   DURATION   AGE
batch-to   Running   0/1           4s         4s

$ kubectl get pod
NAME             READY   STATUS    RESTARTS   AGE
batch-to-jc6dw   1/1     Running   0          7s
$ kubectl get pod
NAME             READY   STATUS        RESTARTS   AGE
batch-to-jc6dw   1/1     Terminating   0          12s

mini:1_Job takara$ kubectl get job
NAME       STATUS   COMPLETIONS   DURATION   AGE
batch-to   Failed   0/1           28s        28s
```


## クリーンナップ
```
$ minikube delete
```


## 参考資料
- ジョブ https://kubernetes.io/docs/concepts/workloads/controllers/job/
- ジョブAPIリファレンス https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/
- 自動生成 APIリファレンス https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#job-v1-batch
- kubectlコマンドリファレンス job https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-job-em-



