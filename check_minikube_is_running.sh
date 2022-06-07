#!/bin/bash

echo "if the minikube cluster is not running, the kubectl cmdline is facing the connection to the server is refused" 
echo "minikube start       necessary to run it"
echo "Otherwise, if the minikube is running , 7 system pods are present" 
echo ""
kubectl get pods -A | grep kube-system
