## Lokiのインストール


helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
# helm inspect values grafana/loki > values2.yml
helm install -n monitoring --values values.yaml loki grafana/loki-stack 

$ kubectl get po -n monitoring 
NAME                                                READY   STATUS    RESTARTS   AGE
grafana-8b68b8dc6-nkkbs                             1/1     Running   0          19m
loki-0                                              1/1     Running   0          3m38s
loki-promtail-fxmgl                                 1/1     Running   0          3m38s
prometheus-alertmanager-0                           1/1     Running   0          19m
prometheus-kube-state-metrics-f7c68b84f-xz6hl       1/1     Running   0          19m
prometheus-prometheus-node-exporter-2bgsq           1/1     Running   0          19m
prometheus-prometheus-pushgateway-568fbf799-vjl9f   1/1     Running   0          19m
prometheus-server-6949d6cfdd-nqvjm                  2/2     Running   0          19m

Grafanaのデータソースに次のURLをセットする
http://loki.monitoring.svc.cluster.local:3100

