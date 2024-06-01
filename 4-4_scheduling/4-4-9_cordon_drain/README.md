# コードンとドレイン

準備作業
```
$ minikube delete
$ minikube start --nodes=3
$ kubectl taint nodes minikube workload:NoSchedule
```

ポッドの配置
```
$ kubectl apply -f deployment.yaml 
$ kubectl get po -o wide
NAME                              READY   STATUS    AGE   IP           NODE
my-pods-normal-5b5569d958-f29m4   1/1     Running   25s   10.244.2.2   minikube-m03
my-pods-normal-5b5569d958-g7dss   1/1     Running   25s   10.244.2.3   minikube-m03
my-pods-normal-5b5569d958-kvq95   1/1     Running   25s   10.244.1.4   minikube-m02
my-pods-normal-5b5569d958-qv26x   1/1     Running   25s   10.244.1.2   minikube-m02
my-pods-normal-5b5569d958-xwn5k   1/1     Running   25s   10.244.1.3   minikube-m02
```

ノード2からポッドを退避する
```
$ kubectl drain minikube-m02 --delete-emptydir-data --ignore-daemonsets
node/minikube-m02 cordoned
Warning: ignoring DaemonSet-managed Pods: kube-system/kindnet-8fjkh, kube-system/kube-proxy-g465h
evicting pod default/my-pods-normal-5b5569d958-qv26x
evicting pod default/my-pods-normal-5b5569d958-kvq95
evicting pod default/my-pods-normal-5b5569d958-xwn5k
pod/my-pods-normal-5b5569d958-qv26x evicted
pod/my-pods-normal-5b5569d958-xwn5k evicted
pod/my-pods-normal-5b5569d958-kvq95 evicted
node/minikube-m02 drained
```

これによりポッドは、ノード３に集約された
```
$ kubectl get po -o wide
NAME                              READY   STATUS    AGE     IP           NODE
my-pods-normal-5b5569d958-c4z8r   1/1     Running   70s     10.244.2.4   minikube-m03
my-pods-normal-5b5569d958-f29m4   1/1     Running   2m47s   10.244.2.2   minikube-m03
my-pods-normal-5b5569d958-fhk45   1/1     Running   70s     10.244.2.6   minikube-m03
my-pods-normal-5b5569d958-g7dss   1/1     Running   2m47s   10.244.2.3   minikube-m03
my-pods-normal-5b5569d958-xbr77   1/1     Running   70s     10.244.2.5   minikube-m03
```

ノード２はスケジュール禁止になった
```
$ kubectl get no
NAME           STATUS                     ROLES           AGE     VERSION
minikube       Ready                      control-plane   4m43s   v1.28.3
minikube-m02   Ready,SchedulingDisabled   <none>          4m23s   v1.28.3
minikube-m03   Ready                      <none>          4m9s    v1.28.3
```

ノード２のメンテナンス作業が完了した後、スケジュール可能に戻す
```
$ kubectl uncordon minikube-m02
node/minikube-m02 uncordoned
$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   3m43s   v1.28.3
minikube-m02   Ready    <none>          3m23s   v1.28.3
minikube-m03   Ready    <none>          3m10s   v1.28.3
$ kubectl get po -o wide
NAME                              READY   STATUS    AGE     IP           NODE
my-pods-normal-5b5569d958-c4z8r   1/1     Running   3m12s   10.244.2.4   minikube-m03
my-pods-normal-5b5569d958-f29m4   1/1     Running   4m49s   10.244.2.2   minikube-m03
my-pods-normal-5b5569d958-fhk45   1/1     Running   3m12s   10.244.2.6   minikube-m03
my-pods-normal-5b5569d958-g7dss   1/1     Running   4m49s   10.244.2.3   minikube-m03
my-pods-normal-5b5569d958-xbr77   1/1     Running   3m12s   10.244.2.5   minikube-m03
```

偏ったポッドの配置を、均一に配置し直す

```
$ kubectl rollout restart deployment my-pods-normal
deployment.apps/my-pods-normal restarted
$ kubectl get po -o wide
NAME                              READY   STATUS    AGE   IP           NODE        
my-pods-normal-848f45587b-45h9n   1/1     Running   38s   10.244.1.7   minikube-m02
my-pods-normal-848f45587b-8hdxn   1/1     Running   38s   10.244.2.8   minikube-m03
my-pods-normal-848f45587b-h7xvk   1/1     Running   40s   10.244.2.7   minikube-m03
my-pods-normal-848f45587b-hk8dn   1/1     Running   40s   10.244.1.6   minikube-m02
my-pods-normal-848f45587b-psd8x   1/1     Running   40s   10.244.1.5   minikube-m02
```

