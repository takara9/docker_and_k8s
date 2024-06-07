# テイント & トーラレーション
テイントは、特定ノードへポッドを配置禁止にする。
トーラレーションは、許可されたポッドだけが、ノードへ配置される。

##　　準備
```
$ minikube start -n 3
$ kubectl get no
```

## テイント
コントロールプレーンにポッドが配置されない様にテイントを付与する。
デプロイメントを適用して、結果を確認する。
```
$ kubectl taint nodes minikube controller:NoSchedule
$ kubectl apply -f deployment-none-toler.yaml
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-76668bb48c-cqtdn   1/1     Running   0          27s   10.244.1.2   minikube-m02
my-pods-76668bb48c-k7nj6   1/1     Running   0          27s   10.244.2.3   minikube-m03
my-pods-76668bb48c-rlpph   1/1     Running   0          27s   10.244.2.2   minikube-m03
my-pods-76668bb48c-vm7kj   1/1     Running   0          27s   10.244.1.3   minikube-m02
my-pods-76668bb48c-wkcb6   1/1     Running   0          27s   10.244.2.4   minikube-m03
```

### トーラレーション
テイントが付与されたノードへ、ポッドを配置する
deployment-toler.yaml の抜粋
```
      tolerations:
        - key: "controller"
          operator: "Exists"
          effect: "NoSchedule"
```

前のデプロイメントを削除して、トーラレーション付きのデプロイメントを適用する。
コントロールプレーンとしてテイントを付与されたノードにもポッドが配置された。
```
$ kubectl delete deploy my-pods
$ kubectl apply -f deployment-toler.yaml
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-5986fbd876-5xccc   1/1     Running   0          18s   10.244.0.4   minikube
my-pods-5986fbd876-6rlxg   1/1     Running   0          18s   10.244.1.5   minikube-m02
my-pods-5986fbd876-8vzv2   1/1     Running   0          18s   10.244.1.4   minikube-m02
my-pods-5986fbd876-rmtwz   1/1     Running   0          18s   10.244.2.5   minikube-m03
my-pods-5986fbd876-szpg7   1/1     Running   0          18s   10.244.2.6   minikube-m03
```



｀｀｀｀｀｀｀｀｀｀　トーラレーションの無いポッドだけを追い出すとするのが、ドレインとの区別ができて良い

## テイント
特定ノードから実行中ポッドを退避させる

```
$ kubectl apply -f deployment-none-toler.yaml
$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66974f9784-8sl7j   1/1     Running   0          19s   10.244.1.2   minikube-m02
my-pods-66974f9784-b2t4l   1/1     Running   0          19s   10.244.2.3   minikube-m03
my-pods-66974f9784-ljzj7   1/1     Running   0          19s   10.244.1.3   minikube-m02
my-pods-66974f9784-q8f8d   1/1     Running   0          19s   10.244.2.2   minikube-m03
my-pods-66974f9784-vr4sq   1/1     Running   0          19s   10.244.1.4   minikube-m02
```

テイントを付与してノードから退避
```
$ kubectl taint nodes minikube-m02 workload:NoExecute
$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE    IP            NODE
my-pods-76668bb48c-4lwnb   1/1     Running   0          101s   10.244.2.9    minikube-m03
my-pods-76668bb48c-bqf92   1/1     Running   0          101s   10.244.2.8    minikube-m03
my-pods-76668bb48c-h2zlv   1/1     Running   0          101s   10.244.2.7    minikube-m03
my-pods-76668bb48c-p7nxb   1/1     Running   0          42s    10.244.2.11   minikube-m03
my-pods-76668bb48c-thwsd   1/1     Running   0          42s    10.244.2.10   minikube-m03
```

テイントの削除と再配置
```
$ kubectl taint nodes minikube-m02 workload:NoExecute-
$ kubectl rollout restart deployment my-pods
$ kubectl get pods -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP            NODE
my-pods-58675dff7d-44f6j   1/1     Running   0          75s   10.244.1.10   minikube-m02
my-pods-58675dff7d-jg965   1/1     Running   0          76s   10.244.2.12   minikube-m03
my-pods-58675dff7d-n7t7t   1/1     Running   0          76s   10.244.1.9    minikube-m02
my-pods-58675dff7d-nk2qn   1/1     Running   0          75s   10.244.2.13   minikube-m03
my-pods-58675dff7d-ntgnt   1/1     Running   0          76s   10.244.1.8    minikube-m02
```

tolerationSecondsで、テイントで追い出されるまでの猶予時間を設定できる。
deployment-toler-2.yaml(抜粋)
```
      tolerations:
        - key: "workload"
          operator: "Equal"
          value: "true"
          effect: "NoExecute"
          tolerationSeconds: 600
```


## 参考資料
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

