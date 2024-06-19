# ポッド・セキュリティ・コンテキスト
ポッド・セキュリティ・コンテキストは、コンテナ実行時のユーザーID,グループIDを強制的に変更して、アクセス権限を変更します。


## 準備
```
$ minikube start
$ kubectl get no
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
$ kubectl apply -f pod-sc-1.yaml 
$ kubectl exec -it my-pod -- bash
groups: cannot find name for group ID 1000

I have no name!@my-pod:/$ id
uid=1000 gid=1000 groups=1000

I have no name!@my-pod:/$ touch /mnt/test

I have no name!@my-pod:/$ ls -la /mnt/test
-rw-r--r-- 1 1000 1000 0 Jun  4 22:07 /mnt/test
```


ルート以外で実行を強制する

pod-sc-nonroot.yaml(抜粋)
```
    spec:
      securityContext: # 実行時のユーザーIDを指定
        runAsNonRoot: true
```

コンテナ内で実行中プロセスのID（権限）を確認する
```
$ kubectl apply -f pod-sc-nonroot.yaml 
$ kubectl exec -it my-pod2 -- bash
nobody@my-pod2:/$ id
uid=65534(nobody) gid=65534(nogroup) groups=65534(nogroup)
nobody@my-pod2:/$ touch /mnt/test
nobody@my-pod2:/$ ls -la /mnt/test
-rw-r--r-- 1 nobody nogroup 0 Jun  4 22:18 /mnt/test
```


# クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
