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
        - topologyKey: kubernetes.io/hostname       # ノードの分散配置
          maxSkew: 1                                # 許容不均一差
          whenUnsatisfiable: DoNotSchedule          # 条件を満たさな場合、割り当てない
          labelSelector:                            # 適用対象のラベル
            matchLabels:
              app: my-pod
        - topologyKey: topology.kubernetes.io/zone  # ゾーンに分散配置
          maxSkew: 1                                # 以下同上
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
$ kubectl get pods -o=jsonpath='{range .items[*]}{.spec.nodeName}{"\n"}{end}' |sort -k 1|uniq -c
   3 minikube-m02
   3 minikube-m03
   3 minikube-m04
```


## クリーンナップ
```
minikube delete
```


## 参考リンク
- https://kubernetes.io/docs/concepts/scheduling-eviction/topology-spread-constraints/
- https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#topologyspreadconstraint-v1-core



