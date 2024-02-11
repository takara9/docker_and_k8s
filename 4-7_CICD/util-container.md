
mini:util-container takara$ echo $CR_PAT | docker login ghcr.io -u $USERNAME --password-stdin
Login Succeeded
mini:util-container takara$ docker images
REPOSITORY                        TAG             IMAGE ID       CREATED          SIZE
my-ubuntu                         0.3             7d24590da482   2 minutes ago    491MB
testredis                         latest          b42731aa79dd   12 minutes ago   453MB
drupal                            latest          1b0c32ed8f78   11 days ago      605MB
busybox                           latest          3e4fd538a9a0   11 days ago      4.04MB
ubuntu                            latest          e2e172ecd069   2 weeks ago      69.3MB
gcr.io/k8s-minikube/kicbase       v0.0.42         62753ecb37c4   2 months ago     1.11GB
docker/volumes-backup-extension   1.1.4           6f83fec5da84   7 months ago     117MB
mariadb                           10.3.39-focal   4c465ff0642c   8 months ago     356MB
felipecruz/alpine-tar-zstd        latest          055e5a7f538a   16 months ago    6.7MB
justincormack/nsenter1            latest          d598f2517351   3 years ago      118kB
mini:util-container takara$ docker tag my-ubuntu:0.3 ghcr.io/takara9/my-ubuntu:0.3
mini:util-container takara$ docker images
REPOSITORY                        TAG             IMAGE ID       CREATED          SIZE
my-ubuntu                         0.3             7d24590da482   3 minutes ago    491MB
ghcr.io/takara9/my-ubuntu         0.3             7d24590da482   3 minutes ago    491MB
testredis                         latest          b42731aa79dd   13 minutes ago   453MB
drupal                            latest          1b0c32ed8f78   11 days ago      605MB
busybox                           latest          3e4fd538a9a0   11 days ago      4.04MB
ubuntu                            latest          e2e172ecd069   2 weeks ago      69.3MB
gcr.io/k8s-minikube/kicbase       v0.0.42         62753ecb37c4   2 months ago     1.11GB
docker/volumes-backup-extension   1.1.4           6f83fec5da84   7 months ago     117MB
mariadb                           10.3.39-focal   4c465ff0642c   8 months ago     356MB
felipecruz/alpine-tar-zstd        latest          055e5a7f538a   16 months ago    6.7MB
justincormack/nsenter1            latest          d598f2517351   3 years ago      118kB
mini:util-container takara$ docker push ghcr.io/takara9/my-ubuntu:0.3
The push refers to repository [ghcr.io/takara9/my-ubuntu]
5f70bf18a086: Mounted from maho/probe 
8f5b01b61aef: Pushed 
01de117294a0: Pushed 
7e4da3c488e5: Pushed 
0.3: digest: sha256:5f4a9ee89e6c92b8c1fa6e0af0c9da0c07277626178302ddeb637972b03a0c1d size: 1154


mini:util-container takara$ docker images
REPOSITORY                        TAG             IMAGE ID       CREATED          SIZE
my-ubuntu                         0.3             7d24590da482   5 minutes ago    491MB
ghcr.io/takara9/my-ubuntu         0.3             7d24590da482   5 minutes ago    491MB
testredis                         latest          b42731aa79dd   15 minutes ago   453MB
drupal                            latest          1b0c32ed8f78   11 days ago      605MB
busybox                           latest          3e4fd538a9a0   11 days ago      4.04MB
ubuntu                            latest          e2e172ecd069   2 weeks ago      69.3MB
gcr.io/k8s-minikube/kicbase       v0.0.42         62753ecb37c4   2 months ago     1.11GB
docker/volumes-backup-extension   1.1.4           6f83fec5da84   7 months ago     117MB
mariadb                           10.3.39-focal   4c465ff0642c   8 months ago     356MB
felipecruz/alpine-tar-zstd        latest          055e5a7f538a   16 months ago    6.7MB
justincormack/nsenter1            latest          d598f2517351   3 years ago      118kB



kubectl run -i --tty tools --image=ghcr.io/takara9/my-ubuntu:0.3 -- bash


nobody@tools:/app$ dig redis-cluster-leader-headless.ot-operators.svc.cluster.local 

; <<>> DiG 9.18.18-0ubuntu0.22.04.1-Ubuntu <<>> redis-cluster-leader-headless.ot-operators.svc.cluster.local
;; global options: +cmd
;; Got answer:
;; WARNING: .local is reserved for Multicast DNS
;; You are currently testing what happens when an mDNS query is leaked to DNS
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 15759
;; flags: qr aa rd; QUERY: 1, ANSWER: 3, AUTHORITY: 0, ADDITIONAL: 1
;; WARNING: recursion requested but not available

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
; COOKIE: a3861cfcef04871a (echoed)
;; QUESTION SECTION:
;redis-cluster-leader-headless.ot-operators.svc.cluster.local. IN A

;; ANSWER SECTION:
redis-cluster-leader-headless.ot-operators.svc.cluster.local. 19 IN A 10.244.0.29
redis-cluster-leader-headless.ot-operators.svc.cluster.local. 19 IN A 10.244.0.27
redis-cluster-leader-headless.ot-operators.svc.cluster.local. 19 IN A 10.244.0.28

;; Query time: 1 msec
;; SERVER: 10.96.0.10#53(10.96.0.10) (UDP)
;; WHEN: Mon Jan 29 07:27:50 UTC 2024
;; MSG SIZE  rcvd: 329


mini:redis-client takara$ docker tag redis-test:0.1 ghcr.io/takara9/redis-test:0.1
mini:redis-client takara$ docker push ghcr.io/takara9/redis-test:0.1
The push refers to repository [ghcr.io/takara9/redis-test]
06ac7c129d4a: Pushed 
5f70bf18a086: Mounted from takara9/my-ubuntu 
cfa64e861a01: Pushed 
82a37f1dcf77: Pushed 
8a48150d96f3: Pushed 
7e4da3c488e5: Mounted from takara9/my-ubuntu 
0.1: digest: sha256:6cf7201a282c1545fbd50e65d0976cfe672f2293a09db48595923097ac2f4102 size: 1572


kubectl run -i --tty tools --image=ghcr.io/takara9/redis-test:0.1 -- bash

