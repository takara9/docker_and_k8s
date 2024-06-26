# ポッド・セキュリティ・アドミッション
ポッド・セキュリティ・アドミッションは、ポッド・セキュリティ標準に準拠に従う様に、警告発生や実行拒否をします


## 準備
```
$ minikube delete
$ mkdir -p ~/.minikube/files/etc/ssl/certs

$ cat <<EOF > ~/.minikube/files/etc/ssl/certs/audit-policy.yaml
# Log all requests at the Metadata level.
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
EOF

$ minikube start \
  --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml \
  --extra-config=apiserver.audit-log-path=-

$ kubectl get no
```



## ポッドセキュリティアドミッション
ポッドセキュリティスタンダードに準拠するように制御
このルール違反した場合、エラー発生、ポッドの実行を拒否するなど選択可能


```
$ kubectl apply -f ns_restricted.yaml 
$ kubectl get ns my-namespace --show-labels
NAME           STATUS   AGE     LABELS
my-namespace   Active   2m13s   kubernetes.io/metadata.name=my-namespace,pod-security.kubernetes.io/audit=restricted,pod-security.kubernetes.io/enforce=restricted,pod-security.kubernetes.io/warn=restricted
```

ルールを設定したネームスペースに、違反するポットをデプロイ、エラー発生でデプロイ失敗
```
$ kubectl run -it my-pod-1 -n my-namespace --image=ubuntu:latest -- bash
Error from server (Forbidden): pods "my-pod-1" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (container "my-pod-1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (container "my-pod-1" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or container "my-pod-1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or container "my-pod-1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```


# クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/security/pod-security-standards/
- https://kubernetes.io/docs/concepts/security/pod-security-admission/
- https://github.com/kubernetes/kubernetes/tree/master/staging/src/k8s.io/pod-security-admission/test/testdata
- https://minikube.sigs.k8s.io/docs/handbook/filesync/


