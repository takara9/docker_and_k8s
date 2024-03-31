kubectl apply -f configmap.yaml
kubectl apply -f pod.yaml


$ kubectl exec -it my-ubuntu2 -- bash
root@my-ubuntu2:/# env | grep POSTGRES
POSTGRES_PASSWORD=pr0dr0b0t
POSTGRES_USER=product_robot
POSTGRES_DB=product


