# イングレス と Gateway API

イングレスとゲートウェイ APIは、クラスタ外部のリクエストを、クラスタ内の「サービス」へ導きます。
そして、負荷分散、暗号化、DNS名の仮想ホスティングを提供します。現在、イングレスの開発は終了しており、ゲートウェイ APIが推奨されています。


Gateway API は、以下の機能を提供する Ingress に替わる新機能です。
- カスタムリソースを使用したKubernetesの機能拡張
- ロードバランサーとの連携
- リクエストをクラスタ内部のサービスへの転送
- TLS暗号化と復号
- DNS名による仮想ホスティング
- リクエストトラフィックの割り合いによる分割

執筆時点では、Gateway APIを minikube で体験することができません。
将来、minikube用のゲートウェイクラスが実装されて、使用可能になれば、このリポジトリに追加したいと思います。


## 準備
最小構成でK8sクラスタを起動して、イングレスコントローラーを有効化します。
そして、アクセステスト用のポッドとサービスを起動しておきます。
```
$ minikube start
$ minikube addons enable ingress
```

```
$ kubectl apply -f pod_and_service.yaml
$ kubectl get svc
NAME          TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
bar-service   ClusterIP   10.103.194.71   <none>        9100/TCP   8s
foo-service   ClusterIP   10.99.200.181   <none>        8080/TCP   8s
kubernetes    ClusterIP   10.96.0.1       <none>        443/TCP    95s

$ kubectl get pod --show-labels
NAME      READY   STATUS    RESTARTS   AGE   LABELS
bar-app   1/1     Running   0          89s   app=bar
foo-app   1/1     Running   0          89s   app=foo

s takara$ kubectl get pods -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.containers[].image}{"\n"}{end}'
bar-app ghcr.io/takara9/ex1:1.5
foo-app kicbase/echo-server:1.0
```


## イングレス実行例
イングレスのオブジェクトをデプロイします。
```
$ kubectl apply -f ingress.yaml 
$ kubectl get ingress
NAME         CLASS   HOSTS         ADDRESS   PORTS   AGE
my-ingress   nginx   foo.bar.com             80      8s
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
```
$ curl --resolve "foo.bar.com:80:127.0.0.1"  http://foo.bar.com/bar/info
Host Name: bar-app
Host IP: 10.244.0.6
Client IP : 10.244.0.5

$ curl --resolve "foo.bar.com:80:127.0.0.1"  http://foo.bar.com/foo
Request served by foo-app

HTTP/1.1 GET /

Host: foo.bar.com
Accept: */*
User-Agent: curl/8.6.0
X-Forwarded-For: 10.244.0.1
X-Forwarded-Host: foo.bar.com
X-Forwarded-Port: 80
X-Forwarded-Proto: http
X-Forwarded-Scheme: http
X-Real-Ip: 10.244.0.1
X-Request-Id: 081dd9a168a9ecd20680aa8e8ef6f3f4
X-Scheme: http
```

 
 IPアドレス直打ちで確認します。
 /fooは設定があるので、転送されて応答がありますが、/barは設定がないので、「404 Not Found」となりました。
```
$ curl http://127.0.0.1/foo
Request served by foo-app

HTTP/1.1 GET /

Host: 127.0.0.1
Accept: */*
User-Agent: curl/8.6.0
X-Forwarded-For: 10.244.0.1
X-Forwarded-Host: 127.0.0.1
X-Forwarded-Port: 80
X-Forwarded-Proto: http
X-Forwarded-Scheme: http
X-Real-Ip: 10.244.0.1
X-Request-Id: 7ea44b3faf8a5955dc72387d02961f6c
X-Scheme: http

$ curl http://127.0.0.1/bar/info
<html>
<head><title>404 Not Found</title></head>
<body>
<center><h1>404 Not Found</h1></center>
<hr><center>nginx</center>
</body>
</html>
```


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