# ポッド・セキュリティ・コンテキスト
ポッド・セキュリティ・コンテキストは、コンテナ実行時のユーザーID,グループIDを強制的に変更して、アクセス権限を変更します。


## 準備
```
$ minikube start
$ kubectl get no
```


## ポッドセキュリティコンテキスト
コンテナの実行時のユーザーIDなどを強制する。また、ルート権限の実行を禁止する。

pod-sc-1.yaml(抜粋)
```
<前略>
spec:
  securityContext:
    runAsUser: 1000
    runAsGroup: 1000
    fsGroup: 1000
<以下省略>
```

実行例
```
$ kubectl apply -f pod-sc-1.yaml 
pod/my-pod created
$ kubectl exec -it my-pod -- bash
groups: cannot find name for group ID 1000
I have no name!@my-pod:/$ id
uid=1000 gid=1000 groups=1000
I have no name!@my-pod:/$ touch /mnt/test
I have no name!@my-pod:/$ ls -la /mnt/test
-rw-r--r-- 1 1000 1000 0 Jun  4 22:07 /mnt/test
```


ルート以外で実行を強制する
```
<前略>
    spec:
      securityContext: # 実行時のユーザーIDを指定
        runAsNonRoot: true
<以下省略>
```

```
$ kubectl apply -f pod-sc-nonroot.yaml 
pod/my-pod2 created
$ kubectl exec -it my-pod2 -- bash
nobody@my-pod2:/$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
nobody@my-pod2:/$ touch /mnt/test
nobody@my-pod2:/$ ls -la /mnt/test
-rw-r--r-- 1 nobody nogroup 0 Jun  4 22:18 /mnt/test
```





## ポッドセキュリティアドミッション
ポッドセキュリティスタンダードに準拠する。
このルール違反した場合、エラー発生、ポッドの実行を拒否するなど選択できる。


ルールを設定したネームスペースに、違反するポットをデプロイする
```
$ kubectl apply -f ns_restricted.yaml 

$ kubectl apply -n my-namespace -f pod-fail-case.yaml 
Error from server (Forbidden): error when creating "pod-fail-case.yaml": pods "hostpathvolumes1" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), restricted volume types (volumes "volume-hostpath-a", "volume-hostpath-b" use restricted volume type "hostPath"), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

ルールを設定していないネームスペースにデプロイする
```
$ kubectl apply -f pod-fail-case.yaml 
pod/hostpathvolumes1 created
```


# クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
