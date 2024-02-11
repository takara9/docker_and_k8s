

minikube start -n 3 --cni calico


mini:ex-3_networkpolicy takara$ kubectl create deployment nginx --image=nginx
deployment.apps/nginx created

mini:ex-3_networkpolicy takara$ kubectl expose deployment nginx --port=80
service/nginx exposed

mini:ex-3_networkpolicy takara$ kubectl get svc,pod
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP   54s
service/nginx        ClusterIP   10.98.172.78   <none>        80/TCP    7s

NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-7854ff8877-99f7p   1/1     Running   0          14s


mini:ex-3_networkpolicy takara$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.2 -- /bin/sh
If you don't see a command prompt, try pressing enter.

# curl http://nginx/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
# 
Session ended, resume using 'kubectl attach my-pod -c my-pod -i -t' command when the pod is running
pod "my-pod" deleted

mini:ex-3_networkpolicy takara$ ls
README.md	np.yaml

mini:ex-3_networkpolicy takara$ cat np.yaml 
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: access-nginx
spec:
  podSelector:
    matchLabels:
      app: nginx
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: "true"

mini:ex-3_networkpolicy takara$ kubectl apply -f np.yaml 
networkpolicy.networking.k8s.io/access-nginx created

mini:ex-3_networkpolicy takara$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.2 -- /bin/sh
If you don't see a command prompt, try pressing enter.

# curl http://nginx/

