# DockerとKubernetes入門

## macOSのターミナルのシェル変更

シェルは、bash で記述しています。そのため、macOSでは、以下のコマンドで切り替えて、ターミナルを再起動する必要があります。

```
% chsh -s /bin/bash
```




## コンテナが起動できない時のトラブルシューティング

docker ps -a して、名前が同じコンテナが存在しないか、確認してください。
コンテナが存在したら、docker rm [コンテナ名 または　コンテナID] で削除してください。




## その他のメモ

docker-entrypoint.sh
dockeriginore が欲しい。


## サブモジュールの組み込み方法
以下のコンテナをビルドするためのリポジトリは、サブモジュールとして、以下のコマンを使って、3-5_app_development 以下のディレクトリへ組み込んでいます。

```
cd 3-5_app_development
git submodule add https://github.com/takara9/ex1 3-5-1-python
git submodule add https://github.com/takara9/ex2 3-5-2-php
git submodule add https://github.com/takara9/ex3 3-5-3-node
git submodule add https://github.com/takara9/ex4 3-5-4-golang
git submodule add https://github.com/takara9/ex5 3-5-5-java
```

## サブモジュールを含めてクローンする方法
サブモジュールをクローンするには、以下のオプションが必要です。

```
git clone --recursive　https://github.com/takara9/docker_and_k8s.git
```

一度、クローンした後に、サブモジュールを取り込むには、以下の手順を実行します。

```
git clone https://github.com/takara9/docker_and_k8s.git
git submodule update --init --recursive
```

## フォークして変更してプッシュ
