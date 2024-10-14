# プライオリティ・クラス

限られたリソース環境で、通常優先度のポッドを退避させて、優先度の高いポッドを実行する。
ただし、悪意のあるユーザーが可能な限り最高の優先度でポッドを作成し、他のポッドが排除されたりスケジュールされなかったりする可能性があります。
管理者は ResourceQuota を使用して、ユーザーが高優先度でポッドを作成できないようにすることができます。


## 準備
```
$ minikube start -n 2
$ minikube addons enable metrics-server
$ kubectl get no
$ kubectl taint nodes minikube workload:NoSchedule
```

ノードの割り当て可能なCPUコア数を確認しておきます。Minikubeの実行環境によって、
割り当て可能なCPU数が異なりますので、環境に対応して調整しなければなりません。

macOS 
```
$ minikube version　コンテナノードで、ホストのCPUコア数が表示されている
minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        8
minikube-m02    8
```

Windows PC (NUC)　コンテナノードで、ホストのCPUコア数が表示されている
```
PS C:\Users\tkr99\docker_and_k8s> minikube version
W1014 17:34:15.000292    3328 main.go:291] Unable to resolve the current Docker CLI context "default": context "default": context not found: open C:\Users\tkr99\.docker\contexts\meta\37a8eec1ce19687d132fe29051dca629d164e2c4958ba141d5f4133a33f0688f\meta.json: The system cannot find the path specified.
minikube version: v1.33.1
commit: 5883c09216182566a63dff4c326a6fc9ed2982ff
PS C:\Users\tkr99\docker_and_k8s> kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        4
minikube-m02    4
```

Linux ノードをコンテナでシミュレートしたケース
```
$ minikube start -n 2
$ minikube version
minikube version: v1.34.0
commit: 210b148df93a80eb872ecbeb7e35281b3c582c61

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        12
minikube-m02    12
```

Linux ノードをVMで起動したケース
```
$ minikube start -n 2 --vm-driver=kvm2
$ minikube version
minikube version: v1.34.0
commit: 210b148df93a80eb872ecbeb7e35281b3c582c61

$ kubectl get no -o=jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.allocatable.cpu}{"\n"}{end}'
minikube        2
minikube-m02    2
```



## プライオリティクラスの設定
```
$ kubectl apply -f priority-class.yaml 
$ kubectl get pc high-priority
NAME            VALUE     GLOBAL-DEFAULT   AGE
high-priority   1000000   false            14s
```

## プライオリティクラスなしのデプロイメントの適用
割り当て可能なCPU数で、動作が異なりますから、
minikubeのリソース一杯のCPU要求数でデプロイする。これ以上レプリカ数を増やしても、リソースが確保されず Pending となる。

```
$ kubectl apply -f deployment-normal.yaml
$ kubectl get po -o wide
NAME                              READY   STATUS    RESTARTS   AGE   IP           NODE
my-pods-normal-7f696b6b96-8kr4p   1/1     Running   0          19s   10.244.1.2   minikube-m02
my-pods-normal-7f696b6b96-cp4bj   1/1     Running   0          19s   10.244.1.4   minikube-m02
my-pods-normal-7f696b6b96-qrncv   1/1     Running   0          19s   10.244.1.3   minikube-m02
```

## 高優先度のデプロイメントの適用
プライオリィクラス high-priority を設定してデプロイする。
その結果、優先度を指定しない低優先度のポッドは押しのけられ、Pending状態になり、高優先度のポッドに置き換わる。
```
$ kubectl apply -f deployment-hp.yaml 
$ kubectl get po -o wide
NAME                                     READY   STATUS    AGE   IP           NODE
my-pods-high-priority-5cd9c8ccb9-5s6kn   1/1     Running   35s   10.244.1.5   minikube-m02
my-pods-high-priority-5cd9c8ccb9-fb4mv   1/1     Running   35s   10.244.1.6   minikube-m02
my-pods-high-priority-5cd9c8ccb9-xb7kb   1/1     Running   35s   10.244.1.7   minikube-m02
my-pods-normal-7f696b6b96-86zjs          0/1     Pending   35s   <none>       <none>
my-pods-normal-7f696b6b96-gs8p6          0/1     Pending   35s   <none>       <none>
my-pods-normal-7f696b6b96-w6rlk          0/1     Pending   35s   <none>       <none>
```


## 既存で動作しているポッドを退かさない様にするには

priority-class-nonp.yaml(抜粋)
```
apiVersion: scheduling.k8s.io/v1
kind: PriorityClass
metadata:
  name: high-priority
value: 1000000
preemptionPolicy: Never  # これを追加する。他のポッドを押し除けない
```

既存の高優先度のクラスを削除して、上記設定を追加した高優先度クラスを適用する
```
$ kubectl delete -f priority-class.yaml
$ kubectl apply -f priority-class-nonp.yaml 
$ kubectl get pc high-priority
NAME            VALUE     GLOBAL-DEFAULT   AGE
high-priority   1000000   false            42s

$ kubectl describe pc high-priority
Name:              high-priority
Value:             1000000
GlobalDefault:     false
PreemptionPolicy:  Never
Description:       This priority class will not cause other pods to be preempted.
Annotations:       kubectl.kubernetes.io/last-applied-configuration={"apiVersion":"scheduling.k8s.io/v1","description":"This priority class will not cause other pods to be preempted.","globalDefault":false,"kind":"PriorityClass","metadata":{"annotations":{},"name":"high-priority"},"preemptionPolicy":"Never","value":1000000}
<以下省略>
```

「`preemptionPolicy: Never`」によって低優伝度のポッドが止められるのを抑止できた。
```
$ kubectl apply -f deployment-hp.yaml 
$ kubectl get pod -o wide
NAME                                     READY   STATUS    RESTARTS   AGE     IP            NODE
my-pods-high-priority-5cd9c8ccb9-gwpfl   0/1     Pending   0          10s     <none>        <none>
my-pods-high-priority-5cd9c8ccb9-qkfj5   0/1     Pending   0          10s     <none>        <none>
my-pods-high-priority-5cd9c8ccb9-w5z99   0/1     Pending   0          10s     <none>        <none>
my-pods-normal-7f696b6b96-86zjs          1/1     Running   0          9m32s   10.244.1.8    minikube-m02
my-pods-normal-7f696b6b96-gs8p6          1/1     Running   0          9m32s   10.244.1.9    minikube-m02
my-pods-normal-7f696b6b96-w6rlk          1/1     Running   0          9m32s   10.244.1.10   minikube-m02
```

低優先度のポッドを削除すると、高優先度のポッドが起動しました。
```
$ kubectl delete deploy my-pods-normal
deployment.apps "my-pods-normal" deleted

$ kubectl get pod -o wide
NAME                                     READY   STATUS    RESTARTS   AGE   IP            NODE
my-pods-high-priority-5cd9c8ccb9-gwpfl   1/1     Running   0          3m    10.244.1.13   minikube-m02
my-pods-high-priority-5cd9c8ccb9-qkfj5   1/1     Running   0          3m    10.244.1.12   minikube-m02
my-pods-high-priority-5cd9c8ccb9-w5z99   1/1     Running   0          3m    10.244.1.11   minikube-m02
```


## クリーンナップ
```
minikube delete
```


## 参照資料
- https://kubernetes.io/docs/concepts/scheduling-eviction/pod-priority-preemption/
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_create/kubectl_create_priorityclass/
