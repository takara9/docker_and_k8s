# ストレージ

演習では、minikube の hostpathについて演習する。

ex1 HostPath
ex2 Secret
ex3 ConfigMap



解説
動的プロビジョニングとストレージクラスとCSI
minikube では動的プロビジョニングは使えない。
クラウドのKuberentesサービスでは、IaaSの永続ボリュームサービスをポッドに接続する形で、永続ディスクの動的なプロビジョニングを実装している。
しかし、そのような動的プロビジョニングに対応するCeph や Longhornと連携しなければ利用はできない。






mini:4.1 takara$ kubectl get sc
NAME                 PROVISIONER                RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
standard (default)   k8s.io/minikube-hostpath   Delete          Immediate           false                  34m


mini:4.1 takara$ kubectl get pv
No resources found

mini:4.1 takara$ kubectl get pvc
No resources found in default namespace.






解説では、クラウドのストレージクラスについて解説

動的プロビジョニングを実施するために必要な、ストレージシステムと連携するコード



３つのストレージについて解説する。


Black 
File
Object

マウントできるのは、上二つ

オブジェクトストレージは、

minio
https://hub.docker.com/r/minio/minio


