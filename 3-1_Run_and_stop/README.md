# Commands

## Hallo worldの表示

docker run --name hw hello-world

## クリーンナップ
docker rm hw
docker rmi hello-world:latest


## イメージの取得
docker pull ghcr.io/takara9/my-ubuntu:0.2 <-- 不要ではないか

## 対話型コンテナの実行
docker run -it --name mu ghcr.io/takara9/my-ubuntu:0.2
exit


## クリーンナップ
docker rm mu
docker rmi ghcr.io/takara9/my-ubuntu:0.2