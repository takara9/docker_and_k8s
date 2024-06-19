# コンテナプローブ
ポッド内のコンテナの活動状態を調べる３つの方法を見ていきます。
- ライブネスプローブ(liveness probe)
- レディネスプローブ(readiness probe)


## 準備
```
$ minikube start
$ kubectl get no
```



## ライブネスプローブ　　コンテナ内コマンド実行で診断

起動から３０秒後に、ファイル /tmp/healthy を削除、ライブネスプローブが失敗するため、コンテナの再起動が実行

pod-liveness-probe.yaml(抜粋)
```
  containers:
  - name: liveness
    image: ubuntu:latest
    args:
    - /bin/sh
    - -c
    - touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; tail -f /dev/null
    livenessProbe:
      exec:
        command: ["cat", "/tmp/healthy"]
      failureThreshold: 1               # 1回の失敗で再起動する
      terminationGracePeriodSeconds: 1  # SIGTERMを送ってからの猶予時間(秒)
      periodSeconds: 5                  # 5秒間隔で診断する
```


ライブネスプローブを使用するポッドのデプロイ
```
$ kubectl apply -f pod-liveness-probe.yaml
pod/liveness-probe created
```


コンテナの起動から、ライブネスプローブの失敗と、コンテナの再起動のイベント(抜粋)
```
$ kubectl describe pod liveness-probe
Name:             liveness-probe
Namespace:        default
＜中略＞
Events:
  Type     Reason     Age   From     Message
  ----     ------     ----  ----     -------
＜中略＞
  Normal   Pulled     37s   kubelet  Successfully pulled image "ubuntu:latest" in 2.087s (2.087s including waiting)
  Normal   Created    37s   kubelet  Created container liveness
  Normal   Started    37s   kubelet  Started container liveness
  Warning  Unhealthy  4s    kubelet  Liveness probe failed: cat: /tmp/healthy: No such file or directory
  Normal   Killing    4s    kubelet  Container liveness failed liveness probe, will be restarted
  Normal   Pulling    2s    kubelet  Pulling image "ubuntu:latest"
 ```


## レディネスプローブを使用するポッドのデプロイ

pod-readiness-probe.yaml(抜粋)
```
  containers:
  - name: readiness
    image: ubuntu:latest
    args:
    - /bin/sh
    - -c
    - sleep 15; touch /tmp/ready; tail -f /dev/null
    readinessProbe: # レディネスプローブ、デフォルト10秒間隔で実行
      exec:
        command: ["cat","/tmp/ready"]
```

コンテナのスタートから15秒以降に、READYに変化
```
$ kubectl apply -f pod-readiness-probe.yaml
pod/readiness-probe created

$ kubectl get po readiness-probe -w
NAME              READY   STATUS              RESTARTS   AGE
readiness-probe   0/1     ContainerCreating   0          0s
readiness-probe   0/1     Running             0          4s
readiness-probe   1/1     Running             0          21s
```  


# クリーンナップ
```
minikube delete
```

## 参考資料
- https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/


