kubectl label nodes minikube-m02 disktype=ssd


For brevity, this example doesn't use the well-known label keys topology.kubernetes.io/zone and topology.kubernetes.io/region. However, those registered label keys are nonetheless recommended rather than the private (unqualified) label keys region and zone that are used here.

You can't make a reliable assumption about the meaning of a private label key between different contexts.


```
mini:docker_and_k8s takara$ kubectl get nodes -o=jsonpath='{.items[*].metadata.labels}' |jq -r .
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube",
  "kubernetes.io/os": "linux",
  "minikube.k8s.io/commit": "8220a6eb95f0a4d75f7f2d7b14cef975f050512d",
  "minikube.k8s.io/name": "minikube",
  "minikube.k8s.io/primary": "true",
  "minikube.k8s.io/updated_at": "2024_05_13T06_41_36_0700",
  "minikube.k8s.io/version": "v1.32.0",
  "node-role.kubernetes.io/control-plane": "",
  "node.kubernetes.io/exclude-from-external-load-balancers": ""
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m02",
  "kubernetes.io/os": "linux"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m03",
  "kubernetes.io/os": "linux"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m04",
  "kubernetes.io/os": "linux"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m05",
  "kubernetes.io/os": "linux"
}
```




minikube start --nodes=5

kubectl taint nodes minikube key1=value1:NoSchedule
kubectl label nodes minikube-m02 kubernetes.io/zone=tokyo
kubectl label nodes minikube-m03 kubernetes.io/zone=tokyo
kubectl label nodes minikube-m04 kubernetes.io/zone=osaka
kubectl label nodes minikube-m05 kubernetes.io/zone=osaka
kubectl get nodes -o=jsonpath='{.items[*].metadata.labels}' |jq -r .
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube",
  "kubernetes.io/os": "linux",
  "minikube.k8s.io/commit": "8220a6eb95f0a4d75f7f2d7b14cef975f050512d",
  "minikube.k8s.io/name": "minikube",
  "minikube.k8s.io/primary": "true",
  "minikube.k8s.io/updated_at": "2024_05_13T10_57_02_0700",
  "minikube.k8s.io/version": "v1.32.0",
  "node-role.kubernetes.io/control-plane": "",
  "node.kubernetes.io/exclude-from-external-load-balancers": ""
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m02",
  "kubernetes.io/os": "linux",
  "kubernetes.io/zone": "tokyo"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m03",
  "kubernetes.io/os": "linux",
  "kubernetes.io/zone": "tokyo"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m04",
  "kubernetes.io/os": "linux",
  "kubernetes.io/zone": "osaka"
}
{
  "beta.kubernetes.io/arch": "arm64",
  "beta.kubernetes.io/os": "linux",
  "kubernetes.io/arch": "arm64",
  "kubernetes.io/hostname": "minikube-m05",
  "kubernetes.io/os": "linux",
  "kubernetes.io/zone": "osaka"
}



kubectl apply -f deployment-ptsc.yaml
kubectl get po -o wide



minikube start --nodes=5

kubectl taint nodes minikube key1=value1:NoSchedule
kubectl label nodes minikube-m02 topology.kubernetes.io/region="jp-tokyo-1"
kubectl label nodes minikube-m02 topology.kubernetes.io/zone="jp-tokyo-1a"
kubectl label nodes minikube-m03 topology.kubernetes.io/region="jp-tokyo-1"
kubectl label nodes minikube-m03 topology.kubernetes.io/zone="jp-tokyo-1b"
kubectl label nodes minikube-m04 topology.kubernetes.io/region="jp-tokyo-1"
kubectl label nodes minikube-m04 topology.kubernetes.io/zone="jp-tokyo-1c"

kubectl get nodes -o=jsonpath='{.items[*].metadata.labels}' |jq -r .
