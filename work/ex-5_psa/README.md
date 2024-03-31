https://minikube.sigs.k8s.io/docs/tutorials/audit-policy/

~~~
minikube delete

mkdir -p ~/.minikube/files/etc/ssl/certs

cat <<EOF > ~/.minikube/files/etc/ssl/certs/audit-policy.yaml
# Log all requests at the Metadata level.
apiVersion: audit.k8s.io/v1
kind: Policy
rules:
- level: Metadata
EOF

minikube start \
  --extra-config=apiserver.audit-policy-file=/etc/ssl/certs/audit-policy.yaml \
  --extra-config=apiserver.audit-log-path=-
~~~



~~~
kubectl logs kube-apiserver-minikube -n kube-system | grep audit.k8s.io/v1
~~~


