
https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/

ノードからの退避

メンテナンスなどの理由で、スケジュールを禁止する


デバイスのあるノードへスケジュール
https://kubernetes.io/docs/tasks/configure-pod-container/assign-pods-nodes-using-node-affinity/


均等に分散配置する。


minikube start --nodes=3


## ノードへのラベル付与
```
mini:4-4_scheduling takara$ kubectl get node --show-labels
NAME           STATUS   ROLES           AGE     VERSION   LABELS
minikube       Ready    control-plane   6d10h   v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube,kubernetes.io/os=linux,minikube.k8s.io/commit=8220a6eb95f0a4d75f7f2d7b14cef975f050512d,minikube.k8s.io/name=minikube,minikube.k8s.io/primary=true,minikube.k8s.io/updated_at=2024_05_06T18_46_15_0700,minikube.k8s.io/version=v1.32.0,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-balancers=,topology.hostpath.csi/node=minikube
minikube-m02   Ready    <none>          12h     v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube-m02,kubernetes.io/os=linux,topology.hostpath.csi/node=minikube-m02
minikube-m03   Ready    <none>          12h     v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube-m03,kubernetes.io/os=linux,topology.hostpath.csi/node=minikube-m03
```

```
$ kubectl get nodes -o=jsonpath='{.items[*].metadata.labels}' |jq -r .
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube",
  "kubernetes.io/os": "linux",
  "minikube.k8s.io/commit": "8220a6eb95f0a4d75f7f2d7b14cef975f050512d",
  "minikube.k8s.io/name": "minikube",
  "minikube.k8s.io/primary": "true",
  "minikube.k8s.io/updated_at": "2024_05_06T18_46_15_0700",
  "minikube.k8s.io/version": "v1.32.0",
  "node-role.kubernetes.io/control-plane": "",
  "node.kubernetes.io/exclude-from-external-load-balancers": "",
  "topology.hostpath.csi/node": "minikube"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m02",
  "kubernetes.io/os": "linux",
  "topology.hostpath.csi/node": "minikube-m02"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m03",
  "kubernetes.io/os": "linux",
  "topology.hostpath.csi/node": "minikube-m03"
}
```



## nodeSelector

ラベルの付与

```
$ kubectl label nodes minikube-m02 disktype=ssd

$ kubectl apply -f deployment.yaml 

$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS      AGE    IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-778bf5d8fd-mpv5t   1/1     Running   0             32s    10.244.1.4   minikube-m02   <none>           <none>
my-pods-778bf5d8fd-r7q26   1/1     Running   0             32s    10.244.1.5   minikube-m02   <none>           <none>
my-pods-778bf5d8fd-zkkp8   1/1     Running   0             32s    10.244.1.3   minikube-m02   <none>           <none>
mypod3                     1/1     Running   3 (13h ago)   6d8h   10.244.0.9   minikube       <none>           <none>
```

## nodeName
ノード名を指定して移動も可能

```
mini:4-4-1_nodeSelector takara$ kubectl get po -o wide
NAME                       READY   STATUS        RESTARTS      AGE     IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-744c85b57-4pd5r    1/1     Running       0             21s     10.244.2.3   minikube-m03   <none>           <none>
my-pods-744c85b57-j9pvm    1/1     Running       0             9s      10.244.2.5   minikube-m03   <none>           <none>
my-pods-744c85b57-kxvts    1/1     Running       0             10s     10.244.2.4   minikube-m03   <none>           <none>
my-pods-778bf5d8fd-mpv5t   1/1     Terminating   0             5m26s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-778bf5d8fd-r7q26   1/1     Terminating   0             5m26s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-778bf5d8fd-zkkp8   1/1     Terminating   0             5m26s   10.244.1.3   minikube-m02   <none>           <none>
mypod3                     1/1     Running       3 (13h ago)   6d8h    10.244.0.9   minikube       <none>           <none>
```

```
mini:4-4-1_nodeSelector takara$ kubectl get po -o wide
NAME                      READY   STATUS    RESTARTS      AGE    IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-744c85b57-4pd5r   1/1     Running   0             96s    10.244.2.3   minikube-m03   <none>           <none>
my-pods-744c85b57-j9pvm   1/1     Running   0             84s    10.244.2.5   minikube-m03   <none>           <none>
my-pods-744c85b57-kxvts   1/1     Running   0             85s    10.244.2.4   minikube-m03   <none>           <none>
mypod3                    1/1     Running   3 (13h ago)   6d8h   10.244.0.9   minikube       <none>           <none>
```

