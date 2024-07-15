# イングレス と Gateway API

イングレスとGateway APIは、Kubernetesクラスタ外部のリクエストと、クラスタ内のサービスへ導きます。
Ingress は、負荷分散、暗号化、DNS名の仮想ホスティングを提供します。

現在、Ingressのプロジェクトは終了しており、Gatwway API の使用が推奨されています。

Gateway API は、以下の機能を提供する Ingress に替わる新機能です。
- カスタムリソースを使用したKubernetesの機能拡張
- ロードバランサーとの連携
- リクエストをクラスタ内部のサービスへの転送
- TLS暗号化と復号
- DNS名による仮想ホスティング
- リクエストトラっフィックの分割割合

執筆時点では、Gateway APIを minikube で体験することができません。
将来、minikube用のゲートウェイクラスが実装されて、使用可能になれば、このリポジトリに追加したいと思います。


## 準備
最小構成でK8sクラスタを起動して、イングレスコントローラーを有効化します。
そして、アクセステスト用のポッドとサービスを起動しておきます。
```
$ minikube start
$ minikube addons enable ingress
$ kubectl apply -f pod_and_service.yaml
```


## イングレス実行例
イングレスのオブジェクトをデプロイします。
```
$ kubectl apply -f ingress.yaml 
$ kubectl get ingress
NAME              CLASS   HOSTS   ADDRESS        PORTS   AGE
example-ingress   nginx   *       192.168.49.2   80      10s
```

イングレスのポートへアクセスするために、トンネルを起動します。
イングレスコントローラーは、パソコンの特権ポート 80を使用するので、パスワードの入力が必要です。
```
$ minikube tunnel
✅  トンネルが無事開始しました

📌  注意: トンネルにアクセスするにはこのプロセスが存続しなければならないため、このターミナルはクローズしないでください ...

❗  my-ingress service/ingress は次の公開用特権ポートを要求します:  [80 443]
🔑  sudo permission will be asked for it.
🏃  my-ingress サービス用のトンネルを起動しています。
Password: ********
```
以降は、別ターミナルでアクセスする。



### IPドレスでアクセスするケース
```
$ curl http://127.0.0.1/foo
Request served by foo-app

HTTP/1.1 GET /foo
```

### DNS名でアクセスするケース

1. minikubeのドライバーに docker を使用している場合
```
curl --resolve "foo.bar.com:80:127.0.0.1" -i http://foo.bar.com/bar/info
curl --resolve "foo.bar.com:80:127.0.0.1" -i http://foo.bar.com/foo
```

2. 仮想マシンで minikube を起動している場合
```
curl --resolve "foo.bar.com:80:$( minikube ip )" -i http://foo.bar.com/bar/info
curl --resolve "foo.bar.com:80:$( minikube ip )" -i http://foo.bar.com/foo
```

リライトが無い場合
```
mini:4_Ingress takara$ curl --resolve "foo.bar.com:80:127.0.0.1" -i http://foo.bar.com/bar/info
HTTP/1.1 404 NOT FOUND
Date: Tue, 11 Jun 2024 22:03:20 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 207
Connection: keep-alive

<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```


MacOSでの実行例1
```
$ curl --resolve "foo.bar.com:80:127.0.0.1" -i http://foo.bar.com/bar/info
HTTP/1.1 200 OK
Date: Tue, 11 Jun 2024 21:56:28 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 62
Connection: keep-alive

Host Name: bar-app
Host IP: 10.244.0.7
Client IP : 10.244.0.5
```

MacOSでの実行例2
```
mini:4_Ingress takara$ curl --resolve "foo.bar.com:80:127.0.0.1" -i http://foo.bar.com/bar/ping;echo
HTTP/1.1 200 OK
Date: Tue, 11 Jun 2024 21:57:41 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 5
Connection: keep-alive

PONG!
```


## クリーンナップ
```
minikube delete
```


## 参考資料
Ingress
- https://kubernetes.io/docs/concepts/services-networking/ingress/
- https://minikube.sigs.k8s.io/docs/tutorials/nginx_tcp_udp_ingress/
- https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/
- https://kubernetes.github.io/ingress-nginx/examples/rewrite/

Gateway API
- https://kubernetes.io/blog/2023/10/31/gateway-api-ga/
- https://kubernetes.io/docs/concepts/services-networking/gateway/
- https://gateway-api.sigs.k8s.io/
- https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/#migrating-from-ingress


https://qiita.com/pqrst1987/items/4b944f4cb805e989915e