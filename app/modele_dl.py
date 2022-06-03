import os
from fastapi import HTTPException, UploadFile
from fastapi.responses import JSONResponse 
import sys, os
import pickle
import cv2

from PIL import Image
import numpy as np
import h5py
import shutil

from tensorflow.keras.models import load_model

# import Rakuten project utils functions
from rakuten_constants import *
from rakuten_preprocessing_utils import *
from rakuten_processing_utils import *


text_test_status = "Harry Potter Tome 5 - Harry Potter Et L'ordre Du Phénix. A quinze ans, Harry s'apprête à entrer en cinquième année à Poudlard. Et s'il est heureux de retrouver le monde des sorciers, il n'a jamais été aussi anxieux. L'adolescence, la perspective des examens importants en fin d'année et ces étranges cauchemars... Car Celui-Dont-On-Ne-Doit-Pas-Prononcer-Le-Nom est de retour et, plus que jamais, Harry sent peser sur lui une terrible menace. Une menace que le ministère de la Magie ne semble pas prendre au sérieux, contrairement à Dumbledore. Poudlard devient alors le terrain d'une véritable lutte de pouvoir. La résistance s'organise autour de Harry qui va devoir compter sur le courage et la fidélité de ses amis de toujours... D'une inventivité et d'une virtuosité rares, découvrez le cinquième tome de cette saga que son auteur a su hisser au rang de véritable phénomène littéraire."
image_test_status = "livre_Harry_Potter.jpg"

def get_status(model_multimodal,tokenizer):
    """retourne le status de l'application DL
       et en simulant en interne la prédiction d'un produit
    """
    top3_classes_predites = {}
    # doit contenir la prédiction des 3 classes les plus probables pour le produit échantillon
    top3_classes_predites = apply_prediction_dl(model_multimodal,tokenizer,DEST_IMG_TEST,text_test_status,image_test_status)
    if (len(top3_classes_predites) != 0):
        return True
    else:
        return False

def get_list_classes():
    dict_classes = { i+1 : name_class[i] for i in range(0, len(name_class) ) }
    return dict_classes

def copy_file_on_disk(src,dst) -> None:
    try:
        src.file.seek(0)
        with open(dst,"wb+") as outFile:
            shutil.copyfileobj(src.file, outFile,1024)
    finally:
        src.file.close()


def update_weights(file_weights):
    try:
        fullpath_weights = os.path.join(DEST_NN_WEIGHTS_FILE, file_weights.filename)
        copy_file_on_disk(file_weights,fullpath_weights)

        file_to_be_checked = h5py.File(fullpath_weights, 'r')
        list_elmts = [key for key in file_to_be_checked['/'].keys()]
        if(len(list_elmts) !=2):
            os.remove(fullpath_weights)
            raise HTTPException(status_code=409, detail="La vérification sur la présence de 2 groupes (couches modèle et optimiseur) dans le fichier HDF5 a échoué ainsi le fichier n'a pas été stocké")

    except Exception as e:
        if ( str(e) == "Unable to open file (file signature not found)"):
            os.remove(fullpath_weights)
            raise HTTPException(status_code=409, detail="il ne s'agit surement pas d'un fichier au format hdf5 !!")
        else:        
            return JSONResponse(
            status_code = 400,
            content = { 'message' : str(e) }
            )
    else:
        return JSONResponse(
            status_code = 200,
            content = {"File saved to disk at": fullpath_weights}
            )


def chargement_model():
    fullpath_weights = os.path.join(DEST, 'Rakuten_multimodal.weights.270122.hdf5')
    loaded_model = load_model(fullpath_weights)
    return loaded_model


def chargement_tokenizer():
    # load tokenizer used when model was trained
    fullpath_tokenizer = os.path.join(DEST, 'Rakuten_tokenizer.pickle')
    with open(fullpath_tokenizer, "rb") as handle:
        loaded_tokenizer = pickle.load(handle)
    return loaded_tokenizer


def apply_prediction_dl(model_multimodal,tokenizer,DEST,text,image):

    test_pred_class_r = []
    three_best_classes_r = []

    cropped_image_name = suppress_white_areas(DEST, image)
    cropped_image_name = DEST + cropped_image_name
    img_tensor = transform_image(cropped_image_name, target_size)

    str_tokens = preprocessing_text(text)
    txt_tensor = transform_text(str_tokens, text_size, tokenizer)

    test_pred_r = model_multimodal.predict([img_tensor, txt_tensor])
    test_pred_class_img_r = test_pred_r.argmax(axis=1)
    # this highest probability set to 0 to find out the second better
    test_pred_r[0][test_pred_class_img_r] = 0
    test_pred_class_img2_r = test_pred_r.argmax(axis=1)
    # this second probability set to 0 to find out the thrid better
    test_pred_r[0][test_pred_class_img2_r] = 0
    test_pred_class_img3_r = test_pred_r.argmax(axis=1)
    test_pred_class_r.append(test_pred_class_img_r[0])
    # we keep 3 classes with best probabilities given by softmax at output of the model
    three_best_classes_r.append(test_pred_class_img_r[0])
    three_best_classes_r.append(test_pred_class_img2_r[0])
    three_best_classes_r.append(test_pred_class_img3_r[0])

    dict_top_3 = {"1": name_class[three_best_classes_r[0]], "2":name_class[three_best_classes_r[1]], "3":name_class[three_best_classes_r[2]]}
    return dict_top_3
