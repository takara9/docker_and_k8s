## イメージのビルド

シングルステージか、マルチステージかは、択一です。
シングルステージは開発やデバッグ用、マルチステージは統合テストや本番用と見なすことができます。

  * マルチステージビルド
  docker build -t ex4:1.0 .

  * シングルステージビルド
   docker build -t ex4:1.0 -f Dockerfile.singlestage .

### イメージの実行
docker run --name ex4 -d -p 9400:8086 ex4:1.0


## アクセス

curl http://localhost:9400/ping;echo


## コンテナへ入る

シングルステージの場合
docker exec -it ex4 bash

注意、マルチステージで作られたイメージのコンテナにはログインできません。


## クリーンナップ

docker stop ex4
docker rm ex4
docker rmi ex4:1.0

