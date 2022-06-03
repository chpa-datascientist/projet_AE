import os
import uvicorn
from fastapi import FastAPI, HTTPException, Response, Depends, status, File, UploadFile, Form
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse
from passlib.context import CryptContext
import modele_dl 
from  typing import List
import aiofiles
from rakuten_constants import *

model_multimodal = modele_dl.chargement_model()
tokenizer = modele_dl.chargement_tokenizer()


app = FastAPI(title='Prédiction de la classe d un produit de e-commerce dans le cadre du challenge data ENS Rakuten avec une taxinomie réduite à 27 classes',
    description ='Cet API propose un modèle de prédiction de Deep Learning bimodal auquel on fournit le texte et une image du produit en complément obligatoirement<br>et qui retourne les 3 classes les plus probables parmi celles disponibles',
    contact={
        "name": "christophe Paquet",
        "url": "https://datascientest.com/",
        "email": "paquet.christophe@orange.fr",
    },
    openapi_tags=[
    {
        'name': 'Utilisateurs',
        'description': 'Gestion de l authentification / autorisation d un utilisateur'
    },
    {
        'name': 'Status API',
        'description': 'Informe si l application est fonctionnelle'
    },
    {
        'name': 'Modeles de classification',
        'description': 'Utilisation de l un des modéles de classification'
    },
    {
        'name': 'Gestion de l evolution des modeles par l ingénieur ML',
        'description': 'activités relatives au suivi en production de ces modéles'
    }

],docs_url="/documentation", redoc_url=None, version="examen_déploiement_ML_datascientest", debug=True)

security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


users = {

    "alice": {
        "username": "alice",
        "name": "alice future datascientist",
        "hashed_password": pwd_context.hash('wonderland'),
    },

    "bob" : {
        "username" :  "bob",
        "name" : "bob futur Machine Learning Engineer",
        "hashed_password" : pwd_context.hash('builder'),
    },

    "clementine": {
        "username": "clementine",
        "name": "clementine future Data Engineer",
        "hashed_password": pwd_context.hash('mandarine'),
    }
}

users_admin = {

    "admin": {
        "username": "admin",
        "name": "admin role",
        "hashed_password": pwd_context.hash('4dm1N'),
    }
}

def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users.get(username)) or not(pwd_context.verify(credentials.password, users[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="utilisateur inconnu ou mot de passe erroné",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

def get_admin_user(credentials: HTTPBasicCredentials = Depends(security)):
    username = credentials.username
    if not(users_admin.get(username)) or not(pwd_context.verify(credentials.password, users_admin[username]['hashed_password'])):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="vous n'avez pas le role admin ou mot de passe erroné",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get('/')
def get_index():
    return "Hello world and Daniel team :-) "

@app.get("/login_utilisateur", name='utilisateur applicatif courant',tags=['Utilisateurs'])
def current_user(username: str = Depends(get_current_user)):
    return "Bonjour {}".format(username)

@app.get("/login_admin", name='administrateur',tags=['Utilisateurs'])
def current_user(username: str = Depends(get_admin_user)):
    return "Bonjour {}".format(username)

@app.get('/status', name='Status applicatif', tags=['Status API'])
async def get_status(username: str = Depends(get_current_user)):
    model_dl_ready = modele_dl.get_status(model_multimodal,tokenizer)
    if (model_dl_ready == True):
        return "le modéle est opérationnel"
    else:
        return "le modéle n'est actuellement pas opérationnel"

@app.get('/list_27_classes', name='taxinomie réduite challenge data Rakuten', tags=['Modeles de classification'])
async def get_list_classes():
       return modele_dl.get_list_classes()

@app.get('/architecture_model',name='Architecture du modèle DL framework tensorflow', tags=['Modeles de classification'])
def get_performance(username: str = Depends(get_current_user)):
    return FileResponse(os.path.join(DEST_IMG_TEST, 'keras_plot_model.png'))

@app.get('/performance_model',name='Résultats de classification du modèle sur le jeu de test qui lui est totalement inconnu', tags=['Modeles de classification'])
def get_performance(username: str = Depends(get_current_user)):
    return FileResponse(os.path.join(DEST_IMG_TEST, 'classification_reportDL.png'))

@app.get('/heatmap_model',name='matrice de confusion des différentes classes sur le jeu de test', tags=['Modeles de classification'])
def get_performance(username: str = Depends(get_current_user)):
    return FileResponse(os.path.join(DEST_IMG_TEST, 'heatmapDL.png'))
 

@app.post('/predict_dl', name='Classification à l aide d un modéle de Deep Learning', response_model="", tags=['Modeles de classification'])
async def apply_prediction_dl(image_produit: UploadFile, texte_produit: str = Form(...), username: str = Depends(get_current_user)):
    """ Modéle développé avec la logique de classification fournie par Rakuten<br>
        donc il est cohérent d'utiliser comme site référence fr.shopping.rakuten.com<br>
        pour y prendre obligatoirement 2 informations :<br>
        le texte du produit qui doit comporter au moins 4 mots<br>
        et etre constitué soit de son titre seul soit du titre concaténé avec le descriptif de l article<br><br>
        ET son image au format classique jpeg, png<br><br>
        **Le modéle retourne 3 propositions de classes dans l'ordre le plus probable**
    """
    # test que le texte est constitué d'au moins 4 mots
    list_mots = texte_produit.split()
    if (len(list_mots) < 4):
        raise HTTPException(status_code=400, detail="le texte doit au moins comporté 4 mots et seulement {0} recus".format(len(list_mots)))
    # nettoyage du répertoire de travail spécifique
    list_imgs = [ f for f in os.listdir(DEST_IMG) if os.path.isfile(os.path.join(DEST_IMG,f)) ]
    for img in list_imgs:
        fullpath_img = os.path.join(DEST_IMG,img)
        os.remove(fullpath_img)

    try:
        fullpath_img = os.path.join(DEST_IMG, image_produit.filename)
        async with aiofiles.open(fullpath_img, 'wb') as out_file:
            content = await image_produit.read()  # async read
            await out_file.write(content)  # async write

    except Exception as e:
        return JSONResponse(
            status_code = 400,
            content = { 'message' : str(e) }
            )

    return modele_dl.apply_prediction_dl(model_multimodal,tokenizer,DEST_IMG,texte_produit,image_produit.filename)

@app.post('/download_new_NN_weights', name='Téléchargement d un nouveau fichier de poids pour configurer le réseau de neurones', response_model="", tags=['Gestion de l evolution des modeles par l ingénieur ML'])
def store_new_weights_file(file_weights: UploadFile = File(...), username: str = Depends(get_admin_user)):
    """ permet d'introduire des évolutions dans le modéle DL
    """
    return modele_dl.update_weights(file_weights)



#if __name__ == "__main__":
#    uvicorn.run(app, host="127.0.0.1", port=8000)
