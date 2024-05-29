# ノードセレクター と ノードネーム
ノードセレクター(nodeSelector)は、ラベルと一致するノードへ、ポッドを選択的に配置します。
ノードネーム(nodeName)は、ノードの名前を指定して、ポッドを配置します。



## ノードセレクター(nodeSelector)

ノードのラベルと一致するノードへ、ポッドを選択的にスケージュール（配置）する。

```
$ minikube start -n 3
$ kubectl label nodes minikube-m02 disktype=ssd
$ kubectl apply -f deployment-ns.yaml 
$ kubectl get po -o wide
NAME                       READY   STATUS    AGE    IP           NODE
my-pods-778bf5d8fd-mpv5t   1/1     Running   32s    10.244.1.4   minikube-m02
my-pods-778bf5d8fd-r7q26   1/1     Running   32s    10.244.1.5   minikube-m02
my-pods-778bf5d8fd-zkkp8   1/1     Running   32s    10.244.1.3   minikube-m02
```

## ノードネーム(nodeName)
ポッドの配置先をノード名で決定します。

```
$ kubectl apply -f deployment-nn.yaml
$ kubectl get po -o wide
NAME                       READY   STATUS        AGE     IP           NODE
my-pods-744c85b57-4pd5r    1/1     Running       21s     10.244.2.3   minikube-m03
my-pods-744c85b57-j9pvm    1/1     Running       9s      10.244.2.5   minikube-m03
my-pods-744c85b57-kxvts    1/1     Running       10s     10.244.2.4   minikube-m03
my-pods-778bf5d8fd-mpv5t   1/1     Terminating   5m26s   10.244.1.4   minikube-m02
my-pods-778bf5d8fd-r7q26   1/1     Terminating   5m26s   10.244.1.5   minikube-m02
my-pods-778bf5d8fd-zkkp8   1/1     Terminating   5m26s   10.244.1.3   minikube-m02

$ kubectl get po -o wide
NAME                      READY   STATUS    AGE    IP           NODE
my-pods-744c85b57-4pd5r   1/1     Running   96s    10.244.2.3   minikube-m03
my-pods-744c85b57-j9pvm   1/1     Running   84s    10.244.2.5   minikube-m03
my-pods-744c85b57-kxvts   1/1     Running   85s    10.244.2.4   minikube-m03
```




> https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/
> ノードからの退避
> メンテナンスなどの理由で、スケジュールを禁止する
> デバイスのあるノードへスケジュール
> https://kubernetes.io/docs/tasks/configure-pod-container/
> assign-pods-nodes-using-node-affinity/
> 均等に分散配置する。



