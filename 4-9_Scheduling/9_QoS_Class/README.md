# QoSクラス
ノードのメモリが不足したとき、退避するポッドを決めるために使われ、優先度の高い順にGuaranteed, Burstable, BestEffortの３つのクラスがあります。ポッド内のコンテナに指定したリソース制約の結果として、Kubernetes が各ポッドに QoS クラスを割り当てます。


## 準備
```
$ minikube start -n 3
$ kubectl taint nodes minikube-m02 workload:NoSchedule
$ kubectl taint nodes minikube-m03 workload:NoSchedule
$ minikube addons enable metrics-server
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl taint nodes minikube-m03 workload:NoSchedule-
$ kubectl get no
$ kubectl get po -A -o wide
NAMESPACE     NAME                               READY   STATUS    RESTARTS       AGE     IP             NODE
kube-system   coredns-7db6d8ff4d-zwmfn           1/1     Running   0              2m32s   10.244.0.2     minikube
kube-system   etcd-minikube                      1/1     Running   0              2m45s   192.168.49.2   minikube
kube-system   kindnet-5fpbb                      1/1     Running   0              100s    192.168.49.4   minikube-m03
kube-system   kindnet-krw79                      1/1     Running   0              2m10s   192.168.49.3   minikube-m02
kube-system   kindnet-nfbcg                      1/1     Running   0              2m33s   192.168.49.2   minikube
kube-system   kube-apiserver-minikube            1/1     Running   0              2m45s   192.168.49.2   minikube
kube-system   kube-controller-manager-minikube   1/1     Running   0              2m45s   192.168.49.2   minikube
kube-system   kube-proxy-8qbcc                   1/1     Running   0              2m10s   192.168.49.3   minikube-m02
kube-system   kube-proxy-llqtg                   1/1     Running   0              100s    192.168.49.4   minikube-m03
kube-system   kube-proxy-xlh2m                   1/1     Running   0              2m33s   192.168.49.2   minikube
kube-system   kube-scheduler-minikube            1/1     Running   0              2m45s   192.168.49.2   minikube
kube-system   metrics-server-c59844bb4-xtcdp     1/1     Running   0              39s     10.244.0.3     minikube
kube-system   storage-provisioner                1/1     Running   1 (2m8s ago)   2m44s   192.168.49.2   minikube
```


## Guaranteed

```
$ kubectl apply -f guaranteed-pod.yaml
<中略>
$ kubectl describe pod
Name:             guaranteed-pod
Namespace:        default
Priority:         0
Service Account:  default
<中略>
Containers:
  guaranteed-container:
    Image:          ghcr.io/takara9/ex3:1.0
<中略>
    Restart Count:  0
    Limits:
      cpu:     700m
      memory:  200Mi
    Requests:
      cpu:        700m
      memory:     200Mi
<中略>
QoS Class:                   Guaranteed   <---- ここに注目 
Node-Selectors:              <none>
<以下省略>
```

ポッドの中に、request/limitが設定されていないコンテナがあると、boostableになる

```
$ kubectl apply -f guaranteed-pod-sidecar.yaml  
<中略>

$ kubectl describe pod guaranteed-pod-with-sidecar 
Name:             guaranteed-pod-with-sidecar
Namespace:        default
Priority:         0
<中略>
Containers:
  guaranteed-container:
    Image:          ghcr.io/takara9/ex3:1.0
    <中略>
    Limits:
      cpu:     700m
      memory:  200Mi
    Requests:
      cpu:        700m
      memory:     200Mi
    <中略>
  best-effort-container:
    Image:          ghcr.io/takara9/ex4:1.0
    <中略>
QoS Class:                   Burstable     <---- ここに注目
<以下省略>
```

## Burstable

```
$ kubectl apply -f .\burstable-pod.yaml           
<中略>

$ kubectl describe pod burstable-pod
Name:             burstable-pod
Namespace:        default
Priority:         0
<中略>

Containers:
  burstable-container:
    Image:          ghcr.io/takara9/ex3:1.0
    <中略>
    Requests:
      cpu:        700m
      memory:     200Mi
    <中略>

QoS Class:                   Burstable     <---- ここに注目
<以下省略>
```

## BestEffort

```
$ kubectl apply -f .\bestefort-pod.yaml
<中略>

$ kubectl describe pod
Name:             bestefort-pod
<中略>
Containers:
  bestefort-container:
    Image:          ghcr.io/takara9/ex3:1.0
    <中略>
QoS Class:                   BestEffort     <---- ここに注目
<以下省略>
```

```
$ kubectl get po -o wide
NAME                          READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
bestefort-pod                 1/1     Running   0          9s    10.244.2.5   minikube-m03   <none>           <none>
burstable-pod                 1/1     Running   0          22s   10.244.2.4   minikube-m03   <none>           <none>
guaranteed-pod                1/1     Running   0          43s   10.244.2.2   minikube-m03   <none>           <none>
guaranteed-pod-with-sidecar   2/2     Running   0          32s   10.244.2.3   minikube-m03   <none>           <none>
```

$ kubectl get pod -o jsonpath='{.status.qosClass}' |jq

kubectl get pod guaranteed-pod-new -o jsonpath='{.metadata.name} {.status.qosClass}'