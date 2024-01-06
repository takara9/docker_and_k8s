  
https://minikube.sigs.k8s.io/docs/tutorials/volume_snapshots_and_csi/
  
minikube addons enable volumesnapshots
minikube addons enable csi-hostpath-driver

$ kubectl get sc
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
csi-hostpath-sc      hostpath.csi.k8s.io        Delete          Immediate           false                  5h1m
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  5h2m




https://minikube.sigs.k8s.io/docs/tutorials/local_path_provisioner/

mini:ex-4 takara$ kubectl get sc
NAME                   PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path      Delete          WaitForFirstConsumer   false                  31s
standard               k8s.io/minikube-hostpath   Delete          Immediate              false                  68s