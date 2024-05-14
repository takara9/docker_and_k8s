https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/


## スケジュールしない

$ minikube start -n 2
s takara$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   31s   v1.28.3
minikube-m02   Ready    <none>          11s   v1.28.3


$ kubectl taint nodes minikube controller:NoSchedule
$ kubectl apply -f deployment.yaml
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-66974f9784-4mzlz   1/1     Running   0          37s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-66974f9784-8vtzt   1/1     Running   0          37s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-66974f9784-9mzd8   1/1     Running   0          37s   10.244.1.3   minikube-m02   <none>           <none>
my-pods-66974f9784-hwqp5   1/1     Running   0          37s   10.244.1.6   minikube-m02   <none>           <none>
my-pods-66974f9784-xkwx8   1/1     Running   0          37s   10.244.1.2   minikube-m02   <none>           <none>

$ kubectl delete -f deployment.yaml

$ kubectl apply -f deployment-toler.yaml
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-7d457d6fb9-8gjn6   1/1     Running   0          20s   10.244.0.4   minikube       <none>           <none>
my-pods-7d457d6fb9-h6dd4   1/1     Running   0          20s   10.244.0.3   minikube       <none>           <none>
my-pods-7d457d6fb9-nnrmd   1/1     Running   0          20s   10.244.1.8   minikube-m02   <none>           <none>
my-pods-7d457d6fb9-rcq7j   1/1     Running   0          20s   10.244.1.9   minikube-m02   <none>           <none>
my-pods-7d457d6fb9-wgpnf   1/1     Running   0          20s   10.244.1.7   minikube-m02   <none>           <none>


## 実行を禁止する


$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   43s   v1.28.3
minikube-m02   Ready    <none>          22s   v1.28.3
minikube-m03   Ready    <none>          8s    v1.28.3

$ kubectl taint nodes minikube controller:NoSchedule
node/minikube tainted

$ kubectl apply -f deployment.yaml

$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-66974f9784-8sl7j   1/1     Running   0          19s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-66974f9784-b2t4l   1/1     Running   0          19s   10.244.2.3   minikube-m03   <none>           <none>
my-pods-66974f9784-ljzj7   1/1     Running   0          19s   10.244.1.3   minikube-m02   <none>           <none>
my-pods-66974f9784-q8f8d   1/1     Running   0          19s   10.244.2.2   minikube-m03   <none>           <none>
my-pods-66974f9784-vr4sq   1/1     Running   0          19s   10.244.1.4   minikube-m02   <none>           <none>

ノード２から退避

$ kubectl taint nodes minikube-m02 workload:NoExecute
$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-66974f9784-b2t4l   1/1     Running   0          2m52s   10.244.2.3   minikube-m03   <none>           <none>
my-pods-66974f9784-cczr8   1/1     Running   0          35s     10.244.2.7   minikube-m03   <none>           <none>
my-pods-66974f9784-q8f8d   1/1     Running   0          2m52s   10.244.2.2   minikube-m03   <none>           <none>
my-pods-66974f9784-vt65c   1/1     Running   0          35s     10.244.2.5   minikube-m03   <none>           <none>
my-pods-66974f9784-wv2h7   1/1     Running   0          35s     10.244.2.6   minikube-m03   <none>           <none>

$ kubectl taint nodes minikube-m02 workload:NoExecute-
node/minikube-m02 untainted



minikube start --nodes=3
$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   69s   v1.28.3
minikube-m02   Ready    <none>          48s   v1.28.3
minikube-m03   Ready    <none>          34s   v1.28.3
kubectl taint nodes minikube controller:NoSchedule
kubectl apply -f deployment-toler-2.yaml
kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-85d7965575-cr6c6   1/1     Running   0          16s   10.244.1.8    minikube-m02   <none>           <none>
my-pods-85d7965575-fsqrn   1/1     Running   0          16s   10.244.2.10   minikube-m03   <none>           <none>
my-pods-85d7965575-j8z47   1/1     Running   0          16s   10.244.1.7    minikube-m02   <none>           <none>
my-pods-85d7965575-r62nw   1/1     Running   0          16s   10.244.2.9    minikube-m03   <none>           <none>
my-pods-85d7965575-xtrk6   1/1     Running   0          16s   10.244.1.9    minikube-m02   <none>           <none>

kubectl taint nodes minikube-m02 workload=true:NoExecute
kubectl get pod -o wide

$ kubectl get pod -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-85d7965575-cr6c6   1/1     Running   0          53s   10.244.1.8    minikube-m02   <none>           <none>
my-pods-85d7965575-fsqrn   1/1     Running   0          53s   10.244.2.10   minikube-m03   <none>           <none>
my-pods-85d7965575-j8z47   1/1     Running   0          53s   10.244.1.7    minikube-m02   <none>           <none>
my-pods-85d7965575-r62nw   1/1     Running   0          53s   10.244.2.9    minikube-m03   <none>           <none>
my-pods-85d7965575-xtrk6   1/1     Running   0          53s   10.244.1.9    minikube-m02   <none>           <none>


$ while true; do kubectl get pod -o wide;sleep 60;done
<中略>
NAME                       READY   STATUS    RESTARTS   AGE     IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-85d7965575-cr6c6   1/1     Running   0          9m31s   10.244.1.8    minikube-m02   <none>           <none>
my-pods-85d7965575-fsqrn   1/1     Running   0          9m31s   10.244.2.10   minikube-m03   <none>           <none>
my-pods-85d7965575-j8z47   1/1     Running   0          9m31s   10.244.1.7    minikube-m02   <none>           <none>
my-pods-85d7965575-r62nw   1/1     Running   0          9m31s   10.244.2.9    minikube-m03   <none>           <none>
my-pods-85d7965575-xtrk6   1/1     Running   0          9m31s   10.244.1.9    minikube-m02   <none>           <none>
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-85d7965575-cr6c6   1/1     Running   0          10m   10.244.1.8    minikube-m02   <none>           <none>
my-pods-85d7965575-fsqrn   1/1     Running   0          10m   10.244.2.10   minikube-m03   <none>           <none>
my-pods-85d7965575-j8z47   1/1     Running   0          10m   10.244.1.7    minikube-m02   <none>           <none>
my-pods-85d7965575-r62nw   1/1     Running   0          10m   10.244.2.9    minikube-m03   <none>           <none>
my-pods-85d7965575-xtrk6   1/1     Running   0          10m   10.244.1.9    minikube-m02   <none>           <none>
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-85d7965575-f67dl   1/1     Running   0          47s   10.244.1.10   minikube-m02   <none>           <none>
my-pods-85d7965575-fsqrn   1/1     Running   0          11m   10.244.2.10   minikube-m03   <none>           <none>
my-pods-85d7965575-mkm7k   1/1     Running   0          47s   10.244.2.11   minikube-m03   <none>           <none>
my-pods-85d7965575-r62nw   1/1     Running   0          11m   10.244.2.9    minikube-m03   <none>           <none>
my-pods-85d7965575-zkpt6   1/1     Running   0          47s   10.244.1.11   minikube-m02   <none>           <none>




kubectl taint nodes minikube-m02 app=true:NoSchedule-
