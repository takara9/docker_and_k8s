# ビルド
```
docker build -t my-ubuntu:0.3 .
```

## コンテナへ入る
```
docker exec -it my-ubuntu:0.3 bash
```

## イメージをレジストリへ登録

### GHCR
```
export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag my-ubuntu:0.3 ghcr.io/takara9/my-ubuntu:0.3
docker push ghcr.io/takara9/my-ubuntu:0.3
```

### DockerHub
```
docker login
docker tag my-ubuntu:0.3 maho/my-ubuntu:0.3
docker push maho/my-ubuntu:0.3
```


## 使用法（どちらかを選択）
- docker run -it my-ubuntu:0.3 bash
- docker run -it ghcr.io/takara9/my-ubuntu:0.3 bash
- docker run -it maho/my-ubuntu:0.3 bash
- kubectl run -it mypod --rm --image maho/my-ubuntu:0.3 -- bash



