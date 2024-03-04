FROM eclipse-temurin:latest

# アプリケーションのインストール
RUN mkdir /app
WORKDIR /app
COPY --chown=65534:65534 target/rest-service-0.0.1.jar /app/rest-service.jar

# コンテナの設定
USER 65534:65534
EXPOSE 8080
CMD ["java", "-jar", "/app/rest-service.jar"]
