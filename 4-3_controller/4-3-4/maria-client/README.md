# ビルド
```
docker build -t mariadb-client:1.0 .
```

## コンテナへ入る
```
docker run -it --rm mariadb-client:1.0 bash
```

## イメージをレジストリへ登録

### GHCR
```
export CR_PAT=YOUR_TOKEN
export USERNAME=YOUR USERID
echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
docker tag mariadb-client:1.0 ghcr.io/takara9/mariadb-client:1.0
docker push ghcr.io/takara9/mariadb-client:1.0
```

### DockerHub
```
docker login
docker tag mariadb-client:1.0 maho/mariadb-client:1.0
docker push maho/mariadb-client:1.0
```


## 使用法（どちらかを選択）
- docker run -it mariadb-client:1.0 bash
- docker run -it ghcr.io/takara9/mariadb-client:1.0 bash
- docker run -it maho/mariadb-client:1.0 bash
- kubectl run -it mypod --rm --image maho/mariadb-client:1.0 -- bash



