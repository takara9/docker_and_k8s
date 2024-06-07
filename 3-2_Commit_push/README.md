
## ubuntuのコンテナを起動　（ターミナルで実行）
docker run -it --name my-ubuntu ubuntu:22.04

## 近くのルーターにpingを実行　（コンテナで実行）
ping 192.168.1.1

## コンテナへpingコマンドをインストール　（コンテナで実行）
apt-get update -y
apt-get install iputils-ping
exit

## コマンドを追加したコンテナを、イメージとして保存 （別ターミナルで実行）
docker commit my-ubuntu my-ubuntu:0.2

## 動作確認 （別ターミナルで実行）
docker run -it --name my-ubuntu2 my-ubuntu:0.2
ping 192.168.1.1
exit

## レジストリへアップロード
docker tag my-ubuntu:0.2 ghcr.io/takara9/my-ubuntu:0.2
docker images
export USERNAME=YOUR_USER_ID
export CR_PAT=YOUR_TOKEN
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker push ghcr.io/takara9/my-ubuntu:0.2


## クリーンナップ
docker stop my-ubuntu2 
docker rm my-ubuntu2
docker rm my-ubuntu
docker rmi my-ubuntu:0.2
docker rmi ghcr.io/takara9/my-ubuntu:0.2
docker rmi ubuntu:22.04


docker run -it ghcr.io/takara9/my-ubuntu:0.2