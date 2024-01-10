  
https://minikube.sigs.k8s.io/docs/tutorials/volume_snapshots_and_csi/



$ minikube start
$ minikube addons enable csi-hostpath-driver

$ kubectl get storageclass
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-hostpath-sc      hostpath.csi.k8s.io        Delete          Immediate           false                  56s
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  2m24s



$ minikube addons enable volumesnapshots
