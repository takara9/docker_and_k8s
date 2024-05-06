# syntax=docker/dockerfile:1
FROM ubuntu:22.04

# モジュールをインストール
RUN apt-get update && apt-get install -y python3 python3-pip iputils-ping dnsutils curl iproute2 zip unzip groff
RUN curl -LJO https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
RUN mv yq_linux_amd64 /usr/local/bin/yq
RUN chmod a+x /usr/local/bin/yq
RUN ARCH=`arch` && curl "https://awscli.amazonaws.com/awscli-exe-linux-$ARCH.zip" -o "awscliv2.zip" 
RUN unzip awscliv2.zip && ./aws/install && rm /awscliv2.zip && rm -fr /aws
WORKDIR /
USER 65534:65534

# コンテナの停止防止
CMD ["tail", "-f", "/dev/null"]