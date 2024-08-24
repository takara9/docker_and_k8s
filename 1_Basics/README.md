# Docker と Kubernetes の基本 



## Docker 
- Dockerホームページ https://www.docker.com/
- Docker 日本語リファレンス https://matsuand.github.io/docs.docker.jp.onthefly/reference/
- Docker ドキュメント https://docs.docker.com/
- Docker ドキュメント日本語化プロジェクト https://docs.docker.jp/
- docker コマンドリファレンス https://docs.docker.com/reference/cli/docker/
- Dockerfile リファレンス https://docs.docker.com/reference/dockerfile/
- Dockerエンジン https://docs.docker.com/engine/

## レジストリサービス
- Docker Hub コンテナレジストリー https://hub.docker.com/
- Amazon Elastic Container Registry https://aws.amazon.com/ecr/
- Google Artifact Registry https://cloud.google.com/artifact-registry/docs
- GitHub packages https://github.co.jp/features/packages


### Dockerの歴史、基礎技術
- Docker の歴史 https://en.wikipedia.org/wiki/Docker_(software)#History
- OSレベル仮想化 https://en.wikipedia.org/wiki/OS-level_virtualization
- UnionFS ユニオンファイルシステム https://ja.wikipedia.org/wiki/UnionFS
- OverlayFS ストレージ ドライバー https://docs.docker.com/engine/storage/drivers/overlayfs-driver/
- DockerのBuild,Share,Run https://www.docker.com/resources/what-container/
- Dockerビルドの概要 https://docs.docker.com/build/
- Docker ガイド https://docs.docker.com/guides/
- Docker マニュアル　https://docs.docker.com/manuals/
- Docker リファレンス ドキュメント https://docs.docker.com/reference/


### OSSの現状
- Linux Foundation アニュアルレポート日本語版2023 https://www.linuxfoundation.jp/publications/2024/01/linux-foundation-annual-report-2023-jp/
- GitHub OSSの現状 2023 https://github.blog/news-insights/research/the-state-of-open-source-and-ai/


### セキュリティ
- CVEの目的と定義 https://www.csoonline.com/article/562175/what-is-cve-its-definition-and-purpose.html
- 共通脆弱性識別子CVE概説 https://www.ipa.go.jp/security/vuln/scap/cve.html
- 共通脆弱性評価システムCVSS概説 https://www.ipa.go.jp/security/vuln/scap/cvss.html
- 共通脆弱性タイプ一覧CWE概説 https://www.ipa.go.jp/security/vuln/scap/cwe.html

- 米国CERTコーディネーションセンター https://www.kb.cert.org/vuls/
- JPCERTコーディネーションセンター https://www.jpcert.or.jp/
- NVD 米国 国立脆弱性データベース https://nvd.nist.gov/
- JVN 日本国 脆弱性対策データベース https://jvndb.jvn.jp/apis/myjvn/

- コンテナセキュリティに関するよくある質問 https://docs.docker.com/security/faqs/containers/
- 一般的なセキュリティに関する質問 https://docs.docker.com/security/faqs/general/
- Dockerコンテナのセキュリティ https://docs.docker.com/engine/security/


### Linuxディストリビューション パッケージの脆弱性
- alpine linux Security Issue Tracker https://security.alpinelinux.org/
- debian linux Security Bug Tracker https://security-tracker.debian.org/tracker/
- Red Hat セキュリティーアドバイザリー https://access.redhat.com/security/security-updates/
- Ubuntu Security Notices https://ubuntu.com/security/notices
- SUSE linux Update Advisories https://www.suse.com/support/update/


### コンテナイメージ作成のベストプラクティス
- Dockerfile Best Practices https://github.com/dnaprawa/dockerfile-best-practices
- Dockerfile Best Practices 入門ガイド https://www.docker.com/blog/intro-guide-to-dockerfile-best-practices/
- Dockerコンテナ内でsshdを実行してはいけない理由 https://postd.cc/docker-ssh-considered-evil/
- Docker ビルドのベストプラクティス https://docs.docker.com/build/building/best-practices/
- なぜコンテナにSSHログが無いのですか？ https://www.reddit.com/r/docker/comments/10ob337/why_does_docker_container_doesnt_have_ssh_log/


## マイクロサービスとコンテナ 
- コンテナはマイクロサービス専用か？ https://www.docker.com/blog/are-containers-only-for-microservices-myth-debunked/
- マイクロサービス　https://martinfowler.com/articles/microservices.html
- マイクロサービスとコンテナ: アプリケーション アーキテクチャの現代的な解釈 https://laerciosantanna.medium.com/microservices-and-containers-a-modern-take-on-application-architecture-2ca97bdd0699



## Kubernetes の基本コンセプト
- Kubernetesプロジェクトホームページ https://kubernetes.io/
- コンセプト https://kubernetes.io/docs/concepts/
- Kubernetes とは何か? 開発者として知っておくべきこと https://medium.com/@rphilogene/what-is-kubernetes-what-you-need-to-know-as-a-developer-674af25e3947
- Kubernetesの概要 https://kubernetes.io/docs/concepts/overview/
- チュートリアル　https://kubernetes.io/docs/tutorials/
- クラウドネイティブ ランドスケープ https://landscape.cncf.io/

## Kuberntesの歴史
- Kubernetesの10年間の歴史 https://kubernetes.io/ja/blog/2024/06/06/10-years-of-kubernetes/
- Kubernetesの歴史 https://ja.wikipedia.org/wiki/Kubernetes#%E6%AD%B4%E5%8F%B2
- TechCrunch: Kubernetes が 1.0 に到達、Google は新たに設立された Cloud Native Computing Foundation に技術を寄付 https://www.cncf.io/news/2015/07/21/techcrunch-as-kubernetes-hits-1-0-google-donates-technology-to-newly-formed-cloud-native-computing-foundation/

## Kubernetesのアーキテクチャー
- Kubernetesのアーキテクチャー https://kubernetes.io/docs/concepts/architecture/
- Kubernetesコンポーネント https://kubernetes.io/docs/concepts/overview/components/


## Kubernetesに必要だけど含まれないもの
- Kubernetes インフラストラクチャとは https://www.vmware.com/topics/kubernetes-infrastructure
- 

### クラウドのKubernetesサービス
- Google Kubernetes Engine（GKE）https://cloud.google.com/kubernetes-engine?hl=ja
- Amazon Elastic Kubernetes Service (EKS) https://aws.amazon.com/jp/eks/
- Azure Kubernetes Service (AKS) https://azure.microsoft.com/ja-jp/products/kubernetes-service
- IBM Cloud Kubernetes Service https://www.ibm.com/products/kubernetes-service


### オンプレミスのKubernetes製品
- VMware Tanzu Kubernetes クラスタ https://docs.vmware.com/jp/VMware-vSphere/7.0/vmware-vsphere-with-tanzu/GUID-DC22EA6A-E086-4CFE-A7DA-2654891F5A12.html
- Red Hat OpenShift https://www.redhat.com/ja/explore/openshift
- SUSE テクニカル リファレンス ドキュメント: コンテナ管理 https://documentation.suse.com/ja-jp/trd/kubernetes/
- Ubuntu linux kubernetes https://jp.ubuntu.com/kubernetes


## Kubernetesのリソースとオブジェクト
- Kubernetes のオブジェクト https://kubernetes.io/docs/concepts/overview/working-with-objects/
- Kubernetes APIのコンセプト https://kubernetes.io/docs/reference/using-api/api-concepts/
- Kubernetes API https://kubernetes.io/docs/reference/kubernetes-api/



