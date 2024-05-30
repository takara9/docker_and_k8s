
```
minikube delete
```

```
mkdir -p ~/.minikube/files/etc/ssl/certs
cat <<EOF > ~/.minikube/files/etc/ssl/certs/audit-policy.yaml
# Log all requests at the Metadata level.
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
EOF
```

## ネームスペースの準備

```
kubectl get no
kubectl apply -f ns_baseline.yaml
kubectl apply -f ns_privileged.yaml
kubectl apply -f ns_restricted.yaml
```


### K8s 1.27 のテスト

```
minikube start --kubernetes-version=v1.27.4 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-
```

バージョン確認とネームスペースの準備
```
$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   15s   v1.27.4
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -f ns_privileged.yaml
namespace/privileged created
$ kubectl apply -f ns_restricted.yaml
namespace/restricted created
```

### K8s-1.27 PSA機能テスト (ベースラインでパスするケース)

```
$ kubectl apply -n privileged -f sysctl-127-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n restricted -f sysctl-127-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-127-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```


### K8s-1.27 に対する 1.30 のルール適用 (ベースラインでパスするケース)

```
$ kubectl apply -n privileged -f sysctl-130-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)

$ kubectl apply -n restricted -f sysctl-130-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "restricted:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes), allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

##　1.28 PSC機能テスト

```
$ minikube start --kubernetes-version=v1.28.3 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-

$ kubectl get no
NAME       STATUS   ROLES           AGE     VERSION
minikube   Ready    control-plane   2m12s   v1.28.3

$ kubectl get ns
NAME              STATUS   AGE
baseline          Active   8s
default           Active   2m56s
kube-node-lease   Active   2m56s
kube-public       Active   2m56s
kube-system       Active   2m56s
privileged        Active   8s
restricted        Active   7s

$ kubectl apply -n privileged -f sysctl-128-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n restricted -f sysctl-128-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-128-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "restricted:latest": allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```

kubectl delete -n privileged -f sysctl-128-baseline-pass.yaml
kubectl delete -n baseline -f sysctl-128-baseline-pass.yaml
kubectl delete -n restricted -f sysctl-128-baseline-pass.yaml


### 1.30のルールを適用

```
$ kubectl apply -n privileged -f sysctl-130-baseline-pass.yaml
pod/sysctls1 created

$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)

$ kubectl apply -n restricted -f sysctl-130-baseline-pass.yaml
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "restricted:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes), allowPrivilegeEscalation != false (containers "initcontainer1", "container1" must set securityContext.allowPrivilegeEscalation=false), unrestricted capabilities (containers "initcontainer1", "container1" must set securityContext.capabilities.drop=["ALL"]), runAsNonRoot != true (pod or containers "initcontainer1", "container1" must set securityContext.runAsNonRoot=true), seccompProfile (pod or containers "initcontainer1", "container1" must set securityContext.seccompProfile.type to "RuntimeDefault" or "Localhost")
```





minikube start --kubernetes-version=v1.29.3 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-



```
$ minikube start --kubernetes-version=v1.30.0 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-

$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   18s   v1.30.0

$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -f ns_privileged.yaml
namespace/privileged created
$ kubectl apply -f ns_restricted.yaml
namespace/restricted created

$ kubectl get ns
NAME              STATUS   AGE
baseline          Active   8s
default           Active   64s
kube-node-lease   Active   64s
kube-public       Active   64s
kube-system       Active   64s
privileged        Active   8s
restricted        Active   7s
```


```
kubectl apply -n privileged -f sysctl-127-baseline-pass.yaml    pass
kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml      pass
kubectl apply -n restricted -f sysctl-127-baseline-pass.yaml    fail

kubectl delete ns baseline 
kubectl delete ns privileged
kubectl delete ns restricted

kubectl apply -f ns_baseline.yaml
kubectl apply -f ns_privileged.yaml
kubectl apply -f ns_restricted.yaml

kubectl apply -n privileged -f sysctl-128-baseline-pass.yaml    pass
kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml      pass
kubectl apply -n restricted -f sysctl-128-baseline-pass.yaml    fail

kubectl delete ns baseline 
kubectl delete ns privileged
kubectl delete ns restricted

kubectl apply -f ns_baseline.yaml
kubectl apply -f ns_privileged.yaml
kubectl apply -f ns_restricted.yaml

kubectl apply -n privileged -f sysctl-129-baseline-pass.yaml    pass
kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml      pass
kubectl apply -n restricted -f sysctl-129-baseline-pass.yaml    fail

kubectl delete ns baseline 
kubectl delete ns privileged
kubectl delete ns restricted

kubectl apply -f ns_baseline.yaml
kubectl apply -f ns_privileged.yaml
kubectl apply -f ns_restricted.yaml

kubectl apply -n privileged -f sysctl-130-baseline-pass.yaml    pass
kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml      pass
kubectl apply -n restricted -f sysctl-130-baseline-pass.yaml    fail
```





minikube start --kubernetes-version=v1.27.4 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-
kubectl get no
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
minikube delete




## 下位バージョンに対する課題検討


$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   36s   v1.27.4

$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
Error from server (Forbidden): error when creating "sysctl-129-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)






minikube start --kubernetes-version=v1.28.3 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-
kubectl get no
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
minikube delete


$ kubectl get no
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   100s   v1.28.3
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
Error from server (Forbidden): error when creating "sysctl-129-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
Error from server (Forbidden): error when creating "sysctl-130-baseline-pass.yaml": pods "sysctls1" is forbidden: violates PodSecurity "baseline:latest": forbidden sysctls (net.ipv4.tcp_keepalive_time, net.ipv4.tcp_fin_timeout, net.ipv4.tcp_keepalive_intvl, net.ipv4.tcp_keepalive_probes)



minikube start --kubernetes-version=v1.29.3 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-
kubectl get no
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
minikube delete



$ 
$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   14s   v1.29.3
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
pod/sysctls1 created
$ minikube delete




minikube start --kubernetes-version=v1.30.0 --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml --extra-config=apiserver.audit-log-path=-
kubectl get no
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
kubectl delete ns baseline
kubectl apply -f ns_baseline.yaml
kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
minikube delete


$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   29s   v1.30.0
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-127-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-128-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-129-baseline-pass.yaml 
pod/sysctls1 created
$ kubectl delete ns baseline
namespace "baseline" deleted
$ kubectl apply -f ns_baseline.yaml
namespace/baseline created
$ kubectl apply -n baseline -f sysctl-130-baseline-pass.yaml 
pod/sysctls1 created