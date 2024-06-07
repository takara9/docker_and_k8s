# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# 依存するモジュールをインストール
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install flask

# アプリケーションのインストール
RUN mkdir /app
WORKDIR /app

USER 65534:65534
COPY --chown=65534:65534 app.py /app/app.py
COPY --chown=65534:65534 app.log /app/app.log

# コンテナの設定
ENV FLASK_APP=app
EXPOSE 9100
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "9100"]


