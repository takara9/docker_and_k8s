mini:ex-8_cm takara$ cd part-3/
mini:part-3 takara$ ls -l
atotal 16
-rw-r--r--  1 takara  staff   407 Jan  8 17:48 cm.yaml
-rw-r--r--  1 takara  staff  1020 Jan  8 17:54 pod.yaml

mini:part-3 takara$ kubectl apply -f cm.yaml 
configmap/game-demo created
mini:part-3 takara$ kubectl apply -f pod.yaml 
pod/pod-configmap created
mini:part-3 takara$ kubectl get po
NAME            READY   STATUS              RESTARTS   AGE
pod-configmap   0/1     ContainerCreating   0          4s


mini:part-3 takara$ kubectl get po
NAME            READY   STATUS    RESTARTS   AGE
pod-configmap   1/1     Running   0          21s


mini:part-3 takara$ kubectl exec -it pod-configmap -- bash
root@pod-configmap:/# echo $PLAYER_INITIAL_LIVES
3
root@pod-configmap:/# echo $UI_PROPERTIES_FILE_NAME
user-interface.properties

root@pod-configmap:/# ls -la /config
total 12
drwxrwxrwx 3 root root 4096 Jan  8 08:56 .
drwxr-xr-x 1 root root 4096 Jan  8 08:56 ..
drwxr-xr-x 2 root root 4096 Jan  8 08:56 ..2024_01_08_08_56_45.1662400597
lrwxrwxrwx 1 root root   32 Jan  8 08:56 ..data -> ..2024_01_08_08_56_45.1662400597
lrwxrwxrwx 1 root root   22 Jan  8 08:56 game.properties -> ..data/game.properties
lrwxrwxrwx 1 root root   32 Jan  8 08:56 user-interface.properties -> ..data/user-interface.properties

root@pod-configmap:/# cat /config/game.properties        
enemy.types=aliens,monsters
player.maximum-lives=5    

root@pod-configmap:/# cat /config/user-interface.properties 
color.good=purple
color.bad=yellow
allow.textmode=true   