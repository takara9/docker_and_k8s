# 永続的データの読み書き


## バインドマウントの使用例 フィボナッチの数列を表示

バインドマウントでパソコンのフォルダーのプログラムを実行
```
$ docker run -it -v ${PWD}/src:/mnt python:latest python3 /mnt/fibo.py
```


## 永続ボリュームの作成

ボリュームを作成
```
$ docker volume ls
$ docker volume create my-vol
```

作成したボリュームの情報表示
```
$ docker volume inspect my-vol
```


## 永続ボリュームをマウントしたコンテナを起動

永続ボリュームをマウントしたコンテナを起動
```
$ docker run -it --name voltest --mount source=my-vol,target=/app ubuntu
# df
```

マウントしたコンテナへ何かデータを書き込み
```
# ps -ax > /app/data.txt
# cat /app/data.txt
```

コンテナを止めて削除
```
$ docker kill voltest
$ docker rm voltest
```

再び、新しいコンテナで、my-volをマウントして保存したデータを確認
```
$ docker run -it --name voltest2 --mount source=my-vol,target=/app ubuntu
# df
# cd /app/
# ls -al
# cat data.txt
```


## tmpfsをマウントしたコンテナの起動

一時ボリュームをマウントしたコンテナを起動して書き込み、exitでコンテナを停止
```
$ docker run -it --name tmptest --tmpfs /app ubuntu
# df -h
# dd if=/dev/urandom of=/app/test.dat bs=80 count=10
# df -h
# ls -al /app
# exit
```

コンテナを再びスタート
```
$ docker ps -a
$ docker start tmptest
```

コンテナにデータが存在するか確認
```
$ docker exec -it tmptest bash
# df -h
# ls -al /app
# exit
```


## Docker Desktopを使ったバックアップ

ボリュームを作成して、データを書き込み
```
$ docker volume create my-vol
$ docker run -it –rm --name voltest --mount source=my-vol,target=/app ubuntu:latest
# ls -lR / > /app/ls-lR.txt
# df -h
# sha1sum /app/ls-lR.txt > /app/check.txt
# exit
```
Docker Desktopからデータのバックアップファイルを作成


## Docker Desktopによるリストア

リストアの確認のため、コンテナとボリュームを削除
```
$ docker ps -a
$ docker rm コンテナID
$ docker volume ls
$ docker volume rm my-vol
```
Docker Desktopを使って、データをリストア


リストアしたデータをハッシュでチェック
```
$ docker run -it --name voltest --mount source=my-vol,target=/app ubuntu
# sha1sum -c /app/check.txt
```


## Docker コマンドを利用したバックアップとリストア

ボリュームのデータをパソコン上のtarファイルにバックアップ
```
$ docker run --rm --mount source=my-vol,target=/backup-volume \
  -v $(PWD):/backup \
  busybox tar -zcvf /backup/my-vol.tar.gz /backup-volume
```


ボリュームを削除、再作成して、リストア、ハッシュでチェック
```
$ docker volume rm my-vol
$ docker volume create my-vol
$ docker run --rm --mount source=my-vol,target=/backup-volume \
   -v "$(pwd)":/backup \
   busybox tar -zxvf /backup/my-vol.tar.gz --strip-components 1 -C /backup-volume

$ docker run -it --rm --name voltest --mount source=my-vol,target=/app ubuntu
# sha1sum -c /app/check.txt
```


## コンテナにデータの保存はNG

```
$ docker run -it ubuntu
# df -h
```


## コマンドでコンテナの重ね合わせ構造を見る

イメージのレイヤー履歴を確認
```
$ docker history ubuntu:latest
```

起動したイメージにパッケージを追加
```
$ docker run -it --name ubuntu-add ubuntu:latest 
# apt update -y
# apt install iputils-ping -y
# exit
```

レイヤーの追加を確認
```
$ docker commit ubuntu-add my-ubuntu:0.3
$ docker history my-ubuntu:0.3
```


## 参考リンク
- 日本語 dockerコマンド https://docs.docker.jp/engine/reference/commandline/#id6
- dockerコマンドリファレンス https://docs.docker.com/reference/cli/docker/volume/
