https://kubernetes.io/docs/tasks/administer-cluster/access-cluster-api/



# Check all possible clusters, as your .KUBECONFIG may have multiple contexts:
kubectl config view -o jsonpath='{"Cluster name\tServer\n"}{range .clusters[*]}{.name}{"\t"}{.cluster.server}{"\n"}{end}'

# Select name of cluster you want to interact with from above output:
export CLUSTER_NAME="some_server_name"

# Point to the API server referring the cluster name
APISERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name==\"$CLUSTER_NAME\")].cluster.server}")

# Create a secret to hold a token for the default service account
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF

# Wait for the token controller to populate the secret with a token:
while ! kubectl describe secret default-token | grep -E '^token' >/dev/null; do
  echo "waiting for token..." >&2
  sleep 1
done

# Get the token value
TOKEN=$(kubectl get secret default-token -o jsonpath='{.data.token}' | base64 --decode)

# Explore the API with TOKEN
curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure



export CLUSTER_NAME="minikube"
APISERVER=$(kubectl config view -o jsonpath="{.clusters[?(@.name==\"$CLUSTER_NAME\")].cluster.server}")
kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF
TOKEN=$(kubectl get secret default-token -o jsonpath='{.data.token}' | base64 --decode)
curl -X GET $APISERVER/api --header "Authorization: Bearer $TOKEN" --insecure
{
  "kind": "APIVersions",
  "versions": [
    "v1"
  ],
  "serverAddressByClientCIDRs": [
    {
      "clientCIDR": "0.0.0.0/0",
      "serverAddress": "192.168.49.2:8443"
    }
  ]
}

curl --header "Authorization: Bearer $TOKEN" --insecure -X GET $APISERVER/api 




kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  namespace: default
  name: pod-reader
rules:
- apiGroups: [""] # "" はコアのAPIグループを示します
  resources: ["pods"]
  verbs: ["get", "watch", "list"]
EOF


kubectl apply -f - <<EOF
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: read-pods
  namespace: default
subjects:
- kind: ServiceAccount
  name: default
  namespace: default
roleRef:
  kind: Role
  name: pod-reader
  apiGroup: rbac.authorization.k8s.io
EOF


kubectl apply -f - <<EOF
apiVersion: v1
kind: Secret
metadata:
  name: default-token
  serviceaccount: default
  annotations:
    kubernetes.io/service-account.name: default
type: kubernetes.io/service-account-token
EOF



curl http://localhost:8080/api/v1/namespaces/default/pods |jq -r .



$ kubectl cluster-info
Kubernetes control plane is running at https://127.0.0.1:54658
CoreDNS is running at https://127.0.0.1:54658/api/v1/namespaces/kube-system/services/kube-dns:dns/proxy



apiサーバーにアクセスできるように、プロキシーを開く
kubectl proxy --port=8080 

curl -s http://localhost:8080/api/v1/pods |jq -r '.items[].metadata | .name, .namespace' | xargs -n2
curl -s http://localhost:8080/api/v1/pods |jq -r '.items[].metadata | [.name, .namespace] |@csv'






mini:~ takara$ kubectl get po -A
NAMESPACE     NAME                               READY   STATUS    RESTARTS        AGE
kube-system   coredns-5dd5756b68-q6vfk           1/1     Running   0               4h30m
kube-system   etcd-minikube                      1/1     Running   0               4h30m
kube-system   kube-apiserver-minikube            1/1     Running   0               4h30m
kube-system   kube-controller-manager-minikube   1/1     Running   0               4h30m
kube-system   kube-proxy-hc84z                   1/1     Running   0               4h30m
kube-system   kube-scheduler-minikube            1/1     Running   0               4h30m
kube-system   storage-provisioner                1/1     Running   1 (4h30m ago)   4h30m


mini:~ takara$ curl -s http://localhost:8080/api/v1/pods |jq -r '.items[].metadata | [.name, .namespace] |@csv'
"coredns-5dd5756b68-q6vfk","kube-system"
"etcd-minikube","kube-system"
"kube-apiserver-minikube","kube-system"
"kube-controller-manager-minikube","kube-system"
"kube-proxy-hc84z","kube-system"
"kube-scheduler-minikube","kube-system"
"storage-provisioner","kube-system"



mini:~ takara$ kubectl exec -it -n kube-system etcd-minikube -- sh -c "ETCDCTL_API=3 etcdctl --endpoints=https://127.0.0.1:2379 --cert /var/lib/minikube/certs/etcd/server.crt --key /var/lib/minikube/certs/etcd/server.key --cacert /var/lib/minikube/certs/etcd/ca.crt get / --prefix --keys-only" | awk 'length($0)>1'|grep pods
/registry/pods/kube-system/coredns-5dd5756b68-q6vfk
/registry/pods/kube-system/etcd-minikube
/registry/pods/kube-system/kube-apiserver-minikube
/registry/pods/kube-system/kube-controller-manager-minikube
/registry/pods/kube-system/kube-proxy-hc84z
/registry/pods/kube-system/kube-scheduler-minikube
/registry/pods/kube-system/storage-provisioner