

~~~
# コンフィグマップにするディレクトリconfigを確認する
$ ls -F
README-1.md             cm-kv.yaml              pod-cm-dir.yaml
README.md               config/                 pod-cm-kv.yaml

# 中には、二つのテキストファイル
$ ls config
default.config  test.conf
~~~



~~~
# コマンドで、ディレクトリをコンフィグマップにする
$ kubectl create cm app-conf --from-file=config
configmap/app-conf created

# コンフィグマップが出来た事を確認
$ kubectl get cm app-conf
NAME               DATA   AGE
app-conf           1      15s
~~~



~~~
$ kubectl describe cm app-conf
Name:         app-conf
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
default.config:  (1)マウントすると、ファイル名になり、以下は内容
----
server {
    listen 9200;
    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}

test.conf:  (2)同様にファイル名と内容
----
server-test {
    listen 9202;
    location / {
        root   /htdocs/html;
        index  index.html;
    }
}

BinaryData　(3)バイナリデータは無し
====

Events:  <none>
~~~



~~~
# コンフィグマップをマウントするポッドをデプロイ
$ kubectl apply -f pod-cm-dir.yaml 
pod/pod-cm-vol created

# ポッドに入って、マウントしたコンフィグマップのファイルを確認
$ kubectl exec -it pod-cm-vol -- bash
nobody@pod-cm-vol:/app$ ls /conf
default.config  test.conf

nobody@pod-cm-vol:/app$ cat /conf/test.conf 
server-test {
    listen 9202;
    location / {
        root   /htdocs/html;
        index  index.html;
    }
}
~~~





~~~
# キーとバリューを登録したコンフィグマップをデプロイ
$ kubectl apply -f cm-kv.yaml 
configmap/game-params created

$ kubectl get cm game-params
NAME          DATA   AGE
game-params   4      12s

$ kubectl describe cm game-params
Name:         game-params
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
user-interface.properties:　(1)マウントするとファイル名、以下はファイルの内容
----
color.good=purple
color.bad=yellow
allow.textmode=true   

game.properties:　(2)同様にファイル名と内容になる
----
enemy.types=aliens,monsters
player.maximum-lives=5    

player_initial_lives:
----
3
ui_properties_file_name:
----
user-interface.properties

BinaryData　(3)バイナリデータは無し
====

Events:  <none>
~~~


~~~
# コンフィグマップをマウントするポッドをデプロイ
$ kubectl apply -f pod-cm-kv.yaml 
pod/pod-cm-kv created
$ kubectl get pod/pod-cm-kv
NAME        READY   STATUS    RESTARTS   AGE
pod-cm-kv   1/1     Running   0          12s

# ポッドに入って、マウントしたコンフィグマップを確認する
$ kubectl exec -it pod-cm-kv -- bash

# マウントしたコンフィグマップを確認、二つのファイルが見える
nobody@pod-cm-kv:/app$ cd /config
nobody@pod-cm-kv:/config$ ls
game.properties  user-interface.properties

# ファイルを表示すると、コンフィグマップに設定したキーとバリューのリストが確認できる
nobody@pod-cm-kv:/config$ cat game.properties 
enemy.types=aliens,monsters
player.maximum-lives=5    

# もう一つのファイルも同様に確認できる
nobody@pod-cm-kv:/config$ cat user-interface.properties 
color.good=purple
color.bad=yellow
allow.textmode=true   
~~~
