# デプロイメントとステートフルセット




apiVersion: apps/v1
kind: StatefulSet # (1)ステートフルセット
metadata:
  name: dbn       # (2)名前
spec:             # (3)ステートフルセットの仕様
  minReadySeconds: 0  # (4)ポッドが使用可能で見なす最小時間
  persistentVolumeClaimRetentionPolicy: # (5)永続ボリュームの取り扱い設定
    whenDeleted: Retain  # StatefulSet が削除されたときに永続ボリュームを保持
    whenScaled: Retain   # StatefulSet がスケールダウンされたときに永続ボリュームを保持
  podManagementPolicy: OrderedReady　# (6)初期、入れ替え、スケールダウンの時にポッド操作順を設定
  replicas: 3 # (4)下記テンプレートのポッド起動数
  revisionHistoryLimit: 10 # (5)履歴に保持されるリビジョンの最大数
  selector: # (6)下記テンプレートで起動するポッドに対するラベルのクエリ
    matchLabels:
      app: dbn
  serviceName: dbx　# (7)下記テンプレートで起動するポッドにDNS名の取得 
  template:
　　　<ポッドの雛形>
  updateStrategy: # (8)Podを更新方法を決める
    type: RollingUpdate
    rollingUpdate:
      partition: 0
　volumeClaimTemplates: # (9)ポッドからマウント可能な永続ボリューム要求のテンプレート
　　　<永続ボリュームの雛形>
