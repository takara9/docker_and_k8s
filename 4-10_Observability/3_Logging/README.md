## Lokiのインストール


## Minikubeのセットアップ
グラフィカルな表示などに、CPUとメモリを必要とするので、メモリ4G CPU４コアを設定します。
読者の環境によっては動かせないかもしれませんのが、ご了承ください。
デフォルトのストレージクラスに csi-hostpath を設定します。
このセットアップは、次節のロギングでも使用します。

```
$ minikube start --memory='4g' --cpus='4'
$ minikube addons disable storage-provisioner
$ minikube addons disable default-storageclass
$ minikube addons list
$ minikube addons enable ingress
$ minikube addons enable csi-hostpath-driver
$ kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
$ kubectl get sc
```

上記のコマンドを列挙したシェルを実行すると、簡単にセットアップできます
```
$ ./start_minikube.sh
```



## Lokiのインストール

モニタリング用のネームスペースを作成
```
$ kubectl create ns monitoring
```

プロメテウスとグラファナのインストール
```
$ helm install -n monitoring prometheus prometheus-community/prometheus
$ helm install -n monitoring grafana grafana/grafana
```


ロキのインストール
```
$ helm install -n monitoring --values values.yaml loki grafana/loki-stack 
```

ポッドが起動して稼働状態になるまで待ちます。
```
$ kubectl get po -n monitoring 
NAME                                                READY   STATUS    RESTARTS   AGE
grafana-7546ccbd55-g2d4x                            1/1     Running   0          59s
loki-0                                              0/1     Running   0          36s
loki-promtail-nrfcr                                 1/1     Running   0          36s
prometheus-alertmanager-0                           1/1     Running   0          70s
prometheus-kube-state-metrics-59b77b956c-gd58g      1/1     Running   0          70s
prometheus-prometheus-node-exporter-jb5rz           1/1     Running   0          70s
prometheus-prometheus-pushgateway-66fc55f8d-qfmpf   1/1     Running   0          70s
prometheus-server-5bf8847f65-42sxt                  2/2     Running   0          70s
```

## グラファナへのログイン
グラファナにログインするためのパスワードを取得します。
```
$ kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

グラファナのポッド名を取得して、ポートフォワードします。
```
$ export POD_NAME=$(kubectl get pods -n monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}");echo $POD_NAME
$ kubectl -n monitoring port-forward $POD_NAME 3000
```



## データソースの追加

Data sourcesの画面から、データソースの追加を選んで、
Lokiをクリックして、Connectionに次のURLをセットする

http://loki.monitoring.svc.cluster.local:3100

画面下の「Save & test」のボタンをクリック





## 監視対象のアプリケーションのインストール
ネームスペース `my-apps` を作成して、アプリケーションをデプロイします。

```
$ kubectl create ns my-apps
$ kubectl apply -n my-apps -f ../../4-8_Network/2_LoadBalancer/deployment.yaml 
$ kubectl apply -n my-apps -f ../../4-8_Network/2_LoadBalancer/service-lb.yaml 
$ kubectl get -n my-apps pod
$ kubectl get -n my-apps svc
$ minikube tunnel
```


## ログの検索
Kubernetesのコントロールプレーンで発生したログを表示してみる。

1. メニューアイコン（通称ハンバーガーアイコン）からExploreを選択
2. 画面上部に、Outlineの横に「prometheus」の選択ウィンドを、「Loki」へ変更
3. 「Enter a Loki query (run with Shift+Enter)」と表示されたフィールドの上部のボタン「Label browser」をクリック
4. 「2. Find values for the selected labels」の 「app」で「my-pod」を選択、「namespace」で「my-apps」を選択
5. ボタン「Show logs」をクリックして、ログを取得

### ログを出力
ログを出力するために、以下のURLをアクセスして、アクセスログを生成しておく
- http://localhost:9100/info
- http://localhost:9100/ping
- http://localhost:9100/


### ログの検索式の作成
メニューアイコン（通称ハンバーガーアイコン）からExploreを選択
「Enter a Loki query (run with Shift+Enter)」と表示されたフィールドに、ログの検索式をインプットする

1. {app="my-pod",namespace="my-apps"}
2. {app="my-pod",namespace="my-apps"}| json 
3. {app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` 
4. {app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` | decolorize | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> -`
5. {app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` | decolorize | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> -` | - line_format `{{.method}}` |~ `[A-Z]+`
6. {app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` | decolorize | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> -` | line_format `{{.method}}` |~ `[A-Z]+`| line_format "{{.status}}"

7. count_over_time({app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` | decolorize | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> -` | line_format `{{.method}}` |~ `[A-Z]+`| line_format "{{.status}}" [$__auto])
  Options Type = Instant

8. sum by (status) (count_over_time({app="my-pod", namespace="my-apps"} | json | line_format `{{.log}}` | decolorize | pattern `<ip> - - [<_>] "<method> <uri> <_>" <status> -` | line_format `{{.method}}` |~ `[A-Z]+`| line_format "{{.status}}" [$__auto]))
  Legend = {{status}}
  Options Type = Instant



## ダッシュボードの作成
1. ログをリストする

- 上記から３番目の検索式を、Exploreで表示される検索式インプットフィールドへセット
- カラー表示のエスケープ文字列を削除するために、「| decolorize」を追加
- 「Add」の「Add to dashboard」を選択
- 「New dashboard」を選択して、ボタン「Open dashboard」をクリック
- パネルの右上隅のマウスカーソルと合わせると表示されるメニューから、Editを選択
- パネルのタイトルなど、お好みにカスタマイズする
- 画面右上の「Save」で設定の保存、「Apply」で設定の適用
- 上記のEdit選択から「Apply」で画面を確認する作業を繰り返し
- 「Save」のクリックで表示されたウィンドにダッシュボード名を設定して、ウィンドの「Save」をクリックして変更を確定 
- ≡ → Dashboardsを選択して、上記で保存したDashboardが表示されることを確認


2. HTTP status をグラフにする
- ≡ → Explore　で、８番の検索式を入力
- Options をクリックして、 Legend = {{status}}、 Options Type = Instant　をセット
- 「Add」の「Add to dashboard」を選択
- 以下は上記と同じ



## クリーンナップ
```
$ minikube delete
```


## 参考資料
- Lokiインストール、https://grafana.com/docs/loki/latest/setup/install/helm/install-monolithic/
- ログの検索、https://grafana.com/docs/grafana/latest/explore/logs-integration/
- ログの検索式、https://grafana.com/docs/loki/latest/query/log_queries/
