# リソース制約
ポッド内コンテナのCPUとメモリの割り当て最低保証と上限値を設定することができます。
それにより、Kubernetesは適切なノードを選び、ポッドを配置できます。


## 準備
```
$ minikube start -n 2
$ minikube addons enable metrics-server
$ kubectl taint nodes minikube workload:NoSchedule
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


## CPUの要求と最大を設定する

## CPUの最大を超過した時の挙動





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
