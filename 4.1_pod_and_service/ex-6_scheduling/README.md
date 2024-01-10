https://kubernetes.io/docs/concepts/scheduling-eviction/


$ minikube delete
$ minikube start --nodes=3 

$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   69s   v1.28.3
minikube-m02   Ready    <none>          49s   v1.28.3
minikube-m03   Ready    <none>          39s   v1.28.3


$ kubectl apply -f pod.yaml 
pod/nginx created

$ kubectl get po -o wide
NAME    READY   STATUS    RESTARTS   AGE   IP           NODE
nginx   1/1     Running   0          14s   10.244.1.2   minikube-m02

