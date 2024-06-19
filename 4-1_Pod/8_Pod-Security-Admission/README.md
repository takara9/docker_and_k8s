# ポッド・セキュリティ・アドミッション
ポッド・セキュリティ・アドミッションは、ポッド・セキュリティ標準に準拠に従う様に、警告発生や実行拒否をします


## 準備
```
$ minikube start
$ kubectl get no
```


## ポッドセキュリティアドミッション
ポッドセキュリティスタンダードに準拠するように制御
このルール違反した場合、エラー発生、ポッドの実行を拒否するなど選択可能


ルールを設定したネームスペースに、違反するポットをデプロイ、エラー発生でデプロイ失敗
```
$ kubectl apply -f ns_restricted.yaml 

$ kubectl apply -n my-namespace -f pod-fail-case.yaml 
Error from server (Forbidden): error when creating "pod-fail-case.yaml": pods "hostpathvolumes1" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), restricted volume types (volumes "volume-hostpath-a", "volume-hostpath-b" use restricted volume type "hostPath"), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```


ルールを設定していないネームスペースにデプロイ、エラーなく、デプロイ成功
```
$ kubectl apply -f pod-fail-case.yaml 
pod/hostpathvolumes1 created
```


# クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/security/pod-security-standards/
- https://kubernetes.io/docs/concepts/security/pod-security-admission/
- https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/pod-security-admission/test/testdata
