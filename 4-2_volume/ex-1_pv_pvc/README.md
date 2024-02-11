mini:ex-1 takara$ kubectl apply -f pv.yaml 
persistentvolume/task-pv-volume created

mini:ex-1 takara$ kubectl apply -f pvc.yaml 
persistentvolumeclaim/task-pv-claim created

mini:ex-1 takara$ kubectl get pv
NAME             CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                   STORAGECLASS   REASON   AGE
task-pv-volume   10Gi       RWO            Retain           Bound    default/task-pv-claim   manual                  11s

mini:ex-1 takara$ kubectl get pvc
NAME            STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
task-pv-claim   Bound    task-pv-volume   10Gi       RWO            manual         7s

mini:ex-1 takara$ kubectl apply -f pod.yaml 
pod/task-pv-pod created

mini:ex-1 takara$ kubectl get po
NAME          READY   STATUS    RESTARTS   AGE
my-ubuntu     1/1     Running   0          17m
my-ubuntu2    1/1     Running   0          3m55s
task-pv-pod   1/1     Running   0          9s
mini:ex-1 takara$ kubectl exec -it task-pv-pod -- bash

root@task-pv-pod:/# df
Filesystem     1K-blocks    Used Available Use% Mounted on
overlay         61202244 6632908  51428012  12% /
tmpfs              65536       0     65536   0% /dev
/dev/vda1       61202244 6632908  51428012  12% /etc/hosts
shm                65536       0     65536   0% /dev/shm
tmpfs            8034972      12   8034960   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs            4017484       0   4017484   0% /sys/firmware

root@task-pv-pod:/# lsblk
NAME   MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
nbd0    43:0    0     0B  0 disk 
nbd1    43:32   0     0B  0 disk 
nbd2    43:64   0     0B  0 disk 
nbd3    43:96   0     0B  0 disk 
nbd4    43:128  0     0B  0 disk 
nbd5    43:160  0     0B  0 disk 
nbd6    43:192  0     0B  0 disk 
nbd7    43:224  0     0B  0 disk 
vda    254:0    0  59.6G  0 disk 
`-vda1 254:1    0  59.6G  0 part /usr/share/nginx/html
                                 /etc/hosts
                                 /etc/hostname
                                 /etc/resolv.conf
                                 /dev/termination-log
vdb    254:16   0   309M  1 disk 
vdc    254:32   0 625.9M  1 disk 
nbd8    43:256  0     0B  0 disk 
nbd9    43:288  0     0B  0 disk 
nbd10   43:320  0     0B  0 disk 
nbd11   43:352  0     0B  0 disk 
nbd12   43:384  0     0B  0 disk 
nbd13   43:416  0     0B  0 disk 
nbd14   43:448  0     0B  0 disk 
nbd15   43:480  0     0B  0 disk 


root@task-pv-pod:/# date
Thu Jan  4 21:18:24 UTC 2024
root@task-pv-pod:/# date > /usr/share/nginx/html/test.dat
root@task-pv-pod:/# cat /usr/share/nginx/html/test.dat
Thu Jan  4 21:18:40 UTC 2024
root@task-pv-pod:/# exit
exit
mini:ex-1 takara$ kubectl delete po task-pv-pod
pod "task-pv-pod" deleted
mini:ex-1 takara$ kubectl get po
NAME         READY   STATUS    RESTARTS   AGE
my-ubuntu    1/1     Running   0          20m
my-ubuntu2   1/1     Running   0          7m9s
mini:ex-1 takara$ kubectl apply -f pod.yaml 
pod/task-pv-pod created
mini:ex-1 takara$ kubectl exec -it task-pv-pod -- bash
root@task-pv-pod:/# cat /usr/share/nginx/html/test.dat
Thu Jan  4 21:18:40 UTC 2024

