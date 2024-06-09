$ minikube start

$ minikube tunnel
✅  トンネルが無事開始しました

📌  注意: トンネルにアクセスするにはこのプロセスが存続しなければならないため、このターミナルはクローズしないでください ...



mini:4-5-2_loadbalancer takara$ kubectl apply -f deployment.yaml 
deployment.apps/my-pods created
mini:4-5-2_loadbalancer takara$ kubectl apply -f sevice-lb.yaml 
service/rest-service-lb created
mini:4-5-2_loadbalancer takara$ kubectl get svc
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
kubernetes        ClusterIP      10.96.0.1       <none>        443/TCP          11m
rest-service-lb   LoadBalancer   10.106.55.146   127.0.0.1     9100:30176/TCP   4s


http://localhost:9100/info
Host Name: my-pods-7dc8dfd5c9-jbgfd Host IP: 10.244.0.5 Client IP : 10.244.0.1