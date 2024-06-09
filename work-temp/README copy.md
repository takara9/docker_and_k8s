

# プロジェクテッドボリューム（シークレット）
シークレットをボリュームとして、ポッドからマウントします。

## 準備
```
$ minikube start
```


## 実行例
```
$ kubectl apply -f secret.yaml 
$ kubectl apply -f pod-secret.yaml 
```

```

```


```
$ kubectl get secret dotfile-secret
$ kubectl get pod pod-secret
```






mini:ex-1 takara$ kubectl create secret --help
Create a secret with specified type.

 A docker-registry type secret is for accessing a container registry.

 A generic type secret indicate an Opaque secret type.

 A tls type secret holds TLS certificate and its associated key.

Available Commands:
  docker-registry   Create a secret for use with a Docker registry
  generic           Create a secret from a local file, directory, or literal value
  tls               Create a TLS secret

Usage:
  kubectl create secret (docker-registry | generic | tls) [options]



# Dockerにログインします
docker login -u dockerhub-user -p <token>

# Dockerの認証情報を元にsecretを作成します
kubectl create secret generic dockerhub \
  --from-file=.dockerconfigjson=$HOME/.docker/config.json \
  --type=kubernetes.io/dockerconfigjson



    spec:
      containers:
      # ...
      imagePullSecrets:
        - name: locred





### Docker Hub
mini:~ takara$ docker login -u maho
Password: 
Login Succeeded

mini:~ takara$ kubectl create secret generic dockerhub \
>   --from-file=.dockerconfigjson=$HOME/.docker/config.json \
>   --type=kubernetes.io/dockerconfigjson
secret/dockerhub created

mini:~ takara$ kubectl get secret
NAME        TYPE                             DATA   AGE
dockerhub   kubernetes.io/dockerconfigjson   1      50s




$ kubectl create secret generic dockerhub2 --from-file=.dockerconfigjson=$HOME/.docker/config.json --type=kubernetes.io/dockerconfigjson --dry-run=client -o yaml
apiVersion: v1
data:
  .dockerconfigjson: ewoJImF1dGhzIjogewoJCSJnaGNyLmlvIjoge30sCgkJImh0dHBzOi8vaW5kZXguZG9ja2VyLmlvL3YxLyI6IHt9Cgl9LAoJImNyZWRzU3RvcmUiOiAiZGVza3RvcCIsCgkiY3VycmVudENvbnRleHQiOiAiZGVza3RvcC1saW51eCIKfQ==
kind: Secret
metadata:
  creationTimestamp: null
  name: dockerhub2
type: kubernetes.io/dockerconfigjson


### GHCR.IO

mini:~ takara$ echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
Login Succeeded

mini:~ takara$ kubectl create secret generic ghcr_cred     --from-file=.dockerconfigjson=$HOME/.docker/config.json     --type=kubernetes.io/dockerconfigjson --dry-run=client -o yaml
apiVersion: v1
data:
  .dockerconfigjson: ewoJImF1dGhzIjogewoJCSJnaGNyLmlvIjoge30sCgkJImh0dHBzOi8vaW5kZXguZG9ja2VyLmlvL3YxLyI6IHt9Cgl9LAoJImNyZWRzU3RvcmUiOiAiZGVza3RvcCIsCgkiY3VycmVudENvbnRleHQiOiAiZGVza3RvcC1saW51eCIKfQ==
kind: Secret
metadata:
  creationTimestamp: null
  name: regcred
type: kubernetes.io/dockerconfigjson


kubectl create secret generic ghcrcred --from-file=.dockerconfigjson=$HOME/.docker/config.json --type=kubernetes.io/dockerconfigjson
secret/ghcrcred created

mini:~ takara$ kubectl get secret
NAME        TYPE                             DATA   AGE
dockerhub   kubernetes.io/dockerconfigjson   1      12m
ghcrcred    kubernetes.io/dockerconfigjson   1      32s


## GHCR.IO からコンテナイメージを取得する。

パーソナルアクセストークン(classic) を取得する
https://github.com/settings/tokens


シークレットを作成する
kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=$YOUR_GITHUB_USERNAME --docker-password=$YOUR_GITHUB_TOKEN --docker-email=$YOUR_EMAIL


イメージを取り出してポッドが作れることを確認する


mini:ex-3 secret takara$ kubectl apply -f pod.yaml 
pod/my-java created

mini:ex-3 secret takara$ kubectl get po
NAME                 READY   STATUS    RESTARTS      AGE
configmap-demo-pod   1/1     Running   3 (32m ago)   3h32m
my-java              1/1     Running   0             77s


## コマンドラインからシークレットを作成

~~~
$ kubectl -n default create secret generic sample-secret \
--from-literal=MYSQL_HOST=localhost \
--from-literal=MYSQL_USER=root \
--from-literal=MYSQL_PASSWORD=password \
--dry-run=client \
-o yaml > secret.yaml
~~~




~~~
$ echo "Secret Strings" |base64
U2VjcmV0IFN0cmluZ3MK

$ echo U2VjcmV0IFN0cmluZ3MK |base64 -d
Secret Strings
~~~


Base64は、データを64種類の印字可能な英数字のみを用いて、それ以外の文字を扱うことの出来ない通信環境にてマルチバイト文字やバイナリデータを扱うためのエンコード方式である。
MIMEによって規定されていて、7ビットのデータしか扱うことの出来ない電子メールにて広く利用されている。
具体的には、A、…、Z、a、…、z、0、…、9 の62種類の文字[注釈 1]と、2種類の記号 (+、/)、さらにパディング（余った部分を詰める）のための記号として = が用いられる。

Base64は、64種類の７ビットで表現できる英数字で、マルチバイト文字やバイナリデータを扱うエンコード方式です。文字種の内訳は、A〜Z,a〜z,0〜9の62種類の文字、2種類の記号(+、/)で表現します。そして、余った部分を詰めるのためのパッティング記号(=)を使用します。



## クリーンナップ
```
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/storage/projected-volumes/
