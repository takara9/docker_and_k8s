# ネットワークポリシー
ポッドのアクセスコントロールを設定します。


## 準備
ネットワークのアクセス制御を実装している CNIプラグインを指定します。
ネットワークポリシーを有効化するプラグインとして、calico、cilium などがあります。
```
minikube start --cni calico
```

Nginxのデプロイメントとサービスを作成します。
```
$ kubectl create deployment nginx --image=nginx
$ kubectl expose deployment nginx --port=80
```

ネットワークポリシーが無い状態で、ポッドのcurlコマンドでアクセスできることを確認します。
```
$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.3 -- /bin/sh
If you don't see a command prompt, try pressing enter.

# curl http://nginx/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
<以下省略>
# exit
```


## アクセス元を、ラベルを持ったポッドに限定

np.yamlでは、ラベル access=true に限定する様にします。
```
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: access-nginx
spec:
  ingress:
  - from:
    - podSelector:
        matchLabels:
          access: "true"
```

この設定により、ポッドにラベルが無ければアクセスできません。
```
$ kubectl apply -f np.yaml 
$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.3 -- /bin/sh

$ curl http://nginx/
^C
$ 
```

ラベルを付与したポッドではアクセスがきます。
```
$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.3 --labels="access=true" -- bash
$ curl http://rest-service.prod.svc.cluster.local:9100/info
Host Name: my-pods-5c84c44bc6-nhd6m
Host IP: 10.244.120.73
Client IP : 10.244.120.76
```


## アクセス元をネームスペースに限定する
前述のネットワークポリシーは、削除しておきます。
ネームスペースを作成して、Nginxにアクセスできる様に、ラベルを付与します。
```
$ kubectl delete -f np.yaml 
$ kubectl create ns client
$ kubectl label namespace client access=true
$ kubectl get ns --show-labels client
NAME     STATUS   AGE    LABELS
client   Active   117s   access=true,kubernetes.io/metadata.name=client
$ kubectl apply -f np-namespace.yaml
```

ネームスペースに、curlクライアントでアクセスするポッドを作成します。
curlコマンドで、デフォルトネームスペースのnginxへアクセスできることが確認できました。
```
$ kubectl run my-pod --rm -ti -n client --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
nobody@my-pod:/$ curl http://nginx.default/
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<以下省略>
```

今後は、ラベルが付与されたネームスペース client 以外からアクセスできない事を確認するため、デフォルトのネームスペースから
curlでアクセスできるかテストします。結果は、応答がありませんでした。
```
$ kubectl run my-pod --rm -ti --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
nobody@my-pod:/$ curl http://nginx/
^C
```


## クリーンナップ
```
minikube delete
```


## 参考資料
- https://kubernetes.io/docs/concepts/services-networking/network-policies/
- https://docs.tigera.io/calico/latest/network-policy/get-started/kubernetes-policy/kubernetes-policy-advanced
