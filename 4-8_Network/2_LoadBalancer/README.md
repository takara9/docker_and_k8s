# ロードバランサー
Kubernetesクラスタと連携するロードバランサーを通じて、ポッドへアクセスします。
minikube では、クラスタ上のKubernetesを再現するために、トンネルを通じてロードバランサータイプのサービスへ接続します。


## 準備
```
$ minikube start
$ minikube tunnel
```


## 実行例
ターミナルをもう一つ開いて、オブジェクトを起動します。
```
$ kubectl apply -f deployment.yaml 
$ kubectl apply -f service-lb.yaml 

$ kubectl get svc rest-service-lb
NAME              TYPE           CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
rest-service-lb   LoadBalancer   10.106.55.146   127.0.0.1     9100:30176/TCP   4s
```

起動したポッドのIPアドレスを確認します。
```
$ kubectl get po -o wide
NAME                      READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-8d5f6cfb4-bgdtq   1/1     Running   0          58s   10.244.0.3   minikube
my-pods-8d5f6cfb4-h7qbd   1/1     Running   0          58s   10.244.0.5   minikube
my-pods-8d5f6cfb4-pdg96   1/1     Running   0          58s   10.244.0.4   minikube
```

curlコマンドで、アクセスすると、応答のIPアドレスから、ランダムにポッドへ割り振られることがわかります。
```
$ curl http://localhost:9100/info
Host Name: my-pods-8d5f6cfb4-pdg96
Host IP: 10.244.0.4
Client IP : 10.244.0.1

$ curl http://localhost:9100/info
Host Name: my-pods-8d5f6cfb4-pdg96
Host IP: 10.244.0.4
Client IP : 10.244.0.1

$ curl http://localhost:9100/info
Host Name: my-pods-8d5f6cfb4-h7qbd
Host IP: 10.244.0.5
Client IP : 10.244.0.1

$ curl http://localhost:9100/info
Host Name: my-pods-8d5f6cfb4-pdg96
Host IP: 10.244.0.4
Client IP : 10.244.0.1

$ curl http://localhost:9100/info
Host Name: my-pods-8d5f6cfb4-bgdtq
Host IP: 10.244.0.3
Client IP : 10.244.0.1
```


## クリーンナップ
```
minikube delete
```


## 参照資料
- https://minikube.sigs.k8s.io/docs/handbook/accessing/#loadbalancer-access
- https://minikube.sigs.k8s.io/docs/commands/tunnel/
- https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/
