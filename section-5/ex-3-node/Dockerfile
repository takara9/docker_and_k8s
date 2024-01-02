FROM node:21.5.0-slim

# アプリケーションのインストール
ENV NODE_ENV production
WORKDIR /app
COPY --chown=1000:1000 app.js .

# 依存するモジュールをインストール
RUN npm install express

# コンテナの設定
USER 1000:1000
EXPOSE 3000
CMD ["node", "app.js"]