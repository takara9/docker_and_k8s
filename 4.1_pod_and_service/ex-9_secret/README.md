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


