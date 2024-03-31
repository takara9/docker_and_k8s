
## 4.1.2.1.	コマンドでポッドを起動

実行例 4.1.2-1 ポッドの実行例
```
$ kubectl run myserver --image=ghcr.io/takara9/ex3:1.0
pod/myserver created

$ kubectl get pod myserver
NAME       READY   STATUS    RESTARTS   AGE
myserver   1/1     Running   0          15s
```


実行例 4.1.2-2 ポッドの起動と対話形シェルの実行
```
$ kubectl run -it my-ubuntu --image=ubuntu -- bash
If you don't see a command prompt, try pressing enter.
root@my-ubuntu:/# cat /etc/issue
Ubuntu 22.04.4 LTS \n \l

root@my-ubuntu:/# ps -x
    PID TTY      STAT   TIME COMMAND
      1 pts/0    Ss     0:00 bash
     10 pts/0    R+     0:00 ps -x
root@my-ubuntu:/# ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var
root@my-ubuntu:/# whoami
root
root@my-ubuntu:/# exit
exit
Session ended, resume using 'kubectl attach my-ubuntu -c my-ubuntu -i -t' command when the pod is running
$ 
```


実行例 4.1.2-3 ポートフォワードとパソコンからポッドへのアクセス
```
$ kubectl port-forward myserver 3000:3000 &
[1] 20200
$ Forwarding from 127.0.0.1:3000 -> 3000
Forwarding from [::1]:3000 -> 3000

$ curl localhost:3000/ping;echo
Handling connection for 3000
pong
```


## 4.1.2.2.ポッドのAPI起動と状態取得

実行例 4.1.2-4 ポッドの実行開始と起動の確認
```
$ kubectl apply -f pod.yaml
pod/my-pod created
$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          13s
```

実行例 4.1.2-5 ポッドの詳細表示
```
$ kubectl describe pod my-pod
Name:             my-pod           (1) ポッドの基本情報
Namespace:        default
Priority:         0
Service Account:  default     
Node:             minikube/192.168.49.2
Start Time:       Fri, 29 Mar 2024 11:15:28 +0900
Labels:           <none>
Annotations:      <none>
Status:           Running          (2) ポッドの実行状態
IP:               10.244.0.3       (3) ポッドのIPアドレス
IPs:
  IP:  10.244.0.3
Containers:                        (4) 内部コンテナの情報
  container-1:
    Container ID:   docker://bedf312a318f4a2858717f194674e97837592f44c7ae440345781ca35dd33b60
    Image:          ghcr.io/takara9/ex3:1.0
    Image ID:       docker-pullable://ghcr.io/takara9/ex3@sha256:34b3d3970b6523095b75f5151b58ce601933ef46a4cd60aeaeba9f4959a2ac85
    Port:           <none>
    Host Port:      <none>
    State:          Running         (5) コンテナの実行状態
      Started:      Fri, 29 Mar 2024 11:15:35 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-rv6d9 (ro)
Conditions:                         (6) ポッドの状況
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:                            (7) ボリューム
  kube-api-access-rv6d9:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:                             (8) ポッドのイベント
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  58s   default-scheduler  Successfully assigned default/my-pod to minikube
  Normal  Pulling    58s   kubelet            Pulling image "ghcr.io/takara9/ex3:1.0"
  Normal  Pulled     51s   kubelet            Successfully pulled image "ghcr.io/takara9/ex3:1.0" in 6.232s (6.232s including waiting)
  Normal  Created    51s   kubelet            Created container container-1
  Normal  Started    51s   kubelet            Started container container-1
  ```



