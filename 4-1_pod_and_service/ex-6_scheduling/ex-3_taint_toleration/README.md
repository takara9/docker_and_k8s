





$ minikube delete
$ minikube start --nodes=3


$ kubectl get nodes
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   13m   v1.28.3
minikube-m02   Ready    <none>          12m   v1.28.3
minikube-m03   Ready    <none>          12m   v1.28.3

$ kubectl taint nodes minikube key=value:NoSchedule
$ kubectl taint nodes minikube-m02 key=value:NoSchedule

$ kubectl describe node minikube
Name:               minikube
Roles:              control-plane
<中略>
Taints:             key=value:NoSchedule
Unschedulable:      false
Lease:
  HolderIdentity:  minikube
  AcquireTime:     <unset>
  RenewTime:       Mon, 08 Jan 2024 07:26:56 +0900




$ kubectl run nginx1 --image=nginx:latest
pod/nginx1 created
$ kubectl run nginx2 --image=nginx:latest
pod/nginx2 created
$ kubectl run nginx3 --image=nginx:latest
pod/nginx3 created
$ kubectl run nginx4 --image=nginx:latest
pod/nginx4 created


$ kubectl get po -o wide
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE        
nginx1   1/1     Running   0          28s   10.244.1.3   minikube-m03
nginx2   1/1     Running   0          23s   10.244.2.2   minikube-m03
nginx3   1/1     Running   0          18s   10.244.1.4   minikube-m03
nginx4   1/1     Running   0          13s   10.244.2.3   minikube-m03


$ kubectl taint nodes minikube-m03 key=value:NoSchedule
node/minikube-m03 tainted

$ kubectl run nginx5 --image=nginx:latest
pod/nginx5 created

$ kubectl get po -o wide
NAME     READY   STATUS    RESTARTS   AGE     IP           NODE        
nginx1   1/1     Running   0          3m4s    10.244.1.2   minikube-m03
nginx2   1/1     Running   0          2m58s   10.244.2.2   minikube-m03
nginx3   1/1     Running   0          2m54s   10.244.1.3   minikube-m03
nginx4   1/1     Running   0          2m49s   10.244.2.3   minikube-m03
nginx5   0/1     Pending   0          34s     <none>       <none>      


$ kubectl apply -f pod-tolerations.yaml 
pod/nginx created


mini:ex-2_taint_toleration takara$ kubectl get po -o wide
NAME     READY   STATUS    RESTARTS   AGE     IP           NODE        
nginx    1/1     Running   0          7s      10.244.1.4   minikube-m02
nginx1   1/1     Running   0          3m4s    10.244.1.2   minikube-m03
nginx2   1/1     Running   0          2m58s   10.244.2.2   minikube-m03
nginx3   1/1     Running   0          2m54s   10.244.1.3   minikube-m03
nginx4   1/1     Running   0          2m49s   10.244.2.3   minikube-m03
nginx5   0/1     Pending   0          54s     <none>       <none>      




$ kubectl taint nodes minikube key=value:NoSchedule-
node/minikube untainted


mini:ex-1 takara$ kubectl describe node minikube
Name:               minikube
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=arm64
<中略>
Taints:             <none>
Unschedulable:      false

