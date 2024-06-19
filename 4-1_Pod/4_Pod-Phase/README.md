# ポッドのフェーズ表示
ポッドのライフサイクルの状態を表示します。

## 準備
```
$ minikube start
$ kubectl get no
```


## 実行例
ポッドのフェーズ表示
```
$ kubectl run my-pod --image=ubuntu --restart=Never
pod/my-pod created
$ kubectl get pod my-pod -o jsonpath='{.status.phase}';echo
Succeeded
```

ポッド上のコンテナのステータス表示
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
- https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- https://kubernetes.io/docs/reference/kubectl/jsonpath/