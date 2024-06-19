# ポッドのログ表示
ポッド内部のコンテナの標準出力と標準エラー出力の表示方法です。


## 準備
```
$ minikube start
$ kubectl get no
```


## 実行例
起動時にメッセージを表示する Webサーバー nginx　のコンテナを起動
```
$ kubectl run nginx1 --image=nginx:latest
pod/nginx1 created
```

コンテナで出力されたメッセージを表示
```
$ kubectl logs nginx1
/docker-entrypoint.sh: /docker-entrypoint.d/ is not empty, will attempt to perform configuration
/docker-entrypoint.sh: Looking for shell scripts in /docker-entrypoint.d/
/docker-entrypoint.sh: Launching /docker-entrypoint.d/10-listen-on-ipv6-by-default.sh
10-listen-on-ipv6-by-default.sh: info: Getting the checksum of /etc/nginx/conf.d/default.conf
10-listen-on-ipv6-by-default.sh: info: Enabled listen on IPv6 in /etc/nginx/conf.d/default.conf
/docker-entrypoint.sh: Sourcing /docker-entrypoint.d/15-local-resolvers.envsh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/20-envsubst-on-templates.sh
/docker-entrypoint.sh: Launching /docker-entrypoint.d/30-tune-worker-processes.sh
/docker-entrypoint.sh: Configuration complete; ready for start up
2024/03/31 00:16:42 [notice] 1#1: using the "epoll" event method
2024/03/31 00:16:42 [notice] 1#1: nginx/1.25.4
2024/03/31 00:16:42 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2024/03/31 00:16:42 [notice] 1#1: OS: Linux 6.6.12-linuxkit
2024/03/31 00:16:42 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/03/31 00:16:42 [notice] 1#1: start worker processes
2024/03/31 00:16:42 [notice] 1#1: start worker process 29
2024/03/31 00:16:42 [notice] 1#1: start worker process 30
2024/03/31 00:16:42 [notice] 1#1: start worker process 31
2024/03/31 00:16:42 [notice] 1#1: start worker process 32
2024/03/31 00:16:42 [notice] 1#1: start worker process 33
2024/03/31 00:16:42 [notice] 1#1: start worker process 34
2024/03/31 00:16:42 [notice] 1#1: start worker process 35
2024/03/31 00:16:42 [notice] 1#1: start worker process 36
```


## クリーンナップ
```
minikube delete
```

## 参考リンク
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_logs/
- https://kubernetes.io/docs/concepts/cluster-administration/logging/
