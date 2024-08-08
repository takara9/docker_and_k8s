# 継続的デリバリー(Contiious Distribution)

ArgoCDで継続デリバリーを体験してみます。


## 準備

```
$ minikube start
$ minikube addons enable csi-hostpath-driver
```


## ArgoCDのインストール

ArgoCDをデプロイ
```
$ kubectl create namespace argocd
$ kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
$ kubectl get po -n argocd
```

ArgoCDのコンソールにアクセスするために、ポートフォワードします。この画面はそのままにします。
```
$ kubectl port-forward service/argocd-server -n argocd 8080:80
```

## コンソールのパスワード取得
別のターミナルを開いて、コマンド実行で、ArgoCDのWeb画面にログインするための、パスワードが表示されます。
```
$ kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
```
ブラウザから、http://localhost:8080/ アクセスして、ユーザー：admin と上記で表示されたパスワードをインプットして、ログインします。

## ArgoCDへリポジトリの登録
メニューから移動 Setting -> Repositories -> CCNNECT REPO

Choose your connection method: 

  VIA HTTPS　に変更

CONNECT REPO USING HTTPS 
  Type: git
  Project: default
  Repository URL https://github.com/takara9/docker_and_k8s.git



## シールドシークレットのインストールと秘密鍵の復元

ArgoCDでは、GitHub上のマニフェストで、Kubernetesクラスタへアプリケーションをデプロイします。
そのため、シークレットに記載されたパスワードやトークンが外部から参照しても、外部へ漏洩しないように、シールドシークレットで暗号化します。

ローカルPCにレポジトリが登録されていな初回だけ実行します。
```
$ helm repo add sealed-secrets https://bitnami-labs.github.io/sealed-secrets
```

シールドシークレットを起動して、秘密鍵をリストアします。
```
$ helm install sealed-secrets -n kube-system --set-string fullnameOverride=sealed-secrets-controller sealed-secrets/sealed-secrets
$ kubectl apply -f private/sealed-secrets-key.yaml 
$ kubectl get po -n kube-system
$ kubectl rollout restart -n kube-system deploy/sealed-secrets-controller
```



## シールドシークレットを使ってシークレットを暗号化　（オプション）

kubesealコマンドのインストールは、参考資料を見てインストールしてください。
暗号化のための証明書を、デプロイ先となるK8sクラスタから取り出します。
```
$ kubeseal --fetch-cert > cert.pem
```

パスワードが記述されたステージング用と本番用のシークレットを、それぞれ暗号化します。
```
$ kubeseal --format=yaml -n stage --cert=cert.pem < private/secret.yaml > webservice-system/overlays/stage/secret-encrypted.yaml 
$ kubeseal --format=yaml -n prod --cert=cert.pem  < private/secret.yaml > webservice-system/overlays/prod/secret-encrypted.yaml 
```

## ArgoCDのアプリケーション登録

ArgoCDに、アプリケーションを登録するマニフェストを登録します。

ステージング用
```
$ kubectl apply -f application-stage.yaml
```

本番用
```
$ kubectl apply -f application-prod.yaml
```


## クリーンナップ

```
$ minikube delete
```



## 参考資料
- https://argoproj.github.io/cd/
- https://github.com/bitnami-labs/sealed-secrets
- https://sealed-secrets.netlify.app/


