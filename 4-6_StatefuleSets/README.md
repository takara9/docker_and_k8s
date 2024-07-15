# ステートフルセット
データベースなどの永続データを管理するミドルウェアなどに適する「コントローラー」です。


## 準備

```
$ minikube start
$ minikube addons disable storage-provisioner
$ minikube addons disable default-storageclass
$ minikube addons enable csi-hostpath-driver
$ kubectl get sc
NAME             PROVISIONER          RECLAIMPOLICY  VOLUMEBINDINGMODE  ALLOWVOLUMEEXPANSION
csi-hostpath-sc  hostpath.csi.k8s.io  Delete         Immediate          false
```


## 実行例
紙面に収まる様に、編集してあります。

```
$ kubectl apply -f minimal-sts.yaml
$ kubectl get sts
NAME          READY   AGE
mariadb-sts   3/3     70s

$ kubectl get po
NAME            READY   STATUS    RESTARTS       AGE
mariadb-sts-0   1/1     Running   0              74s

$ kubectl get pvc
NAME                STATUS  VOLUME            CAPACITY  ACCESS MODES STORAGECLASS     AGE
dbvl-mariadb-sts-0  Bound   pvc-9678f16424f5  20Mi      RWO          csi-hostpath-sc  117s

$ kubectl get pv
NAME              CAPACITY ACCESS MODES  RECLAIM POLICY STATUS CLAIM
pvc-9678f16424f5  20Mi     RWO           Delete         Bound  default/dbvl-mariadb-sts-0
```

IPアドレスの確認
```
$ kubectl get svc mariadb-svc
NAME          TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
mariadb-svc   ClusterIP   None         <none>        3306/TCP   2m59s

$ kubectl get pod -o wide
NAME            READY   STATUS    RESTARTS      AGE     IP            NODE
mariadb-sts-0   1/1     Running   0             3m30s   10.244.0.16   minikube
```
 
内部DNSの確認
```
$ kubectl run -it my-pod --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash
If you don't see a command prompt, try pressing enter.
nobody@my-pod:/$ nslookup mariadb-svc
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   mariadb-svc.default.svc.cluster.local
Address: 10.244.0.16
```

STSのポッドについてアドレス解決を確認
```
nobody@my-pod:/$ nslookup 10.244.0.16
16.0.244.10.in-addr.arpa        name = mariadb-sts-0.mariadb-svc.default.svc.cluster.local.

nobody@my-pod:/$ nslookup mariadb-sts-0.mariadb-svc.default.svc.cluster.local
Server:         10.96.0.10
Address:        10.96.0.10#53

Name:   mariadb-sts-0.mariadb-svc.default.svc.cluster.local
Address: 10.244.0.16
```


```
$ kubectl run -it my-client --image=mariadb:11.3.2-jammy -- bash
If you don't see a command prompt, try pressing enter.
root@my-client:/# mariadb --host mariadb-svc --password
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

MariaDB [(none)]> create database test1;
Query OK, 1 row affected (0.001 sec)

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test1              |
+--------------------+
5 rows in set (0.001 sec)
```


ポッドの削除
```
MariaDB [(none)]> exit
Bye
root@my-client:/# exit
exit
Session ended, resume using 'kubectl attach my-client -c my-client -i -t' command when the pod is running
$ kubectl get pod
NAME            READY   STATUS    RESTARTS      AGE
mariadb-sts-0   1/1     Running   0             4m34s
my-client       1/1     Running   1 (21s ago)   3m35s
$ kubectl delete pod mariadb-sts-0 
pod "mariadb-sts-0" deleted
```


自己回復後のポッドへアクセスして、データが保存されていることを確認
```
$ kubectl exec -it my-client -- bash
root@my-client:/# mariadb --host mariadb-svc --password
Enter password: 
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| test1              |
+--------------------+
5 rows in set (0.001 sec)
```


ステートフルセットのAPIを抜き出したリスト
```
$ kubectl get sts mariadb-sts  -o yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  ＜中略＞
spec:
  persistentVolumeClaimRetentionPolicy:  # 削除時の永続ボリュームの扱い
    whenDeleted: Retain                  # Retain と Delete の選択可
    whenScaled: Retain                   #  同上
  podManagementPolicy: OrderedReady      # ポッドの起動や停止時の順番
  replicas: 1                            # ポッドと永続ボリュームの組みのレプリカ数
  revisionHistoryLimit: 10
  selector:
　　＜中略、管理下ポッドの選択ラベル＞
  serviceName: mariadb-svc               # ポッドをDNSへ登録するサービスを指定
  template:
    ＜中略、ポッドの雛形＞
  updateStrategy:                        # ポッドの更新方法
    rollingUpdate:
      partition: 0                       # 旧ポッドを残す数
    type: RollingUpdate                  # RollingUpdate と OnDelete の選択可
  volumeClaimTemplates:
　　＜中略、永続ボリュームの雛形＞
status:
　＜以下省略＞
```


## クリーンナップ
```
$ minikube deletels
```


## 参考資料
- ステートフルセット https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/
- ステートフルセットAPIリファレンス https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/stateful-set-v1/
- 自動生成 APIリファレンス　https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.30/#statefulset-v1-apps

