# ポッド・セキュリティ・コンテキスト
ポッド・セキュリティ・コンテキストは、コンテナ実行時のユーザーID,グループIDを強制的に変更して、アクセス権限を変更します。


## 準備
```
$ minikube start
$ kubectl get no
```

## 制限しないポッドの例

DockerHubに登録されたコンテナでは、rootユーザーの権限でコマンドが実行
```
$ kubectl run -it my-pod-1 --image=ubuntu:latest -- bash
If you don't see a command prompt, try pressing enter.
root@my-pod-1:/# id
uid=0(root) gid=0(root) groups=0(root)
```

コンテナのビルド時に実行ユーザーIDを指定することもできる
```
$ kubectl run -it my-pod-2 --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
nobody@my-pod-2:/$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
```


## ポッドセキュリティコンテキスト
コンテナの実行時のユーザーIDなどを強制する。また、ルート権限の実行を禁止する。

pod-sc-uid.yaml(抜粋)
```
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
```

実行例
```
$ kubectl apply -f pod-sc-uid.yaml 
$ kubectl exec -it my-pod-3 -- bash
groups: cannot find name for group ID 1000

I have no name!@my-pod:/$ id
uid=1000 gid=1000 groups=1000

I have no name!@my-pod:/$ touch /mnt/test

I have no name!@my-pod:/$ ls -la /mnt/test
-rw-r--r-- 1 1000 1000 0 Jun  4 22:07 /mnt/test
```


root権限の実行を排除する

pod-sc-nonroot.yaml(抜粋)
```
    spec:
      securityContext: # 実行時のユーザーIDを指定
        runAsNonRoot: true
```

```
$ kubectl apply -f pod-sc-nonroot.yaml 
$ kubectl get po　my-pod-4
NAME       READY   STATUS                       RESTARTS      AGE
my-pod-4   0/1     CreateContainerConfigError   0             48s
```

```
$ kubectl get pod my-pod-4 -o jsonpath='{.status.containerStatuses[]}'| jq -r .
{
  "image": "ubuntu:latest",
  "imageID": "",
  "lastState": {},
  "name": "my-container",
  "ready": false,
  "restartCount": 0,
  "started": false,
  "state": {
    "waiting": {
      "message": "container has runAsNonRoot and image will run as root (pod: \"my-pod-4_default(e68e8e28-4a5c-4598-a518-647e94905639)\", container: my-container)",
      "reason": "CreateContainerConfigError"
    }
  }
}
```



# クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
