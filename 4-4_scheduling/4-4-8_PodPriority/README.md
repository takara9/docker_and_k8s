PriorityClass


$ minikube start --nodes=2
$ kubectl get no
$ kubectl taint nodes minikube workload:NoSchedule

$ kubectl apply -f priority-class.yaml 
priorityclass.scheduling.k8s.io/high-priority created

$ kubectl get PriorityClass 
NAME                      VALUE        GLOBAL-DEFAULT   AGE
high-priority             1000000      false            29s
system-cluster-critical   2000000000   false            95s
system-node-critical      2000001000   false            95s


mini:4-4-8_PodPriority takara$ kubectl get pod -o wide
NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-normal-bbdd897d8-bdqc9   0/1     Pending   0          24s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-bfvtk   1/1     Running   0          24s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-bsl6v   1/1     Running   0          24s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-chfgq   1/1     Running   0          24s   10.244.1.3   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-gzm2x   1/1     Running   0          24s   10.244.1.8   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-mtfwj   0/1     Pending   0          24s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-npvcc   1/1     Running   0          24s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-nt6gl   0/1     Pending   0          24s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-nvvxj   1/1     Running   0          24s   10.244.1.7   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-r7jpn   1/1     Running   0          24s   10.244.1.6   minikube-m02   <none>           <none>


mini:4-4-8_PodPriority takara$ kubectl apply -f deployment-hp.yaml 
deployment.apps/my-pods-high created
mini:4-4-8_PodPriority takara$ kubectl get pod -o wide
NAME                             READY   STATUS        RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-high-85bcbc9ff7-5p9jk    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-7pnvb    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-85nzn    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-9gjsr    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-9s8lq    0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-hlwlx    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-jnmp9    0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-n6x7h    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-npsms    0/1     Pending       0          4s    <none>       <none>         minikube-m02     <none>
my-pods-high-85bcbc9ff7-tf4wf    0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-2fd2p   0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-88df5   0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-bbm8q   0/1     Pending       0          3s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-bdqc9   0/1     Pending       0          62s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-bfvtk   1/1     Terminating   0          62s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-bnt2b   0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-bsl6v   1/1     Terminating   0          62s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-chfgq   1/1     Terminating   0          62s   10.244.1.3   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-gzm2x   1/1     Terminating   0          62s   10.244.1.8   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-kkfsz   0/1     Pending       0          4s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-mtfwj   0/1     Pending       0          62s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-npvcc   1/1     Terminating   0          62s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-nt6gl   0/1     Pending       0          62s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-nvvxj   1/1     Terminating   0          62s   10.244.1.7   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-r7jpn   1/1     Terminating   0          62s   10.244.1.6   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-sw88h   0/1     Pending       0          3s    <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-w4t85   0/1     Pending       0          3s    <none>       <none>         <none>           <none>


プライオリィの高いポッドによって、置き換わった。

$ kubectl get pod -o wide
NAME                             READY   STATUS    RESTARTS   AGE    IP            NODE           NOMINATED NODE   READINESS GATES
my-pods-high-85bcbc9ff7-5p9jk    1/1     Running   0          44s    10.244.1.9    minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-7pnvb    1/1     Running   0          44s    10.244.1.15   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-85nzn    1/1     Running   0          44s    10.244.1.11   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-9gjsr    1/1     Running   0          44s    10.244.1.12   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-9s8lq    0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-high-85bcbc9ff7-hlwlx    1/1     Running   0          44s    10.244.1.13   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-jnmp9    0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-high-85bcbc9ff7-n6x7h    1/1     Running   0          44s    10.244.1.14   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-npsms    1/1     Running   0          44s    10.244.1.10   minikube-m02   <none>           <none>
my-pods-high-85bcbc9ff7-tf4wf    0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-2fd2p   0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-88df5   0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-bbm8q   0/1     Pending   0          43s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-bdqc9   0/1     Pending   0          102s   <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-bnt2b   0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-kkfsz   0/1     Pending   0          44s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-mtfwj   0/1     Pending   0          102s   <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-nt6gl   0/1     Pending   0          102s   <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-sw88h   0/1     Pending   0          43s    <none>        <none>         <none>           <none>
my-pods-normal-bbdd897d8-w4t85   0/1     Pending   0          43s    <none>        <none>         <none>           <none>




既存で動作しているポッドを退かさない様にするには


$ minikube start --nodes=2
$ kubectl get nodes
$ kubectl taint nodes minikube workload:NoSchedule
$ kubectl apply -f priority-class-nonp.yaml 
$ kubectl apply -f deployment.yaml 
$ kubectl get pod -o wide
NAME                             READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-normal-bbdd897d8-42tsp   1/1     Running   0          25s   10.244.1.8   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-7f79l   1/1     Running   0          25s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-h6rjh   0/1     Pending   0          25s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-k9p79   0/1     Pending   0          25s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-pqnvf   1/1     Running   0          25s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-pzs7p   1/1     Running   0          25s   10.244.1.7   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-qxflv   1/1     Running   0          25s   10.244.1.6   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-r6nqh   1/1     Running   0          25s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-slj5x   0/1     Pending   0          25s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-vmwpq   1/1     Running   0          25s   10.244.1.3   minikube-m02   <none>           <none>

$ kubectl apply -f deployment-hp.yaml 

$ kubectl get pod -o wide
NAME                             READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
my-pods-high-85bcbc9ff7-57r89    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-62rvg    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-7jn94    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-cnfph    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-dhzh2    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-jbvxh    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-m6pkb    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-rlhs2    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-s5vgd    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-high-85bcbc9ff7-wcmnf    0/1     Pending   0          7m30s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-42tsp   1/1     Running   0          8m27s   10.244.1.8   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-7f79l   1/1     Running   0          8m27s   10.244.1.4   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-h6rjh   0/1     Pending   0          8m27s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-k9p79   0/1     Pending   0          8m27s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-pqnvf   1/1     Running   0          8m27s   10.244.1.2   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-pzs7p   1/1     Running   0          8m27s   10.244.1.7   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-qxflv   1/1     Running   0          8m27s   10.244.1.6   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-r6nqh   1/1     Running   0          8m27s   10.244.1.5   minikube-m02   <none>           <none>
my-pods-normal-bbdd897d8-slj5x   0/1     Pending   0          8m27s   <none>       <none>         <none>           <none>
my-pods-normal-bbdd897d8-vmwpq   1/1     Running   0          8m27s   10.244.1.3   minikube-m02   <none>           <none>