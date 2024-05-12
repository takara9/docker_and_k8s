kubectl label nodes minikube-m02 disktype=ssd


kubectl label nodes minikube topology.kubernetes.io/zone=tokyo-east1
kubectl label nodes minikube-m02 topology.kubernetes.io/zone=tokyo-west1
kubectl label nodes minikube-m03 topology.kubernetes.io/zone=tokyo-north1
kubectl label nodes minikube-m04 topology.kubernetes.io/zone=tokyo-south1
