$ minikube start -n 3
mini:4.5_network takara$ minikube tunnel
✅  トンネルが無事開始しました

📌  注意: トンネルにアクセスするにはこのプロセスが存続しなければならないため、このターミナルはクローズしないでください ...



mini:~ takara$ kubectl create deployment hello-minikube1 --image=kicbase/echo-server:1.0
deployment.apps/hello-minikube1 created
mini:~ takara$ kubectl expose deployment hello-minikube1 --type=LoadBalancer --port=8080
service/hello-minikube1 exposed
mini:~ takara$ kubectl get svc
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-minikube1   LoadBalancer   10.101.231.53   127.0.0.1     8080:30498/TCP   9s
kubernetes        ClusterIP      10.96.0.1       <none>        443/TCP          2m22s

mini:~ takara$ curl http://127.0.0.1:8080/
Request served by hello-minikube1-5f7945679-n2qs6

HTTP/1.1 GET /

Host: 127.0.0.1:8080
Accept: */*
User-Agent: curl/8.4.0
