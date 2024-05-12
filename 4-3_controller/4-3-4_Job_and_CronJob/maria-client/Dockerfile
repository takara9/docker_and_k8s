# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# モジュールをインストール
RUN apt-get update && apt-get install -y mariadb-client mariadb-backup curl iproute2 zip unzip groff
RUN curl -LJO https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
RUN ARCH=`arch` && curl "https://awscli.amazonaws.com/awscli-exe-linux-$ARCH.zip" -o "awscliv2.zip" 
RUN unzip awscliv2.zip && ./aws/install && rm /awscliv2.zip && rm -fr /aws
WORKDIR /
USER 65534:65534

