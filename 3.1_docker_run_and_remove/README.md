# Commands

## Hallo worldの表示

docker run --name hw hello-world

## クリーンナップ
docker rm hw
docker rmi hello-world:latest


## イメージの取得
docker pull ghcr.io/takara9/my-ubuntu:0.2 <-- 不要ではないか

## 対話型コンテナの実行
docker run -it --name mu ghcr.io/takara9/my-ubuntu:0.2
exit


## クリーンナップ
docker rm mu
docker rmi ghcr.io/takara9/my-ubuntu:0.2


~~~
$ podman run hello-world
Resolved "hello-world" as an alias (/etc/containers/registries.conf.d/000-shortnames.conf)
Trying to pull quay.io/podman/hello:latest...
Getting image source signatures
Copying blob sha256:d08b40be68780d583e8c127f10228743e3e1beb520f987c0e32f4ef0c0ce8020
Copying config sha256:e2b3db5d4fdf670b56dd7138d53b5974f2893a965f7d37486fbb9fcbf5e91d9d
Writing manifest to image destination
!... Hello Podman World ...!

         .--"--.           
       / -     - \         
      / (O)   (O) \        
   ~~~| -=(,Y,)=- |         
    .---. /`  \   |~~      
 ~/  o  o \~~~~.----. ~~   
  | =(X)= |~  / (O (O) \   
   ~~~~~~~  ~| =(Y_)=-  |   
  ~~~~    ~~~|   U      |~~ 

Project:   https://github.com/containers/podman
Website:   https://podman.io
Documents: https://docs.podman.io
Twitter:   @Podman_io
~~~

~~~
$ podman ps -a
CONTAINER ID  IMAGE                          COMMAND               CREATED        STATUS                    PORTS       NAMES
c172732f5aeb  ghcr.io/takara9/my-ubuntu:0.1  bash                  4 weeks ago    Exited (0) 4 weeks ago                upbeat_zhukovsky
55407179f5fd  quay.io/podman/hello:latest    /usr/local/bin/po...  3 minutes ago  Exited (0) 3 minutes ago              romantic_booth
~~~



~~~
$ podman run index.docker.io/hello-world

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
~~~



