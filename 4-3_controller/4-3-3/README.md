

https://minikube.sigs.k8s.io/docs/tutorials/volume_snapshots_and_csi/


minikube start
minikube addons enable csi-hostpath-driver


## データベースのポッドでクライアントを実行

```
$ kubectl exec -it db-0 -- bash
```

```
mysql@db-0:/$ mariadb --user user1 --password=secret-passwd1 mydb
```


## 対話型bashコマンドからMariaDBクライアントを起動

```
$ kubectl run -it client --rm --image=mariadb -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# 
```

```
root@client:/# mariadb --host db --port 3306 --user user1 --password=secret-passwd1 mydb
```


## kubectlコマンドからMariaDBクライアントを起動

```
$ kubectl run -it client --rm --image=mariadb -- mariadb --host db --port 3306 --user user1 --password=secret-passwd1 mydb
```


##

$ kubectl exec -it db-0 -c db -- bash
$ mariadb --user user1 --password=secret-passwd1 mydb

CREATE TABLE Persons (PersonID int, LastName varchar(50),FirstName varchar(50));
INSERT INTO Persons VALUES (1, "sazae","fuguta");
INSERT INTO Persons VALUES (2, "masuo","fuguta");
INSERT INTO Persons VALUES (3, "namihei","isono");


kubectl exec -it db-1 -c db -- bash



~~~
$ kubectl apply -f statefulsets-mariadb-single.yaml 
secret/mariadb-secret created
service/db created
statefulset.apps/db created

$ kubectl get sts
NAME   READY   AGE
db     0/1     8s

$ kubectl get po -w
NAME   READY   STATUS    RESTARTS   AGE
db-0   0/1     Pending   0          13s
db-0   0/1     Pending   0          20s
db-0   0/1     ContainerCreating   0          20s
db-0   1/1     Running             0          33s
^C

$ kubectl get pvc
NAME           STATUS  VOLUME         CAPACITY  ACCESS MODES  STORAGECLASS      AGE
data-vol-db-0  Bound   pvc-433d6d30-  200Mi     RWO           csi-hostpath-sc   40s
~~~


~~~
# MariaDBのコンテナを対話型で起動する
$ kubectl run -it client --rm --image=mariadb -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# # MariaDBのクライアントコマンドでログイン
root@client:/# mariadb --host db --port 3306 --user user1 --password=secret-passwd1 mydb
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 3
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mydb               |
+--------------------+
2 rows in set (0.000 sec)

MariaDB [mydb]> 
~~~



~~~
$ minikube delete
🔥  qemu2 の「minikube」を削除しています...
💀  クラスター「minikube」の全てのトレースを削除しました。

$ minikube start
😄  Darwin 14.4.1 (arm64) 上の minikube v1.32.0
✨  qemu2 ドライバーが自動的に選択されました
🌐  builtin ネットワークが自動的に選択されました
❗  You are using the QEMU driver without a dedicated network, which doesn't support `minikube service` & `minikube tunnel` commands.
To try the dedicated network see: https://minikube.sigs.k8s.io/docs/drivers/qemu/#networking
👍  minikube クラスター中のコントロールプレーンの minikube ノードを起動しています
🔥  qemu2 VM (CPUs=2, Memory=4000MB, Disk=20000MB) を作成しています...
🐳  Docker 24.0.7 で Kubernetes v1.28.3 を準備しています...
    ▪ 証明書と鍵を作成しています...
    ▪ コントロールプレーンを起動しています...
    ▪ RBAC のルールを設定中です...
🔗  bridge CNI (コンテナーネットワークインターフェース) を設定中です...
    ▪ gcr.io/k8s-minikube/storage-provisioner:v5 イメージを使用しています
🔎  Kubernetes コンポーネントを検証しています...
🌟  有効なアドオン: storage-provisioner, default-storageclass
🏄  終了しました！kubectl がデフォルトで「minikube」クラスターと「default」ネームスペースを使用するよう設定されました

$ minikube addons enable csi-hostpath-driver
💡  csi-hostpath-driver is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
❗  [警告] フル機能のために、'csi-hostpath-driver' アドオンが 'volumesnapshots' アドオンの有効化を要求しています。

'minikube addons enable volumesnapshots' を実行して 'volumesnapshots' を有効化できます

    ▪ registry.k8s.io/sig-storage/csi-resizer:v1.6.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-snapshotter:v6.1.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-provisioner:v3.3.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-attacher:v4.0.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-external-health-monitor-controller:v0.7.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/csi-node-driver-registrar:v2.6.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/hostpathplugin:v1.9.0 イメージを使用しています
    ▪ registry.k8s.io/sig-storage/livenessprobe:v2.8.0 イメージを使用しています
🔎  csi-hostpath-driver アドオンを検証しています...
🌟  'csi-hostpath-driver' アドオンが有効です
~~~

~~~
$ kubectl get no
NAME       STATUS   ROLES           AGE    VERSION
minikube   Ready    control-plane   104s   v1.28.3
~~~


~~~
$ kubectl apply -f statefulsets-mariadb-cluster.yaml 
configmap/mariadb-configmap created
secret/mariadb-secret created
service/db created
statefulset.apps/db created

$ kubectl get sts
NAME   READY   AGE
db     0/3     7s

