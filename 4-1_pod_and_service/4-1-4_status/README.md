## 4.1.4. ポッドとコンテナの状態管理

実行例 4.1.4-1 ポッドのフェーズ表示
```
$ kubectl run my-pod --image=ubuntu --restart=Never
pod/my-pod created
$ kubectl get pod my-pod -o jsonpath='{.status.phase}';echo
Succeeded
```


実行例 4.1.4-2 ポッド上のコンテナのステータス表示
```
$ kubectl get pod my-pod -o jsonpath='{.status.containerStatuses[]}'| jq -r .
{
  "containerID": "docker://b7c16cda01d27cd32ee0acb8c8fd92f0f98ca7153cb259cda6e4d67436e49031",
  "image": "ubuntu:latest",
  "imageID": "docker-pullable://ubuntu@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e",
  "lastState": {},
  "name": "my-pod",
  "ready": false,
  "restartCount": 0,
  "started": false,
  "state": {
    "terminated": {
      "containerID": "docker://b7c16cda01d27cd32ee0acb8c8fd92f0f98ca7153cb259cda6e4d67436e49031",
      "exitCode": 0,
      "finishedAt": "2024-03-31T00:05:18Z",
      "reason": "Completed",
      "startedAt": "2024-03-31T00:05:18Z"
    }
  }
}
```


実行例 4.1.4-3　ポッドのデプロイとログの表示
```
$ kubectl run nginx1 --image=nginx:latest
pod/nginx1 created

$ kubectl logs nginx1
Error from server (BadRequest): container "nginx1" in pod "nginx1" is waiting to start: ContainerCreating

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

