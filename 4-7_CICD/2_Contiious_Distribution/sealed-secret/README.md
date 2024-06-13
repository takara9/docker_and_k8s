
## Seald Secretをインストールする。
```
$ helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
"sealed-secrets" has been added to your repositories
```

```
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
```


## kubesealed コマンドのインストール

```
$ vi .bash_profile 
$ echo $PATH
/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Users/takara/bin
$ vi .bash_profile 
$ . .bash_profile 
```

## 暗号化のための証明書を取り出す

```
$ kubeseal --fetch-cert > cert.pem
```

後からマニフェストを書き換えると無効になるので、生成時にネームスペースを指定しなければならない。
ネームスペースを設定しないで、適用時に指定することができない。そのため、必ずネームスペースを指定して作成しておく。

```
$ kubeseal --format=yaml -n sandbox --cert=cert.pem < secret.yaml > sealed-secret.yaml
$ kubectl create namespace sandbox
$ kubectl apply -f sealed-secret.yaml 

$ kubectl get secret -n sandbox
NAME              TYPE     DATA   AGE
user-and-passwd   Opaque   2      28s

$ kubectl get secret user-and-passwd -o yaml -n sandbox
apiVersion: v1
data:
  passwd: c2VjcmV0OTk5
  user-id: dXNlcjEyMw==
kind: Secret
metadata:
  creationTimestamp: "2024-05-15T21:58:27Z"
  name: user-and-passwd
  namespace: sandbox
  ownerReferences:
  - apiVersion: bitnami.com/v1alpha1
    controller: true
    kind: SealedSecret
    name: user-and-passwd
    uid: a7292cdf-584c-4b2d-922f-964b7a987925
  resourceVersion: "2444"
  uid: 3713a6e1-96e8-427e-9367-9e0fa4bdccfa
type: Opaque

$ echo c2VjcmV0OTk5 |base64 -d;echo
secret999
```


# K8sクラスタの再作成に備える

## 復号鍵を取り出す

```
$ kubectl get secret -n kube-system \
-l sealedsecrets.bitnami.com/sealed-secrets-key=active \
-o yaml > sealed-secrets-key.yaml 
```

クラスタを一度消去して、再作成する。そして、シールドシークレットも、再びデプロイする
バックアップしておいた鍵をデプロイして、シールドシークレットのコントローラーを再起動する

```
minikube delete
minikube start
helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets
kubectl appy -f sealed-secrets-key.yaml 
kubectl rollout restart -n kube-system deploy/sealed-secrets-controller
```

前の暗号化したシークレットを再デプロイして、復号して確認する

```
kubectl create namespace sandbox
kubectl apply -f sealed-secret.yaml 
```

```
$ kubectl get secret -n sandbox -o yaml
apiVersion: v1
items:
- apiVersion: v1
  data:
    passwd: c2VjcmV0OTk5
    user-id: dXNlcjEyMw==
  kind: Secret

$ echo c2VjcmV0OTk5 | base64 -d;echo
secret999
```

