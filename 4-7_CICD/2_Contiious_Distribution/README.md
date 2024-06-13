# ArgoCD で　CD を構築

## ArgoCDのインストール
```
$ kubectl create namespace argocd
namespace/argocd created
$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
## ArgoCDのコンソールにアクセスする
```
$ kubectl port-forward service/argocd-server -n argocd 8080:80
```

## コンソールのパスワード取得
```
$ kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
ilihlcbO4QUykiZY
```
ユーザー：admin、パスワード：上記で入る。

## シールドシークレットの設定を実施する

```
$ kubeseal --fetch-cert > cert.pem
$ kubeseal --format=yaml -n stage --cert=cert.pem < ./../../4-3_controller/4-3-5-System_Integration/webservice-system/overlays/stage/secret.yaml > webservice-system/overlays/stage/secret-encrypted.yaml 
$ kubeseal --format=yaml -n prod --cert=cert.pem < ./../../4-3_controller/4-3-5-System_Integration/webservice-system/overlays/prod/secret.yaml > webservice-system/overlays/prod/secret-encrypted.yaml 
```


```
$ minikube addons enable csi-hostpath-driver
$ cd webservice-system/
$ kubectl apply -k overlays/stage/
$ kubectl apply -k overlays/prod/
```

##
