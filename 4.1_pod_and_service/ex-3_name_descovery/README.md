ネームスペースと名前解決




# DNS

mini:~ takara$ kubectl run -it mypod --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash
If you don't see a command prompt, try pressing enter.
root@mypod:/# 

root@mypod:/# nslookup www.google.com
Server:		10.96.0.10
Address:	10.96.0.10#53

Non-authoritative answer:
Name:	www.google.com
Address: 172.217.24.68
Name:	www.google.com
Address: 2404:6800:4004:827::2004

## PodのDNS名

mini:~ takara$ kubectl get po -o wide
NAME    READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
mypod   1/1     Running   0          3m37s   10.244.1.2   minikube-m02   <none>           <none>


もう一つポッドを起動して、mypodがDNSに登録されている状況を確認します。

mini:~ takara$ kubectl run -it mypod2 --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash
If you don't see a command prompt, try pressing enter.
root@mypod2:/# dig 10-244-1-2.default.pod.cluster.local +short
10.244.1.2


## サービスとポッドのDNS名

manifest-1で、サービスとポッドを起動します。

mini:4.1 takara$ pwd
/Users/takara/docker_and_k8s/4.1
mini:4.1 takara$ kubectl apply -f manifest-1
pod/my-pod created
service/my-service created

サービスが起動しているのが解ります。

mini:4.1 takara$ kubectl get svc
NAME         TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)          AGE
kubernetes   ClusterIP   10.96.0.1        <none>        443/TCP          10m
my-service   NodePort    10.106.140.136   <none>        9100:32343/TCP   23s

別のターミナルで、対話型ポッドを起動します。

mini:~ takara$ kubectl run -it mypod2 --image=ghcr.io/takara9/my-ubuntu:0.2 -- bash
If you don't see a command prompt, try pressing enter.

DNS名でアドレスを求めてみましょう。　サービス名.ネームスペース.svc.cluster.local　でアドレスを引けます。

root@mypod2:/# dig my-service.default.svc.cluster.local +short
10.106.140.136

環境変数にもセットされています。ただし、サービスの後に起動されたポッドに、限られます。

root@mypod2:/# env |grep MY_SERVICE
MY_SERVICE_SERVICE_HOST=10.106.140.136
MY_SERVICE_SERVICE_PORT_MY_SERVICE=9100
MY_SERVICE_PORT=tcp://10.106.140.136:9100
MY_SERVICE_PORT_9100_TCP=tcp://10.106.140.136:9100
MY_SERVICE_PORT_9100_TCP_PROTO=tcp
MY_SERVICE_PORT_9100_TCP_ADDR=10.106.140.136
MY_SERVICE_SERVICE_PORT=9100
MY_SERVICE_PORT_9100_TCP_PORT=9100


root@mypod2:/# curl http://my-service.default.svc.cluster.local:$MY_SERVICE_SERVICE_PORT_MY_SERVICE/ping;echo
<p>pong</p>

PodのDNS名登録

root@mypod2:/# dig 10-244-1-3.default.pod.cluster.local +short
10.244.1.3

