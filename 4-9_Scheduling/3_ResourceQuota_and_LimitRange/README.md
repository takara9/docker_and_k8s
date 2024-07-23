# リソースクオータとリミットレンジ
リソースクオータ（Resource Quota）は、ネームスペースのCPUとメモリの割り当て量を設定します。また、 リミットレンジ（Limit Range ）は、ネームスペースのデフォルトの要求量と上限を設定し、スケジュール時に自動的に設定を挿入します。

## 準備
```
$ minikube start
```


## リソースクオータ
リソースクォータがネームスペースに設定されていると、リソースが設定されていないとデプロイできない。
```
$ kubectl apply -f resourceQuota.yaml 
$ kubectl get quota
NAME            AGE    REQUEST                                       LIMIT
mem-cpu-limit   2m2s   requests.cpu: 0/1, requests.memory: 0/100Mi   limits.cpu: 0/2, limits.memory: 0/200Mi

$ kubectl run pod --image=ghcr.io/takara9/ex1:1.5 
Error from server (Forbidden): pods "pod" is forbidden: failed quota: mem-cpu-limit: must specify limits.cpu for: pod; limits.memory for: pod; requests.cpu for: pod; requests.memory for: pod
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
$ kubectl run pod --image=ghcr.io/takara9/ex1:1.5
$ kubectl get pod
NAME   READY   STATUS    RESTARTS   AGE
pod    1/1     Running   0          27s

$ kubectl get pod pod -o jsonpath='{.spec.containers[].resources}' |jq -r .
{
  "limits": {
    "cpu": "2",
    "memory": "200Mi"
  },
  "requests": {
    "cpu": "500m",
    "memory": "100Mi"
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

