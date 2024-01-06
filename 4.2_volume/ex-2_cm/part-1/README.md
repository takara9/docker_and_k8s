

kubectl create cm app-conf --from-file=config
kubectl apply -f pod.yaml




mini:ex-2 takara$ ls -F
README.md	config/		pod.yaml
mini:ex-2 takara$ kubectl create cm app-conf --from-file=config
configmap/app-conf created
mini:ex-2 takara$ kubectl get cm
NAME               DATA   AGE
app-conf           1      5s
kube-root-ca.crt   1      5m3s


mini:ex-2 takara$ kubectl get cm app-conf -o yaml
apiVersion: v1
data:
  default.config: |
    server {
        listen 9200;
        location / {
            root   /usr/share/nginx/html;
            index  index.html index.htm;
        }
    }
kind: ConfigMap
metadata:
  creationTimestamp: "2024-01-04T20:54:53Z"
  name: app-conf
  namespace: default
  resourceVersion: "781"
  uid: fb981714-a2fc-45f8-bb2d-9062c70ce74d


mini:ex-2 takara$ kubectl apply -f pod.yaml 
pod/my-ubuntu created


mini:ex-2 takara$ kubectl get po
NAME        READY   STATUS    RESTARTS   AGE
my-ubuntu   1/1     Running   0          3s



mini:ex-2 takara$ kubectl exec -it my-ubuntu -- bash

root@my-ubuntu:/# cat /mnt/default.config 
server {
    listen 9200;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}
