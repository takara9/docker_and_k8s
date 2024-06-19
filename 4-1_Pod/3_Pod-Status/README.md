# ポッドのステータス

## 準備
```
$ minikube start
$ kubectl get node
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   22s   v1.30.0
```

## 実行例
ポッドの実行開始と起動の確認
```
$ kubectl apply -f pod.yaml
pod/my-pod created
$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          13s
```

ポッドの詳細表示
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


実行中ポッドのAPI表示
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


## クリーンナップ
```
$ kubectl delete pod my-pod
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/workloads/pods/
- https://kubernetes.io/docs/reference/kubectl/quick-reference/









# ポッドとコンテナの状態管理
ポッドのライフサイクルの状態を表示します。

## 準備
最小構成のKubernetesクラスタを起動します。
```
$ minikube start
```


## 実行例
ポッドのフェーズ表示
```
$ kubectl run my-pod --image=ubuntu --restart=Never
pod/my-pod created
$ kubectl get pod my-pod -o jsonpath='{.status.phase}';echo
Succeeded
```

ポッド上のコンテナのステータス表示
```
$ kubectl get pod my-pod -o jsonpath='{.status.containerStatuses[]}'| jq -r .
{
  "containerID": "docker://b7c16cda01d27cd32ee0acb8c8fd92f0f98ca7153cb259cda6e4d67436e49031",
  "image": "ubuntu:latest",
  "imageID": "docker-pullable://ubuntu@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e",
  "lastState": {},
  "name": "my-pod",
  "ready": false,
  "restartCount": 0,
  "started": false,
  "state": {
    "terminated": {
      "containerID": "docker://b7c16cda01d27cd32ee0acb8c8fd92f0f98ca7153cb259cda6e4d67436e49031",
      "exitCode": 0,
      "finishedAt": "2024-03-31T00:05:18Z",
      "reason": "Completed",
      "startedAt": "2024-03-31T00:05:18Z"
    }
  }
}
```

ポッドのデプロイとログの表示
```
$ kubectl run nginx1 --image=nginx:latest
pod/nginx1 created

$ kubectl logs nginx1
Error from server (BadRequest): container "nginx1" in pod "nginx1" is waiting to start: ContainerCreating

$ kubectl logs nginx1
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/03/31 00:16:42 [notice] 1#1: using the "epoll" event method
2024/03/31 00:16:42 [notice] 1#1: nginx/1.25.4
2024/03/31 00:16:42 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2024/03/31 00:16:42 [notice] 1#1: OS: Linux 6.6.12-linuxkit
2024/03/31 00:16:42 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/03/31 00:16:42 [notice] 1#1: start worker processes
2024/03/31 00:16:42 [notice] 1#1: start worker process 29
2024/03/31 00:16:42 [notice] 1#1: start worker process 30
2024/03/31 00:16:42 [notice] 1#1: start worker process 31
2024/03/31 00:16:42 [notice] 1#1: start worker process 32
2024/03/31 00:16:42 [notice] 1#1: start worker process 33
2024/03/31 00:16:42 [notice] 1#1: start worker process 34
2024/03/31 00:16:42 [notice] 1#1: start worker process 35
2024/03/31 00:16:42 [notice] 1#1: start worker process 36
```


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://kubernetes.io/docs/concepts/cluster-administration/logging/
