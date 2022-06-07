#!/bin/bash

if [ "$#" -eq 0 ]
    then
        echo "lire attentivement"
        echo "pas de chemin fourni en argument donc /home/ubuntu pris comme localisation de projet_AE"
        echo "contrainte : le container tu écrit ses logs dans le home du shell actuel"
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
    echo "contrainte : le container tu écrit ses logs dans le home du shell actuel"
    sleep 10
fi

project="projet_AE"
app="app"
app_tu="app_tu"
CI_logs="CI_fastapi_projet_ae_ml"
file_weights="Rakuten_multimodal.weights.270122.hdf5"
new_weights_name="tu_weights.hdf5"
path_project_ci_logs="$rpath/$project/$CI_logs"
path_app="$rpath/$project/$app"
path_app_tu="$rpath/$project/$app_tu"
file_hdf5="$path_app/$file_weights"
file_hdf5_tu_orig="$path_app_tu/$file_weights"
file_hdf5_tu_dest="$path_app_tu/$new_weights_name"

mkdir -p $path_project_ci_logs
#mkdir -p "/home/ubuntu/projet_AE/CI_fastapi_projet_ae_ml"
#huge file only stored once under github so local copy to be used in tu container for one test of the admin MLE role 
cp $file_hdf5 $path_app_tu
#cp /home/ubuntu/projet_AE/app/Rakuten_multimodal.weights.270122.hdf5 /home/ubuntu/projet_AE/app_tu
mv $file_hdf5_tu_orig $file_hdf5_tu_dest
#mv /home/ubuntu/projet_AE/app_tu/Rakuten_multimodal.weights.270122.hdf5 /home/ubuntu/projet_AE/app_tu/tu_weights.hdf5
sleep 5
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
#fullpath='/home/ubuntu/projet_AE/app'
#cd $fullpath
cd $path_app
docker image build . -t fastapi_projet_ae_ml:latest
echo ""
echo "============================================"
echo "création de l'image fastapi_projet_ae_ml_tu "
echo "============================================"
sleep 5
#fullpath='/home/ubuntu/projet_AE/app_tu'
#cd $fullpath
cd $path_app_tu
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
echo "les logs de résultats seront disponibles sous $path_project_ci_logs"
echo "============================================================================================"
sleep 15
docker-compose up

echo ""
echo "fichier résultat à consulter sous $path_project_ci_logs"
#fullpath='/home/ubuntu/projet_AE/CI_fastapi_projet_ae_ml'
#cd $fullpath
cd $path_project_ci_logs
recentfile=`ls -got | head -2 | tail -1 | awk '{print $7}'`
echo "$recentfile"
nbr_success=`grep OK $recentfile | wc -l`
nbr_echecs=`grep NOK $recentfile  | wc -l`
echo "résultats avec succés : $nbr_success"
echo "résultat(s) en échec  : $nbr_echecs"
