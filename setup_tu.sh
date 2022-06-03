#!/bin/bash

mkdir -p "/home/ubuntu/projet_AE/CI_fastapi_projet_ae_ml"

echo ""
echo "phase de suppression des containers antérieurs"
docker container rm fastapi_projet_ae_ml -f
docker container rm fastapi_projet_ae_ml_tu -f

echo ""
echo "phase de suppression des images antérieures"
docker image rm fastapi_projet_ae_ml -f 
docker image rm fastapi_projet_ae_ml_tu -f

echo ""
echo "suppression du sous réseau dédié"
docker network rm network_fastapi_projet_ae_ml

echo ""
echo "supression du volume dédié"
docker volume rm logs_fastapi_projet_ae_ml -f

echo ""
echo "création du volume dédié logs_fastapi_projet_ae_ml"
docker volume create --name logs_fastapi_projet_ae_ml


echo ""
echo "création du sous réseau spécifique network_api_ml_sa"
docker network create --subnet 172.50.0.0/16 --gateway 172.50.0.1 network_fastapi_projet_ae_ml

echo ""
echo "phase de création des images docker"
echo "========================================="
echo "création de l'image fastapi_projet_ae_ml "
echo "========================================="
sleep 5
fullpath='/home/ubuntu/projet_AE'
cd $fullpath
docker image build . -t fastapi_projet_ae_ml:latest
echo ""
echo "============================================"
echo "création de l'image fastapi_projet_ae_ml_tu "
echo "============================================"
sleep 5
fullpath='/home/ubuntu/projet_AE/app_tu'
cd $fullpath
echo $fullpath
docker image build . -t fastapi_projet_ae_ml_tu:latest


echo ""
echo "lancement du docker-compose à venir"
echo "avec le container FastAPI à tester et le container des tests unitaires associés"
echo ""
echo "pause du script pour lecture attentive de ces informations:"
echo "==========================================================================================="
echo "Note : fastapi_projet_ae_ml_tu exited with code 0"
echo "signifie que la campagne de test est terminée"
echo ""
echo "taper alors CTRL C pour envoyer un signal de fin au conteneur testé fastapi_projet_ae_ml" 
echo ""
echo "les logs de résultats seront disponibles sous /home/ubuntu/projet_AE/CI_fastapi_projet_ae_ml"
echo "============================================================================================"
sleep 15
docker-compose up

echo ""
echo "fichier résultat à consulter :"
fullpath='/home/ubuntu/projet_AE/CI_fastapi_projet_ae_ml'
cd $fullpath
echo $fullpath
recentfile=`ls -got | head -2 | tail -1 | awk '{print $7}'`
echo "$recentfile"
nbr_success=`grep OK $recentfile | wc -l`
nbr_echecs=`grep NOK $recentfile  | wc -l`
echo "résultats avec succés : $nbr_success"
echo "résultat(s) en échec  : $nbr_echecs"
