$ minikube delete
$ minikube start --nodes=3


$ kubectl get no
NAME           STATUS   ROLES           AGE   VERSION
minikube       Ready    control-plane   38s   v1.28.3
minikube-m02   Ready    <none>          17s   v1.28.3
minikube-m03   Ready    <none>          9s    v1.28.3

全ノードについているラベルをリストする

$ kubectl get no --show-labels
NAME           STATUS   ROLES           AGE   VERSION   LABELS
minikube       Ready    control-plane   45s   v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube,kubernetes.io/os=linux,minikube.k8s.io/commit=8220a6eb95f0a4d75f7f2d7b14cef975f050512d,minikube.k8s.io/name=minikube,minikube.k8s.io/primary=true,minikube.k8s.io/updated_at=2024_01_08T08_40_21_0700,minikube.k8s.io/version=v1.32.0,node-role.kubernetes.io/control-plane=,node.kubernetes.io/exclude-from-external-load-balancers=
minikube-m02   Ready    <none>          24s   v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube-m02,kubernetes.io/os=linux
minikube-m03   Ready    <none>          16s   v1.28.3   beta.kubernetes.io/arch=arm64,beta.kubernetes.io/os=linux,kubernetes.io/arch=arm64,kubernetes.io/hostname=minikube-m03,kubernetes.io/os=linux


特定のノードのラベルを表示する

$ kubectl label --list node minikube-m02
kubernetes.io/os=linux
beta.kubernetes.io/arch=arm64
beta.kubernetes.io/os=linux
kubernetes.io/arch=arm64
kubernetes.io/hostname=minikube-m02


ノード minikube-m02にラベルを付与する

$ kubectl label nodes minikube-m02 gpu=model123
node/minikube-m02 labeled


ラベルが付いたことを確認する

$ kubectl label --list node minikube-m02
kubernetes.io/hostname=minikube-m02
kubernetes.io/os=linux
beta.kubernetes.io/arch=arm64
beta.kubernetes.io/os=linux
gpu=model123
kubernetes.io/arch=arm64



ラベルの付いたノードにポッドを配置する

$ kubectl apply -f pod1-nodeselector.yaml 
pod/nginx-gpu1 created

$ kubectl apply -f pod2-nodeselector.yaml 
pod/nginx-gpu2 created

$ kubectl get po -o wide
NAME         READY   STATUS    RESTARTS   AGE   IP           NODE        
nginx-gpu1   1/1     Running   0          12s   10.244.1.3   minikube-m02
nginx-gpu2   1/1     Running   0          7s    10.244.1.4   minikube-m02



ラベルの削除

$ kubectl label nodes minikube-m02 gpu-
node/minikube-m02 unlabeled
