# イングレス と Gateway API

## 準備

```
$ minikube start
$ minikube addons enable ingress
```

## イングレス実行例
```
$ kubectl apply -f ingress.yaml 
$ kubectl get ingress
NAME              CLASS   HOSTS   ADDRESS        PORTS   AGE
example-ingress   nginx   *       192.168.49.2   80      10s
$ minikube tunnel
```


別ターミナルでアクセスする
```
$ curl http://127.0.0.1/foo
Request served by foo-app

HTTP/1.1 GET /foo
```

```
$ curl http://127.0.0.1/bar
Request served by bar-app

HTTP/1.1 GET /bar
```



## クリーンナップ
```
minikube delete
```


## 参考資料
Ingress
- https://kubernetes.io/docs/concepts/services-networking/ingress/
- https://minikube.sigs.k8s.io/docs/tutorials/nginx_tcp_udp_ingress/
- https://kubernetes.io/docs/tasks/access-application-cluster/ingress-minikube/
- https://gateway-api.sigs.k8s.io/guides/migrating-from-ingress/#migrating-from-ingress

Gateway API
- https://kubernetes.io/blog/2023/10/31/gateway-api-ga/
- https://kubernetes.io/docs/concepts/services-networking/gateway/
- https://gateway-api.sigs.k8s.io/
