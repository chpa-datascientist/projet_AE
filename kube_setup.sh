#!/bin/bash

if [ "$#" -eq 0 ]
    then
        echo "lire attentivement"
        echo "pas de chemin fourni en argument donc /home/ubuntu pris comme localisation de projet_AE"
        rpath="/home/ubuntu"
        sleep 10
elif [ "$#" -ne 1 ]
    then
        echo "seulement un paramétre attendu , le path ou github projet_AE a été cloné"
        exit
else
    rpath=$1
    echo "lire attentivement"
    echo "$rpath est pris comme le chemin ou projet_AE a été déposé"
    sleep 10
fi

project="projet_AE"
path_app_prod="$rpath/$project"

echo ""
echo "arret du déploiement (pods applicatifs et le replicaset) du cluster kubernetes"
kubectl delete deployment fastapi-projet-ae-ml-prod-deployment -n=fastapi-projet-ae-ml-prod-ns

echo ""
echo "suppression du service de fast_api_ae_ml_prod"
kubectl delete svc fastapi-projet-ae-ml-prod-service -n=fastapi-projet-ae-ml-prod-ns

echo ""
echo "suppression de l'accés externe au cluster du service c'est à dire l'objet ingress"
kubectl delete ingress fastapi-projet-ae-ml-prod-ingress -n=fastapi-projet-ae-ml-prod-ns

echo ""
echo "suppression du namespace spécifique fastapi-projet-ae-ml-prod-ns"
#cette commande pourrait suffire à supprimer pods , le service et la régle Ingress
#mais je me méfie des commandes chapeau
kubectl delete namespaces fastapi-projet-ae-ml-prod-ns


echo ""
echo "phase de suppression de l'image antérieure"
docker image rm 16101965/fastapi-projet-ae-ml-prod -f 

echo ""
echo "téléchargement depuis docker hub de l'image"
echo "==========================================="
echo "image    161065/fastapi_projet_ae_ml_prod  "
echo "==========================================="
sleep 5
#fullpath='/home/ubuntu/projet_AE'
#cd $fullpath
cd $path_app_prod
#docker image build . -t fastapi-projet-ae-ml-prod:latest
#docker tag fastapi-projet-ae-ml-prod 16101965/fastapi-projet-ae-ml-prod
docker pull 16101965/fastapi-projet-ae-ml-prod
echo ""
echo "lancement du cluster kubernetes sur un seul noeud"
echo "dans la machine virtuelle linux avec minikube installé"
echo "son cluster démarré (minikube start)"
echo "cmd utile pour le vérifier : kubectl get pods -A | grep kube-system"
echo "et l'addon ingress activé (minikube addons enable ingress)"
echo ""
echo "pause du script pour lecture attentive"
echo "======================================"
sleep 10
kubectl create -f ./fastapi-projet-ae-ml-prod-ns.yaml
kubectl apply -f fastapi-projet-ae-ml-prod-deployment.yaml
kubectl create -f fastapi-projet-ae-ml-prod-service.yaml
kubectl create -f fastapi-projet-ae-ml-prod-ingress.yaml

echo ""
echo "pause 2 mn pour que les phases de création des containers"
echo "puis de démarrage des pods applicatifs soient finalisées"
echo "et que l'@IP externe ingress passe disponible"

sleep 120
echo "================================"
echo "namespace spécifique du projet :"
echo "================================"
kubectl get namespace | grep projet-ae-ml
echo "déploiement :"
kubectl get deployment -n=fastapi-projet-ae-ml-prod-ns | grep projet-ae-ml
echo "pods :"
kubectl get pod -n=fastapi-projet-ae-ml-prod-ns | grep projet-ae-ml
echo "replicaset :"
kubectl get replicaset -n=fastapi-projet-ae-ml-prod-ns | grep projet-ae-ml
echo "service :"
kubectl get service -n=fastapi-projet-ae-ml-prod-ns | grep projet-ae-ml
echo "accés externe au cluster du service ingress :"
kubectl get ingress -n fastapi-projet-ae-ml-prod-ns | grep projet-ae-ml
echo ""
echo "il reste à mettre en place un tunnel ssh avec cette adresse ingress"
echo "ssh -L 5000:@IP_address_ingress:port_ingress ubuntu@IP_address_host -p 22"
echo ""
echo "et ensuite ouvrir un navigateur sur URL localhost:5000/documentation pour profiter du modèle :-)" 
