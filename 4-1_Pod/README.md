# ポッドとサービス

ポッド起動の基本と、ポッドへアクセスするためのサービスの基本をみていきます。



★重要　ポッドの部分に組み込む

プライベートレジストリから、コンテナイメージをプルする時のユーザーパスワード

パーソナルアクセストークン(classic) を取得する
https://github.com/settings/tokens


実行例 4.1.5 8　シークレットの作成
export YOUR_GITHUB_USERNAME=<your_account_id>
export YOUR_GITHUB_TOKEN=<your personal account token>
export YOUR_EMAIL=<your emal address >
kubectl create secret docker-registry ghcr-login-secret --docker-server=https://ghcr.io --docker-username=$YOUR_GITHUB_USERNAME --docker-password=$YOUR_GITHUB_TOKEN --docker-email=$YOUR_EMAIL


実行例 4.1.5 9　コンフィグマップとポッドの適用
apiVersion: v1
kind: Pod
metadata:
  name: my-java
spec:
  containers:
  - name: java
    image: ghcr.io/takara9/ex5:1.0
  imagePullSecrets:
  - name: ghcr-login-secret


