## セルフサービスの設定

~~~
maho-2:argo-cd-2-10-test maho$ pwd
/Users/maho/docker_and_k8s/4-7_CICD/argo-cd-2-10-test
~~~

~~~
minikube start
kubectl get nodes
kubectl create ns guestbook
kubectl create ns app-team-one
kubectl create ns app-team-two
kubectl create ns argocd

kubectl apply -n argocd -f install-argocd-2.10.1-patch.yaml
kubectl get po -n argocd -w　#起動まで待つ
~~~

~~~
## kubectl apply -k . 必須
kubectl apply -n argocd -f argocd-server-rbac-clusterrole.yaml
kubectl apply -n argocd -f argocd-server-rbac-clusterrolebinding.yaml
kubectl apply -n argocd -f argocd-notifications-controller-rbac-clusterrole.yaml
kubectl apply -n argocd -f argocd-notifications-controller-rbac-clusterrolebinding.yaml
kubectl apply -n argocd -f appproject.yaml
~~~

## これ以下はユーザーの作業

~~~
kubectl apply -n app-team-one -f install-2.yaml
kubectl apply -n app-team-one -f secret-for-argocd-notification.yaml
kubectl -n argocd get secret/argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d; echo
kubectl port-forward service/argocd-server -n argocd 8090:80
kubectl apply -f app.yaml 
~~~

