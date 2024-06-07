# トポロジー・スプレッド・コンストレインツ
ゾーンとノードに均一に分散させてポッドを配置する。


## 準備
コントロールプレーンにポッドの配置を禁止して、アベイラビリティーゾーンを想定したゾーンを設定する。

```console
minikube start --nodes=5
kubectl taint nodes minikube key1=value1:NoSchedule
kubectl label nodes minikube-m02 topology.kubernetes.io/zone="jp-tokyo-1a"
kubectl label nodes minikube-m03 topology.kubernetes.io/zone="jp-tokyo-1b"
kubectl label nodes minikube-m04 topology.kubernetes.io/zone="jp-tokyo-1c"
kubectl get nodes -o=jsonpath='{.items[*].metadata.labels}' |jq -r .
```


##　 トポロジー・スプレッド・コンストレインツの設定部分
deployment-tsc.yaml(抜粋)
```
<前略>    
      topologySpreadConstraints:   # トポロジー・スプレッド・コンストレインツ
        - topologyKey: kubernetes.io/hostname  # ノードの分散配置
          maxSkew: 1
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-pod
        - topologyKey: topology.kubernetes.io/zone  # ゾーンに分散配置
          maxSkew: 1
          whenUnsatisfiable: DoNotSchedule
          labelSelector:
            matchLabels:
              app: my-pod
<以下省略>
```


## デプロイした結果
ポッドが、ノードに３つづつ均等にされている事が確認できる。

```console
$ kubectl apply -f deployment-tsc.yaml 
$ kubectl get po -o wide
NAME                       READY   STATUS    AGE   IP           NODE
my-pods-68786c8db9-8pv87   1/1     Running   33s   10.244.3.3   minikube-m04
my-pods-68786c8db9-f5qsh   1/1     Running   33s   10.244.1.3   minikube-m02
my-pods-68786c8db9-ggqv2   1/1     Running   33s   10.244.2.3   minikube-m03
my-pods-68786c8db9-gpngh   1/1     Running   33s   10.244.2.5   minikube-m03
my-pods-68786c8db9-pf7lm   1/1     Running   33s   10.244.2.4   minikube-m03
my-pods-68786c8db9-ppgq7   1/1     Running   33s   10.244.3.4   minikube-m04
my-pods-68786c8db9-sk8lr   1/1     Running   33s   10.244.1.4   minikube-m02
my-pods-68786c8db9-tg4zr   1/1     Running   33s   10.244.3.2   minikube-m04
my-pods-68786c8db9-wbb7v   1/1     Running   33s   10.244.1.5   minikube-m02
```


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/


