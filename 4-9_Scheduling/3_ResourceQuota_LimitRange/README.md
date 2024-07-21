# リソースクオータとリミットレンジ
ネームスペースのCPUとメモリの要求と制限を設定する。
- リソースクオータ: ResourceQuotaは、ネームスペースのCPUとメモリの消費量を決定します。
- リミットレンジ: リソースのデフォルトの要求/制限を設定し、実行時にそれらをコンテナーに自動的に挿入します。

## 準備
```
$ minikube start
```


## リソースクオータ
リソースクォータがネームスペースに設定されていると、リソースが設定されていないとデプロイできない。
```
$ kubectl apply -f resourceQuota.yaml 
$ kubectl get quota
NAME            AGE   REQUEST   LIMIT
mem-cpu-limit   33s             limits.cpu: 0/1, limits.memory: 0/1Gi

$ kubectl apply -f pod.yaml 
Error from server (Forbidden): error when creating "pod.yaml": pods "my-pod" is forbidden: failed quota: mem-cpu-limit: must specify limits.cpu for: container1; limits.memory for: container1; requests.cpu for: container1; requests.memory for: container1
```


## リミットレンジを設定することで、設定が自動的に埋め込まれ、デプロイできる様になる。
ネームスペースに、デフォルトのリソースを設定する。
```
$ kubectl apply -f limitRange.yaml 
$ kubectl get limits
NAME          CREATED AT
mem-min-max   2024-06-02T01:57:29Z
```

リミットレンジで設定したリソースの値が、ポッドに挿入されるので、デプロイできる。
```
 kubectl apply -f pod.yaml 
$ kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          55s

$ kubectl get pod my-pod -o jsonpath='{.spec.containers[].resources}' |jq -r .
{
  "limits": {
    "cpu": "1",
    "memory": "1Gi"
  },
  "requests": {
    "cpu": "100m",
    "memory": "256Mi"
  }
}
```


## クリーンナップ
```
minikube delete
```


## 参照資料
- https://kubernetes.io/docs/concepts/policy/resource-quotas/
- https://kubernetes.io/docs/concepts/policy/limit-range/

