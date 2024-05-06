# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# 依存するモジュールをインストール
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install flask mysql-connector-python

# アプリケーションのインストール
RUN mkdir /app
WORKDIR /app

USER 1000:1000
COPY --chown=1000:1000 app.py /app/app.py
COPY --chown=1000:1000 app.log /app/app.log

# コンテナの設定
ENV FLASK_APP=app
EXPOSE 9100
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9100"]


