# クローンジョブ
ジョブを時間指定で起動するコントローラー

## 準備

```
$ minikube start
```


## クローンジョブのデプロイとポッドの起動

```
$ kubectl apply -f cronjob.yaml 
$ kubectl get cronjob
NAME             SCHEDULE    TIMEZONE   SUSPEND   ACTIVE   LAST SCHEDULE   AGE
job-every-1min   * * * * *   <none>     False     0        4s              23s

$ kubectl get job
NAME                      STATUS     COMPLETIONS   DURATION   AGE
job-every-1min-28681224   Complete   1/1           2s         70s
job-every-1min-28681225   Complete   1/1           3s         10s

$ kubectl get pod
NAME                            READY   STATUS      RESTARTS   AGE
job-every-1min-28681224-fjm2g   0/1     Completed   0          75s
job-every-1min-28681225-2d69g   0/1     Completed   0          15s

$ kubectl logs job-every-1min-28681225-2d69g
28884
10614
17567
47460
4836
```

```
# ┌───────────── minute (0–59)
# │ ┌───────────── hour (0–23)
# │ │ ┌───────────── day of the month (1–31)
# │ │ │ ┌───────────── month (1–12)
# │ │ │ │ ┌───────────── day of the week (0–6) (Sunday to Saturday;
# │ │ │ │ │                                   7 is also Sunday on some systems)
# │ │ │ │ │
# │ │ │ │ │
# * * * * * <command to execute>
```

設定例
- `1 0 * * *`: 毎晩夜中の 00:01で実行
- `45 23 * * 6`: 毎週土曜日の午後 11:45で実行
- `*/5 1,2,3 * * *`: `*/n` nインターバル、`1,2,3` 1〜3の毎時、例えば`01:00, 01:05, 01:10`の感覚で 03:55まで実行


マクロによる指定
- @yearly (or @annually) １月１日の未明に実行 (`0 0 1 1 *`と同じ) 	
- @monthly 毎月1日の未明に実行 (`0 0 1 * *`と同じ)
- @weekly 毎週日曜日の未明に実行 (`0 0 * * 0`と同じ)
- @daily (or @midnight)	毎日の未明に実行 (`0 0 * * *`と同じ) 	
- @hourly 毎時0分に実行	(`0 * * * *`と同じ)
- @reboot スタート時に実行



毎分実行と毎時実行の例
```
$ kubectl apply -f cronjob-every-min.yaml 
$ kubectl apply -f cronjob-every-hourly.yaml 
$ kubectl get cronjob
NAME             SCHEDULE      TIMEZONE   SUSPEND   ACTIVE   LAST SCHEDULE   AGE
job-every-hour   @hourly       <none>     False     0        <none>          6s
job-every-min    */1 * * * *   <none>     False     0        <none>          28s

$ kubectl get job
NAME                      STATUS     COMPLETIONS   DURATION   AGE
job-every-hour-28681740   Complete   1/1           3s         50s
job-every-min-28681740    Complete   1/1           3s         50s

$ kubectl get pod
NAME                            READY   STATUS      RESTARTS   AGE
job-every-hour-28681740-7hrcn   0/1     Completed   0          58s
job-every-min-28681740-ssc44    0/1     Completed   0          58s
```



## クリーンナップ
```
$ minikube delete
```


## 参考資料
- クーロンジョブ https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- ジョブAPIリファレンス https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/cron-job-v1/
- 自動生成 APIリファレンス https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#cronjob-v1-batch
- kubectlコマンドリファレンス https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#-em-cronjob-em-

