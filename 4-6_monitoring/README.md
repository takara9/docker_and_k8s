https://qiita.com/sotoiwa/items/804155aca5ec6d52bac0

# Lokiを起動する

https://github.com/helm/helm/releases



kubectl get secret --namespace default loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo



https://github.com/grafana/helm-charts


https://grafana.com/docs/loki/latest/setup/install/helm/install-monolithic/





## プロメテウスのインストール

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

kubectl create ns monitoring
helm install -n monitoring prometheus prometheus-community/prometheus


## グラファナのインストール

helm repo add grafana https://grafana.github.io/helm-charts
helm install -n monitoring grafana grafana/grafana


## グラファナへのアクセス

kubectl get secret --namespace monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
export POD_NAME=$(kubectl get pods --namespace monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")

kubectl --namespace monitoring port-forward $POD_NAME 3000


http://localhost:3000/


## Lokiのインストール

minikube addons enable ingress


helm repo add grafana https://grafana.github.io/helm-charts
helm repo update


helm inspect values grafana/loki > values2.yml
helm install --namespace monitoring --values values.yaml loki grafana/loki-stack

http://loki.monitoring.svc.cluster.local:3100



## promtail のインストール
https://grafana.com/docs/loki/latest/send-data/promtail/installation/



helm upgrade --install promtail -n monitoring grafana/promtail 

docker pull grafana/loki:2.8.0-amd64