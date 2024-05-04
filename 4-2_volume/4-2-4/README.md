

~~~
minikube start
minikube addons disable storage-provisioner
minikube addons disable default-storageclass
minikube addons list
minikube addons enable csi-hostpath-driver
minikube addons enable volumesnapshots
kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
kubectl get sc
~~~


~~~
kubectl apply -f pvc.yaml 
kubectl get pvc
kubectl apply -f pod-pvc.yaml 
kubectl exec -it pod-pvc -- bash
nobody@pod-pvc:/app$ date > /mnt/test.dat
nobody@pod-pvc:/app$ cat /mnt/test.dat 
Tue Apr  9 22:53:24 UTC 2024
~~~


~~~
$ kubectl get volumesnapshotclasses
NAME                     DRIVER                DELETIONPOLICY   AGE
csi-hostpath-snapclass   hostpath.csi.k8s.io   Delete           112s
~~~


~~~
$ kubectl apply -f snapshot.yaml 
volumesnapshot.snapshot.storage.k8s.io/my-snapshot created

$ kubectl get volumesnapshot
NAME         READYTOUSE  SOURCEPVC  RESTORESIZE  SNAPSHOTCLASS           SNAPSHOTCONTENT       AGE
my-snapshot  true        my-vol     1Gi          csi-hostpath-snapclass  snapcontent-2868f860  26s

$ kubectl get pvc
NAME    STATUS  VOLUME       CAPACITY  ACCESS MODES  STORAGECLASS     AGE
my-vol  Bound   pvc-d4ae742d 1Gi       RWO           csi-hostpath-sc  2m35s
~~~



~~~
$ kubectl apply -f restore.yaml 
persistentvolumeclaim/my-vol-snapshot created

$ kubectl get pvc
NAME             STATUS  VOLUME       CAPACITY  ACCESS MODES  STORAGECLASS     AGE
my-vol           Bound   pvc-d4ae742d 1Gi       RWO           csi-hostpath-sc  2m47s
my-vol-snapshot  Bound   pvc-f9fbfdcd 1Gi       RWO           csi-hostpath-sc  3s
~~~


~~~
$ kubectl apply -f pod.yaml 
pod/pod-pvc2 created

$ kubectl exec -it pod-pvc2 -- bash
nobody@pod-pvc2:/app$ cd /mnt
nobody@pod-pvc2:/mnt$ ls
test.dat
nobody@pod-pvc2:/mnt$ cat test.dat 
Tue Apr  9 22:53:24 UTC 2024
~~~