実行例 4.1.2-6 実行中ポッドのAPI表示
```
$ kubectl get pod my-pod -o yaml
apiVersion: v1
kind: Pod
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Pod","metadata":{"annotations":{},"name":"my-pod","namespace":"default"},"spec":{"containers":[{"image":"ghcr.io/takara9/ex3:1.0","name":"container-1"}]}}
  creationTimestamp: "2024-03-29T02:15:28Z"
  name: my-pod                               (1) ポッド名 
  namespace: default                         (2) ポッドが動作するネームスペース
  resourceVersion: "419"
  uid: 5d56c2c9-bc5d-4dde-a062-49d6a43f9b0e
spec:                                        (3) ポッドのスペック（仕様）が表示される場所
  containers:                                (4) 内包するコンテナ
  - image: ghcr.io/takara9/ex3:1.0           (5) コンテナイメージのアドレス
    imagePullPolicy: IfNotPresent
    name: container-1                        (6) コンテナ名
    resources: {}                            (7) リソース: CPU時間やメモリの割り当て
    terminationMessagePath: /dev/termination-log
    terminationMessagePolicy: File
    volumeMounts:                            (8) ポッドにマウントするボリューム
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-rv6d9
      readOnly: true
  dnsPolicy: ClusterFirst
  enableServiceLinks: true
  nodeName: minikube
  preemptionPolicy: PreemptLowerPriority
  priority: 0
  restartPolicy: Always
  schedulerName: default-scheduler
  securityContext: {}                        (9) 実行権限の制約に関する設定
  serviceAccount: default                    (10) ポッドは割り当てのサービスアカウントの権限で実行
  serviceAccountName: default
  terminationGracePeriodSeconds: 30          (11) 終了シグナルを受けてから強制終了されるまでの猶予秒数
  tolerations:                               (12) ポッドがノードへスケジュールするための設定
  - effect: NoExecute                        (13) 以下のkeyが付いたノードから排除され、ポッドはスケジュールされない
    key: node.kubernetes.io/not-ready
    operator: Exists
    tolerationSeconds: 300                   (14) taintがノードに付けられ、ポッドが排除されるまでの秒数
  - effect: NoExecute                        (15) 以下、(12)〜(14)に同じ、繰り返し
    key: node.kubernetes.io/unreachable
    operator: Exists
    tolerationSeconds: 300
  volumes:　　　　　　　　　　　　　　　　　　　　　(16) ポッドに自動定義されたボリュームの情報
  - name: kube-api-access-rv6d9
    projected:
      defaultMode: 420
      sources:
      - serviceAccountToken:
          expirationSeconds: 3607
          path: token
      - configMap:
          items:
          - key: ca.crt
            path: ca.crt
          name: kube-root-ca.crt
      - downwardAPI:
          items:
          - fieldRef:
              apiVersion: v1
              fieldPath: metadata.namespace
            path: namespace
status:　　　　　　　　　　　　　　　　　　　　　　　　(17) ポッドのステータス（状態）
  conditions:
  - lastProbeTime: null
    lastTransitionTime: "2024-03-29T02:15:28Z"
    status: "True"
    type: Initialized
  - lastProbeTime: null
    lastTransitionTime: "2024-03-29T02:15:35Z"
    status: "True"
    type: Ready
  - lastProbeTime: null
    lastTransitionTime: "2024-03-29T02:15:35Z"
    status: "True"
    type: ContainersReady
  - lastProbeTime: null
    lastTransitionTime: "2024-03-29T02:15:28Z"
    status: "True"
    type: PodScheduled
  containerStatuses:　　　　　　　　　　　　　　　　(18) 内包するコンテナのステータス（状態）
  - containerID: docker://bedf312a318f4a2858717f194674e97837592f44c7ae440345781ca35dd33b60
    image: ghcr.io/takara9/ex3:1.0
    imageID: docker-pullable://ghcr.io/takara9/ex3@sha256:34b3d3970b6523095b75f5151b58ce601933ef46a4cd60aeaeba9f4959a2ac85
    lastState: {}
    name: container-1
    ready: true
    restartCount: 0
    started: true
    state:
      running:
        startedAt: "2024-03-29T02:15:35Z"
  hostIP: 192.168.49.2
  phase: Running　　　　　　　　　　　　　　　　　　(19) ポッドのフェーズ
  podIP: 10.244.0.3                           (20) ポッドのIPアドレス
  podIPs:                                     (21) ポッドにセカンドIPがあれば、ここに表示される
  - ip: 10.244.0.3
  qosClass: BestEffort                        (22) リソース設定により、QOSクラスが決定される.
  startTime: "2024-03-29T02:15:28Z"                  「BestEffor」は優先度が一番低い
```


4.1.2-7 コントローラーによるポッドの起動と確認
```
$ kubectl apply -f deployment.yaml 
deployment.apps/ex1-deploy created

$ kubectl get deploy ex1-deploy 
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
ex1-deploy   3/3     3            3           15m

$ kubectl get pod -l app=ex1 -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP           NODE
ex1-deploy-86cfd74b9d-b8qds   1/1     Running   0          3m19s   10.244.0.4   minikube
ex1-deploy-86cfd74b9d-hq4g4   1/1     Running   0          3m19s   10.244.0.5   minikube
ex1-deploy-86cfd74b9d-n7z97   1/1     Running   0          3m19s   10.244.0.3   minikube
```

