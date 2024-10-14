# リソース制約
ポッド内コンテナのCPUとメモリの割り当て最低保証と上限値を設定することができます。
それにより、Kubernetesは適切なノードを選び、ポッドを配置できます。


## 準備
```
$ minikube start -n 2
$ kubectl taint nodes minikube-m02 workload:NoSchedule
$ minikube addons enable metrics-server
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl taint nodes minikube-m02 workload:NoSchedule-
$ kubectl get no
```

### 演習するにあたって、ノードの割り当て可能なCPUコア数を確認

ノードの割り当て可能なCPUコア数を確認しておきます。Minikubeの実行環境によって、
割り当て可能なCPU数が異なりますので、環境に対応して調整しなければなりません。

macOS 
```
$ minikube version　コンテナノードで、ホストのCPUコア数が表示されている
minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        8
minikube-m02    8
```

Windows PC (NUC)　コンテナノードで、ホストのCPUコア数が表示されている
```
PS C:\Users\tkr99\docker_and_k8s> minikube version
W1014 17:34:15.000292    3328 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\tkr99\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.
minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff
PS C:\Users\tkr99\docker_and_k8s> kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        4
minikube-m02    4
```

Linux ノードをコンテナでシミュレートしたケース
```
$ minikube start -n 2
$ minikube version
minikube version: v1.34.0
commit: 210b148df93a80eb872ecbeb7e35281b3c582c61

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        12
minikube-m02    12
```

Linux ノードをVMで起動したケースは、CPUコア数は、VMに割り当てられたCPUコア数と同じとなる。
```
$ minikube start -n 2 --vm-driver=kvm2
$ minikube version
minikube version: v1.34.0
commit: 210b148df93a80eb872ecbeb7e35281b3c582c61

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        2
minikube-m02    2
```



## メモリの要求と最大を設定する

```
$ kubectl apply -f pod-memory-requests-limits.yaml 
pod/pod-memory-constraints created

$ kubectl get pod
NAME                     READY   STATUS    RESTARTS   AGE
pod-memory-constraints   1/1     Running   0          2s

$ kubectl get pod pod-memory-constraints -o=jsonpath='{.spec.containers[0].resources}' |jq
{
  "limits": {
    "memory": "100Mi"
  },
  "requests": {
    "memory": "50Mi"
  }
}

$ kubectl top pod
NAME                     CPU(cores)   MEMORY(bytes)   
pod-memory-constraints   953m         24Mi        
```

## メモリの最大を超過した時挙動

```
$ kubectl apply -f pod-memory-limits-exceed.yaml 
pod/pod-memory-limits-exceed created
$ kubectl get pod 
NAME                       READY   STATUS      RESTARTS   AGE
pod-memory-limits-exceed   0/1     OOMKilled   0          4s
```


## CPUの要求と最大を設定する

```
$ kubectl apply -f pod-cpu-requests-limits.yaml 
pod/pod-cpu-constraints created

$ kubectl get pod
NAME                  READY   STATUS    RESTARTS   AGE
pod-cpu-constraints   1/1     Running   0          5s

$ kubectl get pod pod-cpu-constraints -o=jsonpath='{.spec.containers[0].resources}' |jq
{
  "limits": {
    "cpu": "500m"
  },
  "requests": {
    "cpu": "100m"
  }
}

$ kubectl top pod
NAME                  CPU(cores)   MEMORY(bytes)   
pod-cpu-constraints   489m         2Mi    
```

requestだけを設定した場合、CPUを割り当てられたポッドが削除されると、ノードの残るのCPUを使用する。

```
$ kubectl apply -f pod-cpu-requests.yaml 
pod/pod-cpu-no-limits created

$ kubectl top pod
NAME                  CPU(cores)   MEMORY(bytes)   
pod-cpu-constraints   501m         2Mi             
pod-cpu-no-limits     1463m        3Mi     

$ kubectl delete pod pod-cpu-constraints 
pod "pod-cpu-constraints" deleted

$ kubectl top pod
NAME                CPU(cores)   MEMORY(bytes)   
pod-cpu-no-limits   1988m        3Mi       

$ kubectl top node minikube-m02
NAME           CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%   
minikube-m02   1999m        24%    314Mi           4%    
```

## スケジューリング

Linux上の仮想マシンベースのMinikubeクラスタで、演習を実施する
```
$ minikube start -n 2 --driver "kvm2"
```

deployment-requests.yaml 
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pods-request
spec:
  replicas: 5
<中略>
    spec:
      containers:
      - name: memory-constraints
        image: polinux/stress
        resources:
          requests:
            cpu: "0.6"     # 割り当て可能なCPUコア数を元に調整しなければならない
            memory: "100Mi"
        command: ["stress"]
        args: ["-c", "2"]
```

```
$ kubectl apply -f deployment-requests.yaml 
deployment.apps/pods-request created

$ kubectl get pod -o wide
NAME                            READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
pods-request-5f6b4fd46b-l7ztl   1/1     Running   0          33m   10.244.1.5   minikube-m02   <none>           <none>
pods-request-5f6b4fd46b-nw2tg   0/1     Pending   0          33m   <none>       <none>         <none>           <none>
pods-request-5f6b4fd46b-pjc5f   0/1     Pending   0          33m   <none>       <none>         <none>           <none>
pods-request-5f6b4fd46b-t6x6m   1/1     Running   0          33m   10.244.1.4   minikube-m02   <none>           <none>
pods-request-5f6b4fd46b-z6hjb   1/1     Running   0          33m   10.244.1.6   minikube-m02   <none>           <none>
```



## クリーンナップ
```
$ minikube delete
```

## 参考リンク
- Resource Management for Pods and Containers https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
- Assign Memory Resources to Containers and Pods https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/
- Assign CPU Resources to Containers and Pods https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/
- Resize CPU and Memory Resources assigned to Containers https://kubernetes.io/docs/tasks/configure-pod-container/resize-container-resources/
- Configure Quality of Service for Pods https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/
