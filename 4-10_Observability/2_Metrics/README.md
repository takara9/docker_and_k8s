# メトリックス監視

CPUとメモリの使用率、ディスクへの書き込みと読み取りの速度など、数値化されるデータを収集して、視覚化します。
定番のGrafanaとPrometheousを使用した例を紹介します。


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


## 時系列データベースのプロメテウスをインストール
プロメテウスをHelmを使用してインストールします。Helmのインストールは参考資料を参照してインストールしてください。

```
$ kubectl create ns monitoring
```

リポジトリの追加（初回のみ）
```
$ helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
$ helm repo update
```

プロメテウスのインストール
```
$ helm install -n monitoring prometheus prometheus-community/prometheus
```

## 視覚化ツールのグラファナのインストール
こちらも、Helmを使用してインストールします。

リポジトリの追加（初回のみ）
```
$ helm repo add grafana https://grafana.github.io/helm-charts
$ helm repo update
```

グラファナのインストール
```
$ helm install -n monitoring grafana grafana/grafana
```


## グラファナへのアクセス
グラファナのポッドが、すべて Running になるまで待ちます。
```
$ kubectl get po -n monitoring
NAME                                                READY   STATUS    RESTARTS   AGE
grafana-58497f6f96-cxdw6                            1/1     Running   0          38s
prometheus-alertmanager-0                           1/1     Running   0          49s
prometheus-kube-state-metrics-f7c68b84f-szb5s       1/1     Running   0          49s
prometheus-prometheus-node-exporter-fs9f6           1/1     Running   0          49s
prometheus-prometheus-pushgateway-568fbf799-pld7f   1/1     Running   0          49s
prometheus-server-6949d6cfdd-npxlr                  2/2     Running   0          49s
```

グラファナにログインするためのパスワードを取得します。
```
$ kubectl get secret -n monitoring grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

グラファナのポッド名を取得して、ポートフォワードします。
```
$ export POD_NAME=$(kubectl get pods -n monitoring -l "app.kubernetes.io/name=grafana,app.kubernetes.io/instance=grafana" -o jsonpath="{.items[0].metadata.name}")
$ echo $POD_NAME
$ kubectl -n monitoring port-forward $POD_NAME 3000
```

## Grafanaのセットアップ

### データソースの設定
ブラウザから以下のURLをアクセスします。

http://localhost:3000/


以下の認証情報で、グラファナへログインします。
  ユーザー: admin
  パスワード: 上記シークレットから取得した値


データソースにPrometheusの選択します<p>

<img src="image/add-data-source.png" width="500">


PrometheusデータベースのURLアドレス 'http://prometheus-server' をインプットします。
<p>
<img src="image/add-data-source-pro.png" width="500">

それ以外はデフォルトのままで、「Save & test」をクリックします。



### 作成済みダッシュボードの設定
Dashboads -> Newボタン　-> import
Grafana.com dashboard URL or ID のフィールドに 1860 をインプットします。

<img src="image/node.png" width="500">

データソースのプロメテウスを選択します。


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

ブラウザから、次のアドレスをアクセスすることで、負荷を与えることができます。
`http://localhost:9100/info`


## myーapps　のダッシュボード作成
上記でデプロイしたアプリケーションのダッシュボードを作ります。
- メニューから、Explore を選択
- 右端の「Builder｜Code」の 「Code」を選択
- 「Mertics browser >」をクリック
- 「1. Select a metric」の入力フィールドで、入力候補「cpu_usage」をインプット
- 下に表示されたメトリックス「container_cpu_usage_seconds_total」をクリックして使用を決定
- 「2. Select labels to search in」の下に選択候補が上がっているが、何もしないで、次へ進む
- 「3. Select (multiple) values for your labels」の下に挙がった namespaceのリストから「my-apps」選択
- 「4. Resulting selector」に表示式の候補が表示されるので、ボタン「Use query」の隣の「Use as rate query」をクリック
- 点と点が線で繋がらないグラフがプロットされた状態になっている、そこで、「Builder｜Code」の 「Builder」を選択
- 「Rate」の選択ウィンド Rangeに表示された「$_rate_interval」から「5m」に変更
- 画面右上の「Run query」をクリックすると再描画されて、線と点が繋がるグラフになる
- 「Builder｜Code」の「Code」を選択、グラフ式下の「Options」をクリック
- 「Legend」の選択フィールドが「Auto」になっているので、「Custom」へ変更
- 「{{label_name}}」を「{{pod}}」へ変更、画面右上の「Run query」をクリック
- 画面上方の「Add to dashboard」をクリック
- 「Target dashboard」に「New dashboard」を選択して、「Open Dashboard」をクリック
- 画面上方のマウスカーソルと合わせると save dashboard が表示されるフロッピーディスクのアイコンをクリック
- タイトル名をインプットして、ボタン「Save」をクリック
- パネル右上角のメニューから、「Edit」を選択して、表示のカスタマイズができる
- 画面右上の「Apply」は変更確認、「Save」は変更内容の保存
- お好みの表示に仕上げて、完了


## ダッシュボードをパソコンのファイルとして保存
- ハンバーガーメニューから「Dashboard」を選択
- ブラウザ画面上部で、歯車アイコン(Dashboard setting)をクリック
- 「JSON Model」のタブをクリック
- 表示されたJSON形式の設定を、パソコンのファイルへコピペする。


## 保存したダッシュボードのファイルを適用するには
- ハンバーガーメニューから「Dashboard」を選択
- ブラウザ画面右上のボタン「New」をクリック、Importを選択
- 「Upload dashboard JSON file」のエリアに、保存しておいたJSONファイルをドラッグ＆ドロップ
- または「Import via dashboard JSON model」に、JSON形式の設定をコピペする。



## クリーンナップ
```
$ minikube delete
```


## 参考資料

- Helmコマンドのインストール、https://helm.sh/docs/intro/install/
- プロメテウスのインストール、https://github.com/prometheus-community/helm-charts
- プロメテウスHP、https://prometheus.io/
- グラファナのインストール、https://grafana.com/docs/grafana/latest/setup-grafana/installation/helm/
- グラファナHP、https://grafana.com/
- グラファナダッシュボードのカタログ、https://grafana.com/grafana/dashboards/

