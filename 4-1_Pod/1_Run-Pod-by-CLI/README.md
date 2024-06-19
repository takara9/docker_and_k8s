# ポッドの実行開始と起動確認
Kubernetesでのコンテナの実行単位であるポッドをCLIコマンドで直接起動します。


## 準備
最小構成のKubernetesクラスタを起動します。
```
$ minikube start
$ kubectl get node
NAME       STATUS   ROLES           AGE   VERSION
minikube   Ready    control-plane   22s   v1.30.0
```


## 実行例

Webサービスのコンテナを内包したポッドの起動
```
$ kubectl run my-web --image=ghcr.io/takara9/ex3:1.0
```

ポッド起動の確認
```
$ kubectl get pod
NAME     READY   STATUS    RESTARTS   AGE
my-web   1/1     Running   0          9s

$ kubectl get pod -o wide
NAME     READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES
my-web   1/1     Running   0          19s   10.244.0.3   minikube   <none>           <none>
```


対話型シェルのポッドを起動
```
$ kubectl run -it my-pod --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
nobody@my-pod:/$ 

nobody@my-pod:/$ ls
bin  boot  dev  etc  home  lib  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var

nobody@my-pod:/$ ps -ux
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
nobody         1  0.0  0.0   4116  3200 pts/0    Ss   23:25   0:00 bash
nobody        10  0.0  0.0   6408  2432 pts/0    R+   23:27   0:00 ps -ux

nobody@my-pod:/$ curl http://10.244.0.3:3000/ping;echo
pong
nobody@my-pod:/$ exit
```


## クリーンナップ
```
$ kubectl delete pod my-web
$ kubectl delete pod my-pod
$ minikube delete
```


## 参考資料
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_run/
- https://kubernetes.io/docs/reference/kubectl/quick-reference/
- https://kubernetes.io/docs/concepts/workloads/pods/