$ kubectl get po -w
NAME   READY   STATUS     RESTARTS   AGE
db-0   0/1     Init:0/1   0          11s
db-0   0/1     PodInitializing   0          15s
db-0   1/1     Running           0          16s
db-1   0/1     Pending           0          0s
db-1   0/1     Pending           0          0s
db-1   0/1     Pending           0          14s
db-1   0/1     Init:0/1          0          14s
db-1   0/1     PodInitializing   0          18s
db-1   1/1     Running           0          19s
db-2   0/1     Pending           0          0s
db-2   0/1     Pending           0          0s
db-2   0/1     Pending           0          17s
db-2   0/1     Init:0/1          0          17s
db-2   0/1     PodInitializing   0          20s
db-2   1/1     Running           0          21s
^C

$ kubectl get po 
NAME   READY   STATUS    RESTARTS   AGE
db-0   1/1     Running   0          82s
db-1   1/1     Running   0          66s
db-2   1/1     Running   0          47s

$ kubectl get sts
NAME   READY   AGE
db     3/3     85s

$ kubectl get pvc
NAME            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS      AGE
data-vol-db-0   Bound    pvc-7aa8bc71-5179-44fa-ac8a-0fcf24b30f71   200Mi      RWO            csi-hostpath-sc   88s
data-vol-db-1   Bound    pvc-fb0472d4-d6ab-4a37-acad-0e421a44b33c   200Mi      RWO            csi-hostpath-sc   72s
data-vol-db-2   Bound    pvc-b936f9a7-5440-4511-9b0e-874e0f691ad4   200Mi      RWO            csi-hostpath-sc   53s

$ kubectl get svc
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
db           ClusterIP   None         <none>        3306/TCP   94s
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP    3m44s

$ kubectl get cm
NAME                DATA   AGE
kube-root-ca.crt    1      3m33s
mariadb-configmap   4      97s

$ kubectl get secret
NAME             TYPE     DATA   AGE
mariadb-secret   Opaque   2      101s
~~~


kubectl run -it client --rm --image=mariadb -- bash
mariadb --host db-0.db --port 3306 --user user1 --password=secret-passwd1 mydb

~~~
$ kubectl run -it client --rm --image=mariadb -- bash
If you don't see a command prompt, try pressing enter.

root@client:/# mariadb --host db-0.db --port 3306 --user user1 --password=secret-passwd1 mydb
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 6
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204-log mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> CREATE TABLE Persons (PersonID int, LastName varchar(50),FirstName varchar(50));
Query OK, 0 rows affected (0.001 sec)

MariaDB [mydb]> INSERT INTO Persons VALUES (1, "sazae","fuguta");
Query OK, 1 row affected (0.000 sec)

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
+----------+----------+-----------+
1 row in set (0.000 sec)

~~~


~~~
root@client:/# mariadb --host db-1.db --port 3306 --user user1 --password=secret-passwd1 mydb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 6
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
+----------+----------+-----------+
1 row in set (0.000 sec)
~~~



~~~
MariaDB [mydb]> INSERT INTO Persons VALUES (2, "masuo","fuguta");
Query OK, 1 row affected (0.000 sec)

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
|        2 | masuo    | fuguta    |
+----------+----------+-----------+
2 rows in set (0.000 sec)


root@client:/# mariadb --host db-0.db --port 3306 --user user1 --password=secret-passwd1 mydb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 7
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204-log mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
+----------+----------+-----------+
1 row in set (0.000 sec)

~~~



~~~
root@client:/# mariadb --host db-2.db --port 3306 --user user1 --password=secret-passwd1 mydb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 6
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
+----------+----------+-----------+
1 row in set (0.000 sec)
~~~



~~~
$ kubectl get pod
NAME   READY   STATUS    RESTARTS   AGE
db-0   1/1     Running   0          9m56s
db-1   1/1     Running   0          9m40s
db-2   1/1     Running   0          9m21s

$ kubectl delete pod db-0
pod "db-0" deleted

$ kubectl get pod
NAME   READY   STATUS    RESTARTS   AGE
db-0   1/1     Running   0          4s
db-1   1/1     Running   0          9m55s
db-2   1/1     Running   0          9m36s

$ kubectl run -it client --rm --image=mariadb -- bash
If you don't see a command prompt, try pressing enter.
root@client:/# mariadb --host db-0.db --port 3306 --user user1 --password=secret-passwd1 mydb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 6
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204-log mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
+----------+----------+-----------+
1 row in set (0.000 sec)

MariaDB [mydb]> INSERT INTO Persons VALUES (3, "namihei","isono");
Query OK, 1 row affected (0.000 sec)

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
|        3 | namihei  | isono     |
+----------+----------+-----------+
2 rows in set (0.000 sec)

MariaDB [mydb]> ^DBye
root@client:/# mariadb --host db-2.db --port 3306 --user user1 --password=secret-passwd1 mydb
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 7
Server version: 11.3.2-MariaDB-1:11.3.2+maria~ubu2204 mariadb.org binary distribution

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [mydb]> SELECT * FROM Persons;
+----------+----------+-----------+
| PersonID | LastName | FirstName |
+----------+----------+-----------+
|        1 | sazae    | fuguta    |
|        3 | namihei  | isono     |
+----------+----------+-----------+
2 rows in set (0.000 sec)
~~~