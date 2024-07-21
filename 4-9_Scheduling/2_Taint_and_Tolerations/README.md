# テイント & トーラレーション
テイントは、特定ノードへポッドを配置禁止にする。
トーラレーションは、許可されたポッドだけが、ノードへ配置される。

##　　準備
```
$ minikube start -n 3
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl get node minikube -o jsonpath='{.spec.taints}' |jq
[
  {
    "effect": "NoSchedule",
    "key": "workload"
  }
]
```

## テイント
コントロールプレーンにポッドが配置されない様にテイントを付与する。デプロイメントを適用して、結果を確認する。
```
$ kubectl create deployment my-pods --image=ghcr.io/takara9/ex1:1.5 --replicas=2
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66dbbd8bd4-4bcz2   1/1     Running   0          22s   10.244.2.2   minikube-m03
my-pods-66dbbd8bd4-swbhc   1/1     Running   0          22s   10.244.1.2   minikube-m02
```

特定ノードから実行中ポッドを退避させる
```
$ kubectl taint nodes minikube-m02 workload:NoExecute
$ kubectl get node minikube-m02 -o jsonpath='{.spec.taints}' |jq
[
  {
    "effect": "NoExecute",
    "key": "workload"
  }
]
$ kubectl get po -o wide
NAME                       READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-66dbbd8bd4-4bcz2   1/1     Running   0          78s   10.244.2.2   minikube-m03
my-pods-66dbbd8bd4-hr69v   1/1     Running   0          18s   10.244.2.3   minikube-m03
```


テイントを削除して、ポッドを再配置
```
$ kubectl taint nodes minikube-m02 workload:NoExecute-
$ kubectl rollout restart deployment my-pods
$ kubectl get pods -o wide
NAME                      READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-bbf5bcf4b-hfzkd   1/1     Running   0          12s   10.244.2.4   minikube-m03
my-pods-bbf5bcf4b-jpq2w   1/1     Running   0          14s   10.244.1.3   minikube-m02
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


## トーラレーション
テイントが付与されたノードへ、ポッドを配置する
deployment-toler.yaml の抜粋
```
    spec:
      containers:
        - name: ubuntu
          image: ghcr.io/takara9/ex1:1.5
      tolerations:       # ノードに一致するテイントがあれば配置可能となる
        - key: "workload"
          operator: "Exists"
          effect: "NoSchedule"
```

前のデプロイメントを削除して、トーラレーション付きのデプロイメントを適用する。
コントロールプレーンとしてテイントを付与されたノードにもポッドが配置された。
```
$ minikube delete
$ minikube start
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl apply -f deployment-toler.yaml
$ kubectl get pods -o wide
NAME                      READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-bbf5bcf4b-hfzkd   1/1     Running   0          12s   10.244.2.4   minikube-m03
my-pods-bbf5bcf4b-jpq2w   1/1     Running   0          14s   10.244.1.3   minikube-m02
```


## クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

