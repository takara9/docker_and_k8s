# コンテナプローブ
ポッド内のコンテナの活動状態を調べる３つの方法を見ていきます。


## 準備
最小構成のKubernetesクラスタを起動します。
```
$ minikube start
```


## 実行例
ライブネスプローブを使用するポッドのデプロイ
```
$ kubectl apply -f pod-liveness-probe.yaml
pod/liveness-probe created
```

コンテナの起動から再スタートのイベント（編集済み）
```
$ kubectl describe pod liveness-probe
Name:             liveness-probe
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Sun, 31 Mar 2024 13:53:05 +0900
Labels:           <none>
Annotations:      <none>
Status:           Running
IP:               10.244.0.17
IPs:
  IP:  10.244.0.17
Containers:
  liveness:
    Container ID:  docker://68c5def7536f3b5ea836baa7bd00a19ce6b3750278a53c303e259ef4cc5ff036
    Image:         ubuntu:latest
    Image ID:      docker-pullable://ubuntu@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
    Port:          <none>
    Host Port:     <none>
    Args:
      /bin/sh
      -c
      touch /tmp/healthy; sleep 30; rm -f /tmp/healthy; tail -f /dev/null
    State:          Running
      Started:      Sun, 31 Mar 2024 13:53:07 +0900
    Ready:          True
    Restart Count:  0
    Liveness:       exec [cat /tmp/healthy] delay=0s timeout=1s period=5s #success=1 #failure=1
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-z4kzg (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-z4kzg:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age               From               Message
  ----     ------     ----              ----               -------
  Normal   Scheduled  39s               default-scheduler  Successfully assigned default/liveness-probe to minikube
  Normal   Pulled     37s               kubelet            Successfully pulled image "ubuntu:latest" in 2.087s (2.087s including waiting)
  Normal   Created    37s               kubelet            Created container liveness
  Normal   Started    37s               kubelet            Started container liveness
  Warning  Unhealthy  4s                kubelet            Liveness probe failed: cat: /tmp/healthy: No such file or directory
  Normal   Killing    4s                kubelet            Container liveness failed liveness probe, will be restarted
  Normal   Pulling    2s (x2 over 39s)  kubelet            Pulling image "ubuntu:latest"
  ```


レディネスプローブを使用するポッドのデプロイ
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


