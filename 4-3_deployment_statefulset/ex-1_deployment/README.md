# Deployments


https://kubernetes.io/ja/docs/concepts/workloads/controllers/deployment/

セットアップ

mini:~ takara$ minikube start -n 3


ローリングアップデート

自己回復


mini:ex-1_deployment takara$ kubectl get no
NAME           STATUS   ROLES           AGE     VERSION
minikube       Ready    control-plane   4m57s   v1.28.3
minikube-m02   Ready    <none>          4m40s   v1.28.3
minikube-m03   Ready    <none>          4m29s   v1.28.3
mini:ex-1_deployment takara$ ls
README.md       deployment.yaml service.yaml

mini:ex-1_deployment takara$ kubectl apply -f deployment.yaml 
deployment.apps/nginx created
mini:ex-1_deployment takara$ kubectl get deploy
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
nginx   3/3     3            3           10s
mini:ex-1_deployment takara$ kubectl get all
NAME                        READY   STATUS    RESTARTS   AGE
pod/nginx-97988c57f-bzq8w   1/1     Running   0          17s
pod/nginx-97988c57f-kqvl2   1/1     Running   0          17s
pod/nginx-97988c57f-qd8k6   1/1     Running   0          17s

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   5m27s

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/nginx   3/3     3            3           17s

NAME                              DESIRED   CURRENT   READY   AGE
replicaset.apps/nginx-97988c57f   3         3         3       17s


mini:~ takara$ kubectl port-forward deployment/my-nginx 9200:9200
Forwarding from 127.0.0.1:9200 -> 9200
Forwarding from [::1]:9200 -> 9200
Handling connection for 9200






mini:ex-1_deployment takara$ kubectl get pdb -A
No resources found
mini:ex-1_deployment takara$ kubectl apply -f service.yaml 
service/my-nginx created
mini:ex-1_deployment takara$ kubectl get svc
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.96.0.1       <none>        443/TCP    29m
my-nginx     ClusterIP   10.102.134.44   <none>        9200/TCP   9s


