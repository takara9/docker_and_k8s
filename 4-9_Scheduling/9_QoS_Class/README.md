# QoSクラス
ノードのメモリが不足したとき、退避するポッドを決めるために使われ、優先度の高い順にGuaranteed, Burstable, BestEffortの３つのクラスがあります。ポッド内のコンテナに指定したリソース制約の結果として、Kubernetes が各ポッドに QoS クラスを割り当てます。


## 準備
```
$ minikube start -n 2
$ minikube addons enable metrics-server
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl get no
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

ポッド名とQoSクラスをリストする

```
$ kubectl get pod guaranteed-pod-new -o jsonpath='{.metadata.name} {.status.qosClass}'
```

## クリーンナップ
```
minikube delete
```


## 参照資料
- Pod Quality of Service Classes https://kubernetes.io/docs/concepts/workloads/pods/pod-qos/
- Configure Quality of Service for Pods https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/

