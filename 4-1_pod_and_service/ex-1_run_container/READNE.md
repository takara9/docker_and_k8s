

mini:4.1 takara$ kubectl get no -o wide
NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION    CONTAINER-RUNTIME
minikube       Ready    control-plane   25m   v1.28.3   192.168.49.2   <none>        Ubuntu 22.04.3 LTS   6.5.11-linuxkit   docker://24.0.7
minikube-m02   Ready    <none>          25m   v1.28.3   192.168.49.3   <none>        Ubuntu 22.04.3 LTS   6.5.11-linuxkit   docker://24.0.7
minikube-m03   Ready    <none>          25m   v1.28.3   192.168.49.4   <none>        Ubuntu 22.04.3 LTS   6.5.11-linuxkit   docker://24.0.7

mini:4.1 takara$ docker ps
CONTAINER ID   IMAGE                                 COMMAND                   CREATED          STATUS          PORTS                                                                                                                                  NAMES
15048252294c   gcr.io/k8s-minikube/kicbase:v0.0.42   "/usr/local/bin/entr…"   25 minutes ago   Up 25 minutes   127.0.0.1:51048->22/tcp, 127.0.0.1:51049->2376/tcp, 127.0.0.1:51051->5000/tcp, 127.0.0.1:51052->8443/tcp, 127.0.0.1:51050->32443/tcp   minikube-m03
a629ca6c5cb5   gcr.io/k8s-minikube/kicbase:v0.0.42   "/usr/local/bin/entr…"   26 minutes ago   Up 26 minutes   127.0.0.1:51001->22/tcp, 127.0.0.1:51002->2376/tcp, 127.0.0.1:50999->5000/tcp, 127.0.0.1:51000->8443/tcp, 127.0.0.1:51003->32443/tcp   minikube-m02
a025e417b9d0   gcr.io/k8s-minikube/kicbase:v0.0.42   "/usr/local/bin/entr…"   26 minutes ago   Up 26 minutes   127.0.0.1:50973->22/tcp, 127.0.0.1:50974->2376/tcp, 127.0.0.1:50976->5000/tcp, 127.0.0.1:50977->8443/tcp, 127.0.0.1:50975->32443/tcp   minikube

minikubeのkubernetesノードは、コンテナで動作しているので、コンテナからしかアクセスできません。

mini:4.1 takara$ docker network ls
NETWORK ID     NAME       DRIVER    SCOPE
c59ce2e65ee8   bridge     bridge    local
c9dca41f34bc   host       host      local
924209379adf   minikube   bridge    local
29a8bc8b20cc   none       null      local

minikube ネットワークへ繋いだコンテナを起動して、ノードポードにアクセスします。
pingが通過することが確認できたました。

mini:4.1 takara$ docker run -it --network minikube ghcr.io/takara9/my-ubuntu:0.2 bash
root@3e9080f20c4d:/# ping 192.168.49.2
PING 192.168.49.2 (192.168.49.2) 56(84) bytes of data.
64 bytes from 192.168.49.2: icmp_seq=1 ttl=64 time=0.228 ms
64 bytes from 192.168.49.2: icmp_seq=2 ttl=64 time=0.435 ms
^C

curlでアクセスします。

--- 192.168.49.2 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss, time 1034ms
rtt min/avg/max/mdev = 0.228/0.331/0.435/0.103 ms
root@3e9080f20c4d:/# curl http://192.168.49.2:32343/ping;echo
<p>pong</p>
root@3e9080f20c4d:/# curl http://192.168.49.3:32343/ping;echo
<p>pong</p>
root@3e9080f20c4d:/# curl http://192.168.49.4:32343/ping;echo
<p>pong</p>

どのノードにアクセスしても、サービスに到達することが確認できました。



マルチコンテナポッドも知って欲しい。




$ kubectl apply -f pod.yaml 
pod/my-pod created

$ kubectl get pods
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          5s



$ kubectl describe pods my-pod
Name:             my-pod
Namespace:        default
Priority:         0
Service Account:  default
Node:             minikube/192.168.49.2
Start Time:       Sun, 07 Jan 2024 15:57:21 +0900
Labels:           app=my-app-1
                  run=my-pod
Annotations:      <none>
Status:           Running
IP:               10.244.0.13
IPs:
  IP:  10.244.0.13
