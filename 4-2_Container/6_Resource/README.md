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
