# projet_AE
Modèle de classification bimodale (text , image) accessible sur une interface FasAPI.

# Contexte
Ce projet a été réalisé dans le cadre de la formation Data Scientist de Datascientest (promotion formation continue mai 2021) 
et du challenge Rakuten France Multimodal Product Data Classification.
Ce projet R&D a ensuite servi de base pour apprendre le processus de mise en production durant la formation Approfondissement Engineering (promotion formation continue mars 2022)

# Objectif 
Le problème consiste, à partir d'informations de textes et d'une image associés à chaque produit du catalogue, à classifier automatiquement ceux ci avec la meme taxinomie que Rakuten avec le moins d'erreurs possibles.<br />
En réalité, la taxinomie Rakuten comprend plus de 1000 catégories, mais dans le cadre de ce challenge, l'étude proposée est limitée à seulement 27 de celles ci.

# Jeu de données
Lors de l'inscription au challenge , Rakuten met à disposition un jeu de données pour l'entrainement (et la validation) de 84916 observations 
et un jeu de test de 13812 articles sans label pour pouvoir déposer une réponse de classification associée au concours.

Chaque échantillon représente un article du catalogue de la plateforme de e-commerce Rakuten France, et comporte nécessairement un champ textuel désignation ainsi qu'une image , et potentiellement une description textuelle plus détaillée additionnelle.


# Description des fichiers
Le dossier app contient les sources python associés au modèle de classification incluant le préprocessing NLP du texte.<br>
Le dossier app_tu contient le jeu de tests unitaires<br>
**Note : il manque sous app le fichier de 452 Mb des poids du réseaux de neurones sauvegardés dans la phase entrainement**<br>
Le shell setup_tu.sh associé au docker-compose.yml<br>
(aprés clonage du projet sur une machine virtuelle linux ou docker et docker-compose sont installés)<br>
sert au déploiement des deux containers (système testé et sa série de tests untaires)<br> 
qui permettra de vérifier si le modèle peut etre exposé en production.<br><br>
Le shell kube_setup.sh sert à démarrer l'application dans un cluster kubernetes (minikube avec un seul noeud) <br>
aprés avoir téléchargée celle ci depuis docker hub<br>
Le shell check_minikube_is_running.sh aide à vérifier que les pods systéme de minikube sont bien lancés sur la VM. 

**modèle de classification choisi pour la généralisation :**<br />
basé sur une architecture DL framework tensorflow multimodale (texte + image)<br />

Christophe Paquet [LinkedIn](https://www.linkedin.com/in/c-paquet-machine-and-deep-learning-for-fun)