Containers:
  my-pod:
    Container ID:   docker://489e10f9cfcf9f4fdee26619cef0ef5086bca9d577e0a84ba76606a9ae530b0f
    Image:          ghcr.io/takara9/ex1:1.0
    Image ID:       docker-pullable://ghcr.io/takara9/ex1@sha256:cb6cd2557aa67456f72663d3d612f5741de72a0b4635fdd2a10c9c1ac3238344
    Port:           9100/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Sun, 07 Jan 2024 15:57:21 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-n4ftc (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
  kube-api-access-n4ftc:
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
  Type    Reason     Age    From              Message
  ----    ------     ----   ----              -------
  Normal  Scheduled  4m23s  default-scheduler Successfully assigned default/my-pod to minikube
  Normal  Pulled     4m23s  kubelet           Container image "ghcr.io/takara9/ex1:1.0" already present on machine
  Normal  Created    4m23s  kubelet           Created container my-pod
  Normal  Started    4m23s  kubelet           Started container my-pod



サービスのデプロイ

$ kubectl apply -f service.yaml 
service/my-service configured


サービスの存在確認

$ kubectl get service
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP    9h
my-service   ClusterIP   10.100.232.199   <none>        9100/TCP   6h58m


サービスをPCターミナルへフォワード

$ kubectl port-forward service/my-service 9100:9100
Forwarding from 127.0.0.1:9100 -> 9100
Forwarding from [::1]:9100 -> 9100


別ターミナルでcurlコマンドでアクセスして確認

$ curl http://localhost:9100/ping;echo
<p>pong</p>



$ kubectl apply -f pod-multi-container.yaml 
pod/my-pod created

$ kubectl get pod my-pod -o wide
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE
my-pod   2/2     Running   0          28m   10.244.0.8   minikube

$ kubectl get pod -o jsonpath='{.items[].spec.containers}' |jq -r '.[]| [.name, .image]'
[
  "my-pod1",
  "ghcr.io/takara9/ex1:1.0"
]
[
  "my-pod2",
  "ghcr.io/takara9/ex3:1.0"
]






## ポッド内でのボリュームの共有
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
Status:           Running
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
    State:          Running
      Started:      Tue, 20 Feb 2024 06:29:16 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /cache from cache-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xzrgb (ro)
  my-container-2:
    Container ID:   docker://cf0f352de8f346b5cf01f35d5e9c96537d28f1bf6d3838905a245651cd1672c8
    Image:          ghcr.io/takara9/ex3:1.0
    Image ID:       docker-pullable://ghcr.io/takara9/ex3@sha256:34b3d3970b6523095b75f5151b58ce601933ef46a4cd60aeaeba9f4959a2ac85
    Port:           3000/TCP
    Host Port:      0/TCP
    State:          Running
      Started:      Tue, 20 Feb 2024 06:29:16 +0900
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /cache from cache-volume (rw)
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-xzrgb (ro)
Conditions:
  Type              Status
  Initialized       True 
  Ready             True 
  ContainersReady   True 
  PodScheduled      True 
Volumes:
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



$ kubectl exec -it my-pod-vol-share -c my-container-1 -- bash
nobody@my-pod-vol-share:/app$ ps -ax > /cache/test.dat
nobody@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
nobody@my-pod-vol-share:/app$ exit 
exit

$ kubectl exec -it my-pod-vol-share -c my-container-2 -- bash
node@my-pod-vol-share:/app$ cat /cache/test.dat 
    PID TTY      STAT   TIME COMMAND
      1 ?        Ss     0:00 /usr/bin/python3 /usr/local/bin/flask run --host 0.0.0.0 --port 9100
      7 pts/0    Ss     0:00 bash
     15 pts/0    R+     0:00 ps -ax
node@my-pod-vol-share:/app$ ps -ax
bash: ps: command not found


```
apiVersion: v1
kind: Pod
metadata:
  name: my-pod-hook
spec:
  restartPolicy: Never
  containers:
  - name: container-1
    image: ubuntu:22.04
    command: ["/bin/sh", "-c", "/usr/bin/sleep 30"]
    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh","-c", "echo postStart >/var/log/msg.log; /usr/bin/sleep 15"]
      preStop:
        exec:
          command: ["/bin/sh","-c","echo preStop >>/var/log/msg.log"]
```

$ kubectl apply -f pod-hook.yaml 
pod/my-pod-hook created

$ kubectl get pod
NAME          READY   STATUS              RESTARTS   AGE
my-pod-hook   0/1     ContainerCreating   0          4s
$ kubectl get pod my-pod-hook -o jsonpath='{.status.containerStatuses[].state}'| jq -r .
{
  "waiting": {
    "reason": "ContainerCreating"
  }
}

$ kubectl get pod
NAME          READY   STATUS    RESTARTS   AGE
my-pod-hook   1/1     Running   0          19s
$ kubectl get pod my-pod-hook -o jsonpath='{.status.containerStatuses[].state}'| jq -r .
{
  "running": {
    "startedAt": "2024-02-26T21:34:12Z"
  }
}

$ kubectl get pod
NAME          READY   STATUS      RESTARTS   AGE
my-pod-hook   0/1     Completed   0          32s
$ kubectl get pod my-pod-hook -o jsonpath='{.status.containerStatuses[].state}'| jq -r .
{
  "terminated": {
    "containerID": "docker://8c7d90221a9a74c2a315fa69a1298f73c4236443a723d73154368e10ec4eadba",
    "exitCode": 0,
    "finishedAt": "2024-02-26T21:34:42Z",
    "reason": "Completed",
    "startedAt": "2024-02-26T21:34:12Z"
  }
}


$ kubectl exec -it my-pod-hook -- bash
root@my-pod-hook:/# tail -f /var/log/msg.log 
postStart
preStop
command terminated with exit code 137


$ kubectl get pod
NAME          READY   STATUS    RESTARTS   AGE
my-pod-hook   1/1     Running   0          23s

$ kubectl delete pod my-pod-hook
pod "my-pod-hook" deleted