## CICD

GitHub Actionsで、minikube を実行して、
コードを修正したら、ビルドとテストを自動実施する。


https://minikube.sigs.k8s.io/docs/tutorials/setup_minikube_in_github_actions/


GitHub Actions 上で　
コンテナをビルドして、minikube を起動して、実行するまでを演習する。

Dockerfileで、ARM と ADMDを区別しなくても良いようにする。

docker pull maven:3.9.6-eclipse-temurin-21-jammy




以下を追加する

CI GitHub Actions
CD ArgoCD　shield secret 





## ArgoCDのインストール
mini:~ takara$ kubectl create namespace argocd
namespace/argocd created
mini:~ takara$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

## ArgoCDのコンソールにアクセスする
mini:~ takara$ kubectl port-forward service/argocd-server -n argocd 8090:80
Forwarding from 127.0.0.1:8090 -> 8080
Forwarding from [::1]:8090 -> 8080

## コンソールのパスワード取得
mini:~ takara$ kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
ilihlcbO4QUykiZY

ユーザー：admin、パスワード：上記で入る。


## Seald Secretをインストールする。

$ helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
"sealed-secrets" has been added to your repositories


$ helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets
NAME: sealed-secrets
LAST DEPLOYED: Tue Jan 16 09:28:23 2024
NAMESPACE: kube-system
STATUS: deployed
REVISION: 1
TEST SUITE: None
NOTES:
** Please be patient while the chart is being deployed **

You should now be able to create sealed secrets.

1. Install the client-side tool (kubeseal) as explained in the docs below:

    https://github.com/bitnami-labs/sealed-secrets#installation-from-source

2. Create a sealed secret file running the command below:

    kubectl create secret generic secret-name --dry-run=client --from-literal=foo=bar -o [json|yaml] | \
    kubeseal \
      --controller-name=sealed-secrets-controller \
      --controller-namespace=kube-system \
      --format yaml > mysealedsecret.[json|yaml]

The file mysealedsecret.[json|yaml] is a commitable file.

If you would rather not need access to the cluster to generate the sealed secret you can run:

    kubeseal \
      --controller-name=sealed-secrets-controller \
      --controller-namespace=kube-system \
      --fetch-cert > mycert.pem

to retrieve the public cert used for encryption and store it locally. You can then run 'kubeseal --cert mycert.pem' instead to use the local cert e.g.

    kubectl create secret generic secret-name --dry-run=client --from-literal=foo=bar -o [json|yaml] | \
    kubeseal \
      --controller-name=sealed-secrets-controller \
      --controller-namespace=kube-system \
      --format [json|yaml] --cert mycert.pem > mysealedsecret.[json|yaml]

3. Apply the sealed secret

    kubectl create -f mysealedsecret.[json|yaml]

Running 'kubectl get secret secret-name -o [json|yaml]' will show the decrypted secret that was generated from the sealed secret.

Both the SealedSecret and generated Secret must have the same name and namespace.





$ helm list -n kube-system
NAME          	NAMESPACE  	REVISION	UPDATED                             	STATUS  	CHART                	APP VERSION
sealed-secrets	kube-system	1       	2024-01-16 09:28:23.593848 +0900 JST	deployed	sealed-secrets-2.14.1	v0.24.5    



## kubesealed コマンドのインストール

mini:~ takara$ vi .bash_profile 
mini:~ takara$ echo $PATH
/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Users/takara/bin
mini:~ takara$ vi .bash_profile 
mini:~ takara$ . .bash_profile 
mini:~ takara$ kubeseal --fetch-cert > cert.pem

