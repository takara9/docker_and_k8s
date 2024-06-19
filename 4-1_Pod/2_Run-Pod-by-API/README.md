# ポッドをAPIで起動
Kubernetesでのコンテナの実行単位であるポッドをAPI(YAMLファイル)で起動します。


## 準備
```
$ minikube start
$ kubectl get node
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   22s   v1.30.0
```


## 実行例
Kubernetes APIを記述したYAMLファイルを Kubernetesクラスタへ適用して、ポッドを起動
```
$ kubectl apply -f pod.yaml
pod/my-pod created

$ kubectl get po
NAME     READY   STATUS    RESTARTS   AGE
my-pod   1/1     Running   0          20s
```

デプロイメントのAPIを記述したYAMLファイルを適用してポッドを起動
```
$ kubectl apply -f deployment.yaml 
deployment.apps/ex1-deploy created

$ kubectl get pod
NAME                          READY   STATUS    RESTARTS   AGE
ex1-deploy-655bbfc5d7-5hjjq   1/1     Running   0          19s
ex1-deploy-655bbfc5d7-fh5bz   1/1     Running   0          19s
ex1-deploy-655bbfc5d7-g8th6   1/1     Running   0          19s
my-pod                        1/1     Running   0          2m37s
```


## クリーンナップ
```
$ kubectl delete -f pod.yaml
$ kubectl delete -f deployment.yaml 
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_apply/
- https://kubernetes.io/docs/concepts/workloads/pods/



