
minikube addons enable ingress



mini:ex-4_ingress takara$ vi ingress.yaml
mini:ex-4_ingress takara$ kubectl apply -f ingress.yaml 
pod/foo-app created
service/foo-service created
pod/bar-app created
service/bar-service created
ingress.networking.k8s.io/example-ingress created
mini:ex-4_ingress takara$ kubectl get ingress
NAME              CLASS   HOSTS   ADDRESS        PORTS   AGE
example-ingress   nginx   *       192.168.49.2   80      10s

mini:~ takara$ minikube tunnel
✅  トンネルが無事開始しました

📌  注意: トンネルにアクセスするにはこのプロセスが存続しなければならないため、このターミナルはクローズしないでください ...

❗  example-ingress service/ingress は次の公開用特権ポートを要求します:  [80 443]
🔑  sudo permission will be asked for it.
🏃  example-ingress サービス用のトンネルを起動しています。
Password:



別ターミナルでアクセスする
mini:ex-4_ingress takara$ curl http://127.0.0.1/foo
Request served by foo-app

HTTP/1.1 GET /foo

Host: 127.0.0.1
Accept: */*
User-Agent: curl/8.4.0
X-Forwarded-For: 10.244.120.64
X-Forwarded-Host: 127.0.0.1
X-Forwarded-Port: 80
X-Forwarded-Proto: http
X-Forwarded-Scheme: http
X-Real-Ip: 10.244.120.64
X-Request-Id: 054773f103473694964c4a288e1c7b8a
X-Scheme: http


mini:ex-4_ingress takara$ curl http://127.0.0.1/bar
Request served by bar-app

HTTP/1.1 GET /bar

Host: 127.0.0.1
Accept: */*
User-Agent: curl/8.4.0
X-Forwarded-For: 10.244.120.64
X-Forwarded-Host: 127.0.0.1
X-Forwarded-Port: 80
X-Forwarded-Proto: http
X-Forwarded-Scheme: http
X-Real-Ip: 10.244.120.64
X-Request-Id: b69d91be337a6fd4513e49f9b2dd3f46
X-Scheme: http

