


minikube start --cni calico

$ kubectl create deployment nginx --image=nginx
deployment.apps/nginx created

$ kubectl expose deployment nginx --port=80
service/nginx exposed

$ kubectl get svc,pod
NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1      <none>        443/TCP   54s
service/nginx        ClusterIP   10.98.172.78   <none>        80/TCP    7s

NAME                         READY   STATUS    RESTARTS   AGE
pod/nginx-7854ff8877-99f7p   1/1     Running   0          14s


$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.2 -- /bin/sh
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



$ ls
README.md	np.yaml

$ cat np.yaml 
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

$ kubectl apply -f np.yaml 
networkpolicy.networking.k8s.io/access-nginx created

$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.2 -- /bin/sh
If you don't see a command prompt, try pressing enter.

# curl http://nginx/




nobody@my-pods-5c84c44bc6-44zmq:/$ curl http://rest-service.prod.svc.cluster.local:9100/info
Host Name: my-pods-5c84c44bc6-nhd6m
Host IP: 10.244.120.73
Client IP : 10.244.120.76
nobody@my-pods-5c84c44bc6-44zmq:/$ curl http://rest-service.stage.svc.cluster.local:9100/info
Host Name: my-pods-5c84c44bc6-7phwt
Host IP: 10.244.120.78
Client IP : 10.244.120.76


mini:4-5-3_networkpolicy takara$ kubectl apply -f deny-all-ingress.yaml -n stage
networkpolicy.networking.k8s.io/default-deny-ingress created

nobody@my-pods-5c84c44bc6-44zmq:/$ curl http://rest-service.prod.svc.cluster.local:9100/info
Host Name: my-pods-5c84c44bc6-ldx9w
Host IP: 10.244.120.74
Client IP : 10.244.120.76

nobody@my-pods-5c84c44bc6-44zmq:/$ curl http://rest-service.stage.svc.cluster.local:9100/info

mini:4-5-3_networkpolicy takara$ kubectl apply -n stage -f deny-all-ingress.yaml 
mini:4-5-3_networkpolicy takara$ kubectl get po -n prod
NAME                       READY   STATUS    RESTARTS   AGE
my-pods-5c84c44bc6-gkxsf   2/2     Running   0          33m
my-pods-5c84c44bc6-ldx9w   2/2     Running   0          33m
my-pods-5c84c44bc6-nhd6m   2/2     Running   0          33m
mini:4-5-3_networkpolicy takara$ kubectl exec -it my-pods-5c84c44bc6-gkxsf -n prod -c my-pod -- bash
nobody@my-pods-5c84c44bc6-gkxsf:/$ curl http://rest-service.stage.svc.cluster.local:9100/info
^C
nobody@my-pods-5c84c44bc6-gkxsf:/$ http://rest-service.prod.svc.cluster.local:9100/info
bash: http://rest-service.prod.svc.cluster.local:9100/info: No such file or directory
nobody@my-pods-5c84c44bc6-gkxsf:/$ curl http://rest-service.prod.svc.cluster.local:9100/info
Host Name: my-pods-5c84c44bc6-ldx9w
Host IP: 10.244.120.74
Client IP : 10.244.120.75