# DockerとKubernetes入門


## macOSのターミナルのシェル変更

シェルは、bash で記述しています。そのため、macOSでは、以下のコマンドで切り替えて、ターミナルを再起動する必要があります。

```
% chsh -s /bin/bash
```


## コンテナが起動できない時のトラブルシューティング

docker ps -a して、名前が同じコンテナが存在しないか、確認してください。
コンテナが存在したら、docker rm [コンテナ名 または　コンテナID] で削除してください。




その他のメモ

docker-entrypoint.sh
dockeriginore が欲しい。




追加できたら良いかな
4.6. 集中監視　オブザーbアビリティー
4.7. CI/CD + ArgoCD

