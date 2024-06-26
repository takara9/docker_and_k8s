# 実行中ポッドのAPI表示
実行中ポッドの全てのAPIを表示します。
これには、statusの表示項目があり、ポッドのライフサイクルと内部のコンテナの状態も確認できます。


## 準備
```
$ minikube start
$ kubectl get no
```


## 実行中ポッドのAPI表示

```
$ kubectl get pod my-pod -o yaml
```

ポッドのステータスを抜き出して表示
```
$ kubectl get pod my-pod -o jsonpath='{.status}';echo
```

ポッドのステータスからフェースだけを抜き出して表示
```
$ kubectl get pod my-pod -o jsonpath='{.status.phase}';echo
```


ポッドのコンテナのステータスだけを抜き出して表示
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


## クリーンナップ
```
$ kubectl delete pod my-pod
$ minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/
- https://kubernetes.io/docs/reference/ 
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://kubernetes.io/docs/reference/kubectl/jsonpath/

