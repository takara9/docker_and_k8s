

```
$ kubectl apply -f pod-emptydir.yaml 
pod/pod-emptydir created

$ kubectl get pod
NAME           READY   STATUS    RESTARTS   AGE
pod-emptydir   1/1     Running   0          6s
```


```
$ kubectl exec -it pod-emptydir -- bash
nobody@pod-emptydir:/app$ df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          59G   22G   35G  38% /
tmpfs            64M     0   64M   0% /dev
/dev/vda1        59G   22G   35G  38% /cache
shm              64M     0   64M   0% /dev/shm
tmpfs           7.7G   12K  7.7G   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs           3.9G     0  3.9G   0% /sys/firmware

nobody@pod-emptydir:/app$ tar cvf /cache/test.tar /usr 
tar: Removing leading `/' from member names
/usr/
/usr/games/
/usr/src/

nobody@pod-emptydir:/app$ ls -lh /cache/
total 389M
-rw-r--r-- 1 nobody nogroup 389M Apr  7 08:35 test.tar
nobody@pod-emptydir:/app$ exit
$
```

```
$ kubectl get po
NAME           READY   STATUS    RESTARTS      AGE
pod-emptydir   1/1     Running   1 (69s ago)   3m9s
mini:EphemeralVolumes takara$ kubectl exec -it pod-emptydir -- bash
nobody@pod-emptydir:/app$ ls -lh /cache/
total 389M
-rw-r--r-- 1 nobody nogroup 389M Apr  7 08:35 test.tar
nobody@pod-emptydir:/app$ exit
```