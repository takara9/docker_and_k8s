# コントローラーの役割

Kubernetes のコントローラーとは、繰り返し状態を監視して、新たな要求や障害などで状態が変化すると、目的とする状態を維持する働きをします。例えば、大量のクライアントからのリクエストに応答するため Pod 数が 5 に定められた状態で、ハードウェアの障害で Pod 数が 3 に減少した場合、目標とする 5 へ回復するるために、新たな 2つの Pod を起動します。状態監視と対応実行の繰り返しを制御ループ (controll loop / reconcile loop) と呼ばれます。これは宣言的なAPIを実現する基礎になっています。

Kubernetesには、用途に合わせたコントローラーが複数あります。また、自作のコントローラーを開発して Kubernetes の機能を拡張することができます。そのようなコントローラーはカスタムコントローラー、これを使用するためのAPIをカスタムリソースと呼ばれます。カスタムコントローラーについては、後述の章で紹介しましす。

コントローラーは、そのAPIをYAMLで記述したファイル を Kubernetes クラスタへ適用して、オブジェクトとして使用します。

Kubernetes クラスタで 使用可能なリソースをリストするには　`kubectl api-resources` で参照できます。この中でコントローラーのオブジェクトにできる代表的なリソースを次に紹介します。　リソース名は複数形で表され、APIの種別を表す KIND は、単数形になっています。次のリソースは、KIND名で記載します。


## 組み込み済みコントローラーの概要


- Deployment は、目的とするコンテナのポッドを展開するコントローラーです。内部で ReclicaSet と連携して、ポッド数を制御します。アプリケーションのサービス提供を維持しながら、Pod をアップデートする機能を提供します。 https://kubernetes.io/docs/concepts/workloads/controllers/deployment/

- ReplicaSet は、定められた Pod の数を維持するコントローラーです。Pod が予期しない障害などの理由で喪失した場合、定められた目標の Pod 数まで代替 Pod を起動して、定められた数に回復します。Deploymentは、より上位レベルの概念で、他の多くの有益な機能と、宣言的なPodのアップデート機能を提供します。そのため、コンテナのアップデートを必要としない限り、Deploymentを使用するべきです。

- StatefulSet は、永続的なデータを保持するステートフルなアプリケーションの Pod のためのコントローラーです。定められたポッド数を維持するだけでなく、ポッドとボリュームの対応付けを維持して、データの一貫性維持の支援をします。 https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/

- ReplicationController は、次世代版の ReplicaSet で置き換えられます。そのため、Deploymentを使うことが推奨されます。 https://kubernetes.io/docs/concepts/workloads/controllers/replicationcontroller/

- Job は、1 つ以上の Pod を起動して、それら全てが正常に終了するまで Pod の再試行し続けます。Pod が正常終了すると Job は正常完了したと見做して終了します。予期しない障害や不意な削除で、Job の制御下の Pod を喪失すると、新たな Pod を起動して正常に終了するまで管理します。 https://kubernetes.io/docs/concepts/workloads/controllers/job/

- CronJob は、定期的なスケジュールで Job を起動します。ユースケースとして、データのバックアップやバッチ処理などがあります。　https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

- DaemonSet は、Kubernetesクラスタの全てのノードで、Pod のコピーを実行することを保証します。クラスターにノードが追加されると、自動的に DaemonSetの管理する Pod が起動します。反対に、ノードが削除されると、Pod も削除されます。また、DaemonSet のオブジェクト を削除すると、管理対象の Pod が、全ノードから消去されます。 https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/



　



## 参考資料
- https://kubernetes.io/docs/concepts/architecture/controller/
