$ minikube delete
$ minikube start --nodes=3
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl apply -f deployment.yaml 

$ kubectl get po -o wide
NAME                              READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-normal-5b5569d958-52xn7   1/1     Running   0          41s   <none>       minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-dh272   1/1     Running   0          41s   <none>       minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-h9wsn   1/1     Running   0          41s   10.244.1.3   minikube-m02   <none>           <none>
my-pods-normal-5b5569d958-mqhvb   1/1     Running   0          41s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-normal-5b5569d958-x5fwv   1/1     Running   0          41s   10.244.1.4   minikube-m02   <none>           <none>

$ kubectl drain minikube-m02 --delete-emptydir-data --ignore-daemonsets
node/minikube-m02 cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-d52sq, kube-system/kube-proxy-4zd52
evicting pod default/my-pods-normal-5b5569d958-x5fwv
evicting pod default/my-pods-normal-5b5569d958-h9wsn
evicting pod default/my-pods-normal-5b5569d958-mqhvb
pod/my-pods-normal-5b5569d958-mqhvb evicted
pod/my-pods-normal-5b5569d958-x5fwv evicted
pod/my-pods-normal-5b5569d958-h9wsn evicted
node/minikube-m02 drained

$ kubectl get po -o wide
NAME                              READY   STATUS    RESTARTS      AGE    IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-normal-5b5569d958-52xn7   1/1     Running   1 (65s ago)   118s   10.244.2.3   minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-cl7js   1/1     Running   0             45s    10.244.2.5   minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-dh272   1/1     Running   1 (66s ago)   118s   10.244.2.2   minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-hlflm   1/1     Running   0             45s    10.244.2.4   minikube-m03   <none>           <none>
my-pods-normal-5b5569d958-mhwzk   1/1     Running   0             45s    10.244.2.6   minikube-m03   <none>           <none>

$ kubectl get no
NAME           STATUS                     ROLES           AGE     VERSION
minikube       Ready                      control-plane   3m15s   v1.28.3
minikube-m02   Ready,SchedulingDisabled   <none>          2m55s   v1.28.3
minikube-m03   Ready                      <none>          2m42s   v1.28.3

$ kubectl uncordon minikube-m02
node/minikube-m02 uncordoned

$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   3m43s   v1.28.3
minikube-m02   Ready    <none>          3m23s   v1.28.3
minikube-m03   Ready    <none>          3m10s   v1.28.3


