# 特権モードを使わないNginx
docker build -t sec-nginx:1.0 .


## ローカルでの実行
docker run -d --publish 9600:9200 --name snginx sec-nginx:1.0

## コンテナへ入る
docker exec -it snginx sh 


## イメージをレジストリへ登録

export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID 
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag sec-nginx:1.0 ghcr.io/takara9/sec-nginx:1.0
docker push ghcr.io/takara9/sec-nginx:1.0


## clean up
docker stop snginx
docker rm snginx
docker rmi sec-nginx:1.0
