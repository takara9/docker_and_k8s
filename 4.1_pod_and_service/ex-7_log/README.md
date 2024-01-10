# logging


ログのアーキテクチャ

ログの管理

$ minikube delete
$ minikube start

$ kubectl run nginx1 --image=nginx:latest
pod/nginx1 created

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
2024/01/08 00:46:59 [notice] 1#1: using the "epoll" event method
2024/01/08 00:46:59 [notice] 1#1: nginx/1.25.3
2024/01/08 00:46:59 [notice] 1#1: built by gcc 12.2.0 (Debian 12.2.0-14) 
2024/01/08 00:46:59 [notice] 1#1: OS: Linux 6.5.11-linuxkit
2024/01/08 00:46:59 [notice] 1#1: getrlimit(RLIMIT_NOFILE): 1048576:1048576
2024/01/08 00:46:59 [notice] 1#1: start worker processes
2024/01/08 00:46:59 [notice] 1#1: start worker process 29
2024/01/08 00:46:59 [notice] 1#1: start worker process 30
2024/01/08 00:46:59 [notice] 1#1: start worker process 31
2024/01/08 00:46:59 [notice] 1#1: start worker process 32
2024/01/08 00:46:59 [notice] 1#1: start worker process 33
2024/01/08 00:46:59 [notice] 1#1: start worker process 34
2024/01/08 00:46:59 [notice] 1#1: start worker process 35
2024/01/08 00:46:59 [notice] 1#1: start worker process 36


$ kubectl port-forward pod/nginx1 9080:80
Forwarding from 127.0.0.1:9080 -> 80
Forwarding from [::1]:9080 -> 80


curl http://localhost:9080/


$ kubectl logs nginx1
<前略>
2024/01/08 00:46:59 [notice] 1#1: start worker process 35
2024/01/08 00:46:59 [notice] 1#1: start worker process 36
127.0.0.1 - - [08/Jan/2024:00:48:30 +0000] "GET / HTTP/1.1" 200 615 "-" "curl/8.4.0" "-"

