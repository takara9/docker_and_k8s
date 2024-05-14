
$ minikube start

$ kubectl create deployment hello-minikube1 --image=kicbase/echo-server:1.0
$ kubectl expose deployment hello-minikube1 --type=NodePort --port=8080
service/hello-minikube1 exposed

$ kubectl get svc
NAME              TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
hello-minikube1   NodePort    10.109.248.79   <none>        8080:31240/TCP   20s
kubernetes        ClusterIP   10.96.0.1       <none>        443/TCP          5m19s

$ minikube service hello-minikube1 --url
http://127.0.0.1:59455
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。


mini:4-5-1_nodeport takara$ kubectl apply -f deployment.yaml 
deployment.apps/my-pods created
mini:4-5-1_nodeport takara$ kubectl apply -f sevice-np.yaml 
service/rest-service-np created
mini:4-5-1_nodeport takara$ kubectl get svc
NAME              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes        ClusterIP   10.96.0.1        <none>        443/TCP          61s
rest-service-np   NodePort    10.109.193.255   <none>        9100:31256/TCP   15s

mini:4-5-1_nodeport takara$ minikube service rest-service-np --url
http://127.0.0.1:59566
❗  Docker ドライバーを darwin 上で使用しているため、実行するにはターミナルを開く必要があります。



http://127.0.0.1:59566/info
Host Name: my-pods-7dc8dfd5c9-9g45b Host IP: 10.244.0.4 Client IP : 10.244.0.1

mini:docker_and_k8s takara$ kubectl get pod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-7dc8dfd5c9-9g45b   1/1     Running   0          2m23s
my-pods-7dc8dfd5c9-9pvk2   1/1     Running   0          2m23s
my-pods-7dc8dfd5c9-z4qqv   1/1     Running   0          2m23s

際読み込みで、複数のポッドが出てくるので、分散されている事がわかる。