$ kubeseal --fetch-cert > cert.pem
$ cat cert.pem 
-----BEGIN CERTIFICATE-----
MIIEzTCCArWgAwIBAgIRAOFSu0N+4JuGss5PN7niyeMwDQYJKoZIhvcNAQELBQAw
ADAeFw0yNDAxMTUxMjE3MTBaFw0zNDAxMTIxMjE3MTBaMAAwggIiMA0GCSqGSIb3
DQEBAQUAA4ICDwAwggIKAoICAQCpT6EF2aNRAim3SFu8Lq2MCcokHUrsGkcE16fr
WoO8X8xG3xZUGoWWF72bD9pUBrW29Mceooir3ipNWhzDY9OKBRc+AT2m+FCwcmub
nORpT+aqBHDOTR7zTpzmQcgAPgImp1pKZJfJOHdtYtrj00hDUrXfFhAzG/cZe2WI
O1NfL+UAlngIjde8cMw+p6pclwEQ0+MLiKY7nSvwtJGQcenUlC8OUYk3+RCvLn1Y
+xiCwCckFmerjnBo1ECFJitxnl4WGm007uG9qboXDZIG3ZXNGpWnY6+rOayw0g0B
GEz5phWhe2r674jpJy2IO0stpjbXuycXTeYVSSl7ZUllg53IZRGmfAHVqhLmrha+
RRhPWhFJ4usdY0LqLfsI3+sD9YMHlDtgjb3MFO0a2j6AAT/u07Y9U8ps6dhzC5wH
gS1x/SDJlmaXn2ghROWKm4Pckpad/A7jziB/rQUETOx+MqanxwUCY8oQFlpwxaOc
A+P8Qrpzfplp1Q8l7okxma4M/d8nDChHtUuN1bxntEmLkXfbuqKdHTA/19yKCKhX
1absJ7ic+7gHBI6dgZ2QfEfEDjB8mU18jhYqtt6NitVt7YbyDS0DUcxwrnwrHCXq
miURRZ4Rd8ScJs3tZ7Dg/yUp8rJQZWzrObT6Te6MPw8h9eVhti2jmh5a5FGC/xnB
gKD4+QIDAQABo0IwQDAOBgNVHQ8BAf8EBAMCAAEwDwYDVR0TAQH/BAUwAwEB/zAd
BgNVHQ4EFgQULsFDZKNl6e4dRIXkRFj80EPYkTIwDQYJKoZIhvcNAQELBQADggIB
AKFoRXOvAt/aeE6Wmrd1NYSRaEet/+4Id0dFf15/8gq8VOHmS5OXF3Qne5Mgg1nH
+o/l4yDMUg2lJzrO1o5TiIkxPwvfNzGa+7QrgP0jgbDwdJrq2dPzsCizKAo89jaD
TGmVXmL4kTrXVdWlD7cOruIAPnSDBHtgA2mHLYYut7IqJQ/p2D2+IzdM5lzPn8bj
Q/NkxHt1phC1Zjb+3dOJFS7Erf/TFyaApJa0JuF7Ws+jIPZqqvKXTt/FNWT6cRDP
ScKICe8PcChcQlaBW66Ihp6KNuTHdcM7socyoasiDtgcCKVcfSLDc1QeVEpy1V0L
jOhxaX7L6sAliBBP3E8GgL5mx6tpGWOSo0ArrdWV4osCS+IMkurtX7uEZP+F581S
uYl2FHvDGOaJ+7fLjK/FeEOnFoIaK3Bu3eNvoWZizRKS3KNFvEyiokgUuQQxjR+p
8zl0Biqd2EcsheYQ9IjwaP3q0DuXfYb2hdUVOzyt7G88zm3H5Ec0wP8wV1fEvJpz
CHkKCfM5iaV9Maohb3VJaPVMeumIK1u+2Nd9rd8fxFlpqZY4CauvTi5IasPC7sWA
PaTn0NVerLGq6xRnqUKLGKCjgfwEJQ6+sRAV369hqkEAaiGPgvU+oZDl1QcAxRhZ
P56OWAULHIUbvDNAxO3PL2Dyftm8WIC3zlTBsW8qom5N
-----END CERTIFICATE-----


後からマニフェストを書き換えると無効になるので、生成時にネームスペースを指定しなければならない。

$ kubeseal --format=yaml -n sandbox --cert=cert.pem < secret.yaml > sealed-secret.yaml


mini:4-7_CICD takara$ kubeseal --format=yaml --cert=cert.pem < secret.yaml 
---
apiVersion: bitnami.com/v1alpha1
kind: SealedSecret
metadata:
  creationTimestamp: null
  name: dotfile-secret
  namespace: default
spec:
  encryptedData:
    .secret-file: AgAMU3i7YmpwzPamIdqyhBtQ7UnaswM5B/DoNJ0crH5ieiG0Q6L0cMfGagZksc40SVx6JdKonW4fiUHBnazJnbY48OnTmf7LIugUUawocV6LbtjY56sYALUSVjbQTtsvt4v3N1A7IaXrj7LEICPfTd840UM4NueW7iHjrJRlBoxQxH1kKCmY5EAYiJxqFTYaUrNa/TO2ejEwnkzDhNJbESxGZMH7dVPRfchKs+nTfQqWcsCeceN4JV2aqWi3ydRxp48ZA43fEcFCIuAN5QOZjC3n9gLCt6QoClP9+FKKkhSVGtGI2o81DsKj/bjZTVBzFp+Z0h7dU/h2pBNEz+8aqYUA62bjcplt5wZL87nJKJrsJL7+Dpye4fRtH3BzVI/+oX1Map3I4FCvXRZSZNmSl/jyRLGiiNuXb5Sjd4RTSzIP3bBgW0blUt5xzyUl+Bka8uLbuOANIUkdHp5BZHIRuhxtG556yiY6I1heH58x5/2UyL4He+V98A/gdn6W2swpnfeH19yJxaD50MmgiVwmgkgDq0mnW6bymy06Ne+gweoJRvRM6ELUBKU79fvzzxJglk/mxr/Z13IgL/CZBcU6dOeYNj/+htnz2M4empDXQvvBojcUK73kgj71OBrazPJddo3Eb7d2MVpnrOv5Lj8oGERkhFaEMuw2yLjGeZAmOCW94DkQCOcLeplr0SYId0Rb+927ZkR17rSFB1g37g==
  template:
    metadata:
      creationTimestamp: null
      name: dotfile-secret
      namespace: default


https://qiita.com/butterv/items/877b0a499becbabf3398



Unable to delete application: error patching application with finalizers: Application.argoproj.io "secret" is invalid: metadata.finalizers: Forbidden: no new finalizers can be added if the object is being deleted, found new finalizers []string{"resources-finalizer.argocd.argoproj.io/background"}



# 証明書だけを取り出す
brew install python-yq

yq '.items[].data."tls.crt"' sealed-secrets-key.yaml|sed 's/"//g'  |base64 -d




https://zenn.dev/ring_belle/articles/argocd-notification-configure

xoxb-29787719972-6463030610839-R2bb91e1S00BPL2ApbZGeMfA

User OAuth Token
xoxp-29787719972-29787719988-6480913580004-d6e1b26ec4dfaa35e86c2459328fc791

Bot User OAuth Token
xoxb-29787719972-6463030610839-R2bb91e1S00BPL2ApbZGeMfA


# ArgoCD Notification

~~~
$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/release-1.0/manifests/install.yaml
$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj-labs/argocd-notifications/release-1.0/catalog/install.yaml


KUBE_EDITOR=vim kubectl edit cm nginx-config
$ KUBE_EDITOR=vim kubectl edit cm -n argocd argocd-notifications-cm
~~~

The AppProject referenced by the .spec.project field of the Application must have the namespace listed in its .spec.sourceNamespaces field. 




## ArgoCD 2.8.6 + ArogCD Notifications

~~~
curl -OL https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.6/manifests/install.yaml
curl -OL https://raw.githubusercontent.com/argoproj/argo-cd/v2.8.6/notifications_catalog/install.yaml




$ kubectl create namespace argocd
$ kubectl apply -n argocd -f argocd-2-8-6-install.yaml
$ kubectl apply -n argocd -f argocd-notif-2-8-6-install.yaml
$ kubectl apply -n argocd -f ../secret-for-argocd-notification.yaml
$ kubectl apply -n argocd -k argocd-server-applications

