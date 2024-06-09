# カスタムコントローラー

図解と用語の解説

CR
CRD
Hook
  Validator
  Defaulter
RBAC

開発する時のツールのリンクまで



## 参考資料
- https://kubernetes.io/docs/concepts/extend-kubernetes/operator/
オペレーター パターンは、Kubernetes 自体が提供するものを超えてタスクを自動化するコードを記述する方法を示します。

- https://book.kubebuilder.io/getting-started
カスタム リソース (CR) とカスタム リソース定義 (CRD) を作成
Kubebuilder ツールを活用することで、これらのプラットフォームのソリューションを表す API とオブジェクトを定義できます。 



the Custom Resource (CR) and Custom Resource Definition (CRD) for the Memcached Kind.

It creates the API with the group cache.example.com and version v1alpha1, uniquely identifying the new CRD of the Memcached Kind






# RBAC　ロール・ベース・アクセス・コントロール

コントローラーのポッドが、kube-apiserverにアクセスして、オブジェクトを作成や削除などの操作をしたいケースでは、APIをアクセスする特権が必要となる。RBACは、役割を設けて、役割に対して、特権を与える役割別のアクセス制御を採用している。運用の自動化や省力化を推進するカスタムコントローラーやオペレーターは、RBACを使った特権付与がなければ、K8sクラスタのAPIを操作できない。

## RBACの　APIの種類
- ClusterRole
- Role
- ClusterRoleBinding
- RoleBinding

