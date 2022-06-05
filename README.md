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

**modèle de classification choisi pour la généralisation :**<br />
basé sur une architecture DL framework tensorflow multimodale (texte + image)<br />

Christophe Paquet [LinkedIn](https://www.linkedin.com/in/c-paquet-machine-and-deep-learning-for-fun)


