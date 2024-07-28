#!/bin/bash
minikube delete
minikube start --memory='4g' --cpus='4'
minikube addons disable storage-provisioner
minikube addons disable default-storageclass
minikube addons list
minikube addons enable ingress
minikube addons enable csi-hostpath-driver
minikube addons enable metrics-server
minikube addons enable dashboard
kubectl patch storageclass csi-hostpath-sc -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'
kubectl get sc