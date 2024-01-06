minikube start -n 3
mini:4.5_network takara$ kubectl create deployment hello-minikube1 --image=kicbase/echo-server:1.0
deployment.apps/hello-minikube1 created
mini:4.5_network takara$ kubectl expose deployment hello-minikube1 --type=NodePort --port=8080
service/hello-minikube1 exposed
mini:4.5_network takara$ kubectl get svc
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-minikube1   NodePort    10.110.56.212   <none>        8080:31867/TCP   11s
kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP          72s
mini:4.5_network takara$ minikube service hello-minikube1 --url
http://127.0.0.1:52616
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。


mini:~ takara$ curl http://127.0.0.1:52616
Request served by hello-minikube1-5f7945679-nk589

HTTP/1.1 GET /

Host: 127.0.0.1:52616
Accept: */*
User-Agent: curl/8.4.0
mini:~ takara$ 