$ kubectl port-forward service/argocd-server -n argocd 8090:80
$ kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo

$ kubectl create ns guestbook
$ kubectl create ns app-team-one
$ kubectl create ns app-team-two
~~~



## ArgoCD 2.10 のテスト


mini:argo-cd-test takara$ kubectl get no
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   12s   v1.28.3


kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v2.10.0-rc3/manifests/install.yaml

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/notifications_catalog/install.yaml




argo-cd-2-10-test/


kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
XPKjNIiBqN0WOfXN


kubectl apply -n argocd -f ../secret-for-argocd-notification.yaml
KUBE_EDITOR=vim kubectl edit cm -n argocd argocd-notifications-cm



# ここから始め


$ kubectl create ns guestbook
$ kubectl create ns app-team-one
$ kubectl create ns app-team-two


$ kubectl create namespace argocd
$ kubectl apply -n argocd -f argo-cd-2-10-test/install-1.yaml 
$ kubectl apply -n app-team-one -f argo-cd-2-10-test/install-2.yaml
$ kubectl apply -n app-team-one -f secret-for-argocd-notification.yaml
$ kubectl apply -n argocd -f argo-cd-2-10-test/appproject.yaml

$ kubectl apply -k argo-cd-2-10-test


$ kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
$ kubectl port-forward service/argocd-server -n argocd 8090:80


Unable to sync: error setting app operation: error updating application "guestbook": applications.argoproj.io "guestbook" is forbidden: User "system:serviceaccount:argocd:argocd-server" cannot update resource "applications" in API group "argoproj.io" in the namespace "app-team-one"


mini:argo-cd-2-10-test takara$ diff -u install-1.yaml upstream/install-1.yaml 
--- install-1.yaml	2024-01-24 16:02:58
+++ upstream/install-1.yaml	2024-01-24 15:50:30
@@ -20993,9 +20993,6 @@
     app.kubernetes.io/name: argocd-cmd-params-cm
     app.kubernetes.io/part-of: argocd
   name: argocd-cmd-params-cm
-data:
-  application.namespaces: app-team-one, app-team-two
-  notificationscontroller.selfservice.enabled: "true"
 ---
 apiVersion: v1
 kind: ConfigMap
@@ -21561,8 +21558,6 @@
       containers:
       - args:
         - /usr/local/bin/argocd-notifications
-        - --application-namespaces="*"
-        - --self-service-notification-enabled
         env:
         - name: ARGOCD_NOTIFICATIONS_CONTROLLER_LOGFORMAT
           valueFrom:
@@ -22028,7 +22023,6 @@
       containers:
       - args:
         - /usr/local/bin/argocd-server
-        - --application-namespaces="*"
         env:
         - name: ARGOCD_SERVER_INSECURE
           valueFrom:
@@ -22369,7 +22363,6 @@
       containers:
       - args:
         - /usr/local/bin/argocd-application-controller
-        - --application-namespaces="*"
         env:
         - name: ARGOCD_CONTROLLER_REPLICAS
           value: "1"


mini:argo-cd-2-10-test takara$ diff -u install-2.yaml upstream/install-2.yaml 
--- install-2.yaml	2024-01-24 16:05:24
+++ upstream/install-2.yaml	2024-01-24 15:50:35
@@ -1,7 +1,5 @@
 apiVersion: v1
 data:
-  service.slack: |
-    token: $slack-token
   template.app-created: |
     email:
       subject: Application {{.app.metadata.name}} has been created.


  
mini:argo-cd-2-10-test takara$ kubectl get secret -n app-team-one
NAME                          TYPE     DATA   AGE
argocd-notifications-secret   Opaque   1      19m
mini:argo-cd-2-10-test takara$ kubectl get cm -n app-team-one
NAME                      DATA   AGE
argocd-notifications-cm   17     20m
kube-root-ca.crt          1      22m


