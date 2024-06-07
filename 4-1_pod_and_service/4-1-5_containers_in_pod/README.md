## 4.1.5.複数のコンテナを内包するポッド

実行例 4.1.5-1 複数のコンテナを内包するポッドの実行と起動
```
kubectl apply -f pod-multi-container.yaml 
pod/my-pod-mc created

$ kubectl get pod my-pod-mc -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pod-mc  2/2     Running   0          28m   10.244.0.8   minikube
```


実行例 4.1.5-2 ポッドで実行するコンテナの表示
```
$ kubectl get pod my-pod-mc -o jsonpath='{.spec.containers}' |jq -r '.[]| [.name, .image]'
[
  "my-container-1",
  "ghcr.io/takara9/ex1:1.0"
]
[
  " my-container-2",
  "ghcr.io/takara9/ex3:1.0"
]
```


実行例 4.1.5-3 ボリュームを共有するコンテナを内包するポッドの起動と確認
```
$ kubectl apply -f pod-vol-share.yaml 
pod/my-pod-vol-share created

$ kubectl get pod my-pod-vol-share
NAME               READY   STATUS    RESTARTS   AGE
my-pod-vol-share   2/2     Running   0          5m49s

$ kubectl describe po  my-pod-vol-share
Name:             my-pod-vol-share
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Tue, 20 Feb 2024 06:29:16 +0900
Labels:           app=my-pod
Annotations:      <none>
Status:           Running　　　　　　　(1)ポッドのテータス
IP:               10.244.0.14
IPs:
  IP:  10.244.0.14
Containers:
  my-container-1:
    Container ID:   docker://0282f14c82ba303c3d2021722a5a6562bd420ac205dfa468a9c57ddc50540163
    Image:          ghcr.io/takara9/ex1:1.0
    Image ID:       docker-pullable://ghcr.io/takara9/ex1@sha256:cb6cd2557aa67456f72663d3d612f5741de72a0b4635fdd2a10c9c1ac3238344
    Port:           9100/TCP
    Host Port:      0/TCP
    State:          Running　　　　　　(2)コンテナ１の状態
      Started:      Tue, 20 Feb 2024 06:29:16 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:　　　　　　　　　　　　 　　　(3)共通ボリュームをマウント
      /cache from cache-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xzrgb (ro)
  my-container-2:
    Container ID:   docker://cf0f352de8f346b5cf01f35d5e9c96537d28f1bf6d3838905a245651cd1672c8
    Image:          ghcr.io/takara9/ex3:1.0
    Image ID:       docker-pullable://ghcr.io/takara9/ex3@sha256:34b3d3970b6523095b75f5151b58ce601933ef46a4cd60aeaeba9f4959a2ac85
    Port:           3000/TCP
    Host Port:      0/TCP
    State:          Running　　　　　　(4)コンテナ２の状態
      Started:      Tue, 20 Feb 2024 06:29:16 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:                          (5)共通ボリュームをマウント
      /cache from cache-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xzrgb (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:　　　　　　　　　　　　　　　　　　(6)ポッド内部で共通利用するボリューム
  cache-volume:
    Type:       EmptyDir (a temporary directory that shares a pod's lifetime)
    Medium:     
    SizeLimit:  500Mi
  kube-api-access-xzrgb:
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
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  20s   default-scheduler  Successfully assigned default/my-pod-vol-share to minikube
  Normal  Pulled     20s   kubelet            Container image "ghcr.io/takara9/ex1:1.0" already present on machine
  Normal  Created    20s   kubelet            Created container my-container-1
  Normal  Started    20s   kubelet            Started container my-container-1
  Normal  Pulled     20s   kubelet            Container image "ghcr.io/takara9/ex3:1.0" already present on machine
  Normal  Created    20s   kubelet            Created container my-container-2
  Normal  Started    20s   kubelet            Started container my-container-2
```



実行例 4.1.5-4 コンテナ１から共有ボリュームへの書き込み
```
$ kubectl exec -it my-pod-vol-share -c my-container-1 -- bash
nobody@my-pod-vol-share:/app$ ps -ax > /cache/test.dat
nobody@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
nobody@my-pod-vol-share:/app$ exit 
exit
```

実行例 4.1.5-5 ポッドの実行開始と起動の確認
```
$ kubectl exec -it my-pod-vol-share -c my-container-2 -- bash
node@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
node@my-pod-vol-share:/app$ ps -ax
bash: ps: command not found
```


実行例 4.1.5-6 初期化専用コンテナの実行例
```
$ kubectl apply -f init-container.yaml 
pod/myapp-pod created

$ kubectl get po myapp-pod
NAME        READY   STATUS            RESTARTS   AGE
myapp-pod   0/1     PodInitializing   0          28s　　　← 初期化専用コンテナが実行中

$ kubectl get po myapp-pod
NAME        READY   STATUS    RESTARTS   AGE
myapp-pod   1/1     Running   0          32s　　← メインコンテナが実行中

$ kubectl logs -c myapp myapp-pod
initialize data
```