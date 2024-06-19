## イメージのビルド
ghcr.ioに登録されたコンテナを利用するのであれば不要です。

```
docker build -t probe:1.0 .
```

## イメージをレジストリへ登録
ghcr.ioに登録されたコンテナを利用するのであれば不要です。

```
export CR_PAT=(YOUR_TOKEN)
export USERID=(YOUR USERID)
export REGISTRY=ghcr.io  # (YOUR_REGISTRY)
export TAG=1.0
export REPOSITORY=probe:${TAG}
echo $CR_PAT | docker login ghcr.io -u ${USERID} --password-stdin
docker tag ${REPOSITORY} $REGISTRY/$USERID/$REPOSITORY
docker push ${REGISTRY}/${USERID}/${REPOSITORY}
```



## コンテナ単体のテスト
```
docker run -d --name webservice --rm -p 9000:9000 probe:1.0 
```

コンテナのアプリケーションの死活監視
curl -v http://127.0.0.1:9000/healthz
  正常 HTTP STATUS = 200
  異常 HTTP STATUS = 500

コンテナのアプリケーションの準備状態
curl -v http://127.0.0.1:9000/readiness
  準備完了 HTTP STATUS = 200
  準備中   HTTP STATUS = 500

ライブネスプローブの状態変更
　curl -v http://127.0.0.1:9000/fail
  正常 -> 異常

レディネスプローブの状態変更
　curl -v http://127.0.0.1:9000/be_ready
  準備中 -> 準備完了





