## Minikubeのセットアップ

minikube start --memory='7g' --cpus='4'
minikube addons disable storage-provisioner
minikube addons disable default-storageclass
minikube addons list
minikube addons enable ingress
minikube addons enable csi-hostpath-driver

# minikube addons enable volumesnapshots
kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
kubectl get sc

## プロメテウスのインストール

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
kubectl create ns monitoring
helm install -n monitoring prometheus prometheus-community/prometheus


## グラファナのインストール

helm repo add grafana https://grafana.github.io/helm-charts
helm install -n monitoring grafana grafana/grafana


## グラファナへのアクセス
$ kubectl get po -n monitoring
NAME                                                READY   STATUS    RESTARTS   AGE
grafana-58497f6f96-cxdw6                            1/1     Running   0          38s
prometheus-alertmanager-0                           1/1     Running   0          49s
prometheus-kube-state-metrics-f7c68b84f-szb5s       1/1     Running   0          49s
prometheus-prometheus-node-exporter-fs9f6           1/1     Running   0          49s
prometheus-prometheus-pushgateway-568fbf799-pld7f   1/1     Running   0          49s
prometheus-server-6949d6cfdd-npxlr                  1/2     Running   0          49s

kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
export POD_NAME=$(kubectl get pods -n monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
echo $POD_NAME
kubectl -n monitoring port-forward $POD_NAME 3000
http://localhost:3000/


