## Dashboard 

ダッシュボードの起動方法


minikube addons enable dashboard
minikube addons enable metrics-server
minikube dashboard --url


mini:docker_and_k8s takara$ minikube addons enable dashboard
💡  dashboard is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ docker.io/kubernetesui/metrics-scraper:v1.0.8 イメージを使用しています
    ▪ docker.io/kubernetesui/dashboard:v2.7.0 イメージを使用しています
💡  いくつかのダッシュボード機能は metrics-server アドオンを必要とします。全機能を有効にするためには、次のコマンドを実行します:

        minikube addons enable metrics-server


🌟  'dashboard' アドオンが有効です
mini:docker_and_k8s takara$ minikube addons enable metrics-server
💡  metrics-server is an addon maintained by Kubernetes. For any concerns contact minikube on GitHub.
You can view the list of minikube maintainers at: https://github.com/kubernetes/minikube/blob/master/OWNERS
    ▪ registry.k8s.io/metrics-server/metrics-server:v0.6.4 イメージを使用しています
🌟  'metrics-server' アドオンが有効です
mini:docker_and_k8s takara$ kubectl --namespace monitoring port-forward $POD_NAME 3000
mini:docker_and_k8s takara$ minikube dashboard --url
🤔  ダッシュボードの状態を検証しています...
🚀  プロキシーを起動しています...
🤔  プロキシーの状態を検証しています...
http://127.0.0.1:65389/api/v1/namespaces/kubernetes-dashboard/services/http:kubernetes-dashboard:/proxy/