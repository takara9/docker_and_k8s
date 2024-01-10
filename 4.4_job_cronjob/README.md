# ジョブとクローンジョブ

バッチ処理のためのコントローラー

## ジョブ
バッチ処理などを、処理の開始と終了がある処理を担当するポッド
正常終了するまで、所定回数をリトライするポッド

ジョブの実行順序や条件を制御するジョブスケジューラーではない。


## クーロンジョブ

定期実行するジョブコントローラー
UNIXのクロックデーモン（クーロン）と同様の役割を実施


科学計算や業務処理など、バッチ処理の用途がある。


mini:ex-2_cronjob takara$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   37s   v1.28.3
minikube-m02   Ready    <none>          21s   v1.28.3
minikube-m03   Ready    <none>          12s   v1.28.3
mini:ex-2_cronjob takara$ ls
cronjob.yaml
mini:ex-2_cronjob takara$ kubectl apply -f cronjob.yaml 
cronjob.batch/hello created
mini:ex-2_cronjob takara$ kubectl get po
No resources found in default namespace.
mini:ex-2_cronjob takara$ kubectl get cronjob
NAME    SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   5 * * * *   False     0        <none>          16s


mini:ex-2_cronjob takara$ kubectl get cronjob
NAME    SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   5 * * * *   False     0        78s             48m
mini:ex-2_cronjob takara$ kubectl get po
NAME                   READY   STATUS      RESTARTS   AGE
hello-28412645-p4p8q   0/1     Completed   0          82s


mini:ex-2_cronjob takara$ kubectl get po
NAME                   READY   STATUS      RESTARTS   AGE
hello-28413125-gkwm9   0/1     Completed   0          163m
hello-28413185-pbv46   0/1     Completed   0          103m
hello-28413245-trnn4   0/1     Completed   0          43m
mini:ex-2_cronjob takara$ kubectl get cronjob
NAME    SCHEDULE    SUSPEND   ACTIVE   LAST SCHEDULE   AGE
hello   5 * * * *   False     0        43m             11h
mini:ex-2_cronjob takara$ kubectl logs hello-28413125-gkwm9
Tue Jan  9 08:05:00 UTC 2024
Hello from the Kubernetes cluster
mini:ex-2_cronjob takara$ kubectl logs hello-28413185-pbv46
Tue Jan  9 09:05:00 UTC 2024
Hello from the Kubernetes cluster
mini:ex-2_cronjob takara$ kubectl logs hello-28413245-trnn4
Tue Jan  9 10:05:00 UTC 2024
Hello from the Kubernetes cluster