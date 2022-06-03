import os
import time
import shutil
from datetime import datetime
import re
import requests
from requests.auth import HTTPBasicAuth

#délai pour que le modèle DL soit créé à partir du fichier de poids ainsi que le tokenizer
# et enfin que la librairie NLP spacy charge son modèle large 
time.sleep(90)

# définition de l'adresse de l'API
#api_address = '172.50.0.2'
#service fastapi défini dans le fichier docker-compose.yml
api_address = 'fastapi'
# port de l'API
api_port = 80

headers = {
    'accept': 'application/json',
}

output = '''
    test_description_status = {status}
    status_code = {status_code} 
    content = {content}

    '''

r = requests.get('http://{address}:{port}/status'.format(address=api_address,port=api_port), headers=headers)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 401):
    print("\ntest route status sans etre authentifié accés refusé OK")
    print("content:\n",content)
    status = "test route status sans etre authentifié accés refusé OK"
else:
    print("\ntest route status sans etre authentifié accés refusé NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route status sans etre authentifié accés refusé NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))

#########################
# utilisateur applicatif
#########################

basic = HTTPBasicAuth('alice', 'wonderland')

url1='http://{address}:{port}/login_utilisateur'.format(address=api_address, port=api_port)
url2='http://{address}:{port}/status'.format(address=api_address, port=api_port)
url3='http://{address}:{port}/list_27_classes'.format(address=api_address, port=api_port)
list_url = [url1,url2,url3]
#list_url = ['http://localhost:8000/login_utilisateur','http://localhost:8000/status','http://localhost:8000/list_27_classes']
list_route = ['login_utilisateur','status','list_27_classes']
for url , route in zip(list_url,list_route):
    r = requests.get(url, auth=basic)

    # statut de la requête
    status_code = r.status_code
    content = r.content
    if (status_code == 200):
        print("\ntest {0} OK".format(route))
        print("content:\n",content)
        status = "test {0} OK".format(route) 
        # impression dans un fichier
        if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content=content))
    else:
        print("\ntest {0} NOK".format(route))
        status = "test {0} NOK".format(route)
        # impression dans un fichier
        if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content="no meaningfull"))

url1='http://{address}:{port}/architecture_model'.format(address=api_address, port=api_port)
url2='http://{address}:{port}/performance_model'.format(address=api_address, port=api_port)
url3='http://{address}:{port}/heatmap_model'.format(address=api_address, port=api_port)
list_url = [url1,url2,url3]
#list_url = ['http://localhost:8000/architecture_model','http://localhost:8000/performance_model','http://localhost:8000/heatmap_model']
list_route = ['architecture_model','performance_model','heatmap_model']
for url , route in zip(list_url,list_route):
    r = requests.get(url, auth=basic)

    # statut de la requête
    status_code = r.status_code
    content = r.content
    if (status_code == 200):
        print("\ntest {0} OK".format(route))
        #print("content:\n",content)
        status = "test {0} OK".format(route)
        # impression dans un fichier
        if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content="image not logged"))
    else:
        print("\ntest {0} NOK".format(route))
        status = "test {0} NOK".format(route)
        # impression dans un fichier
        if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content="no meaningfull"))

headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWxpY2U6d29uZGVybGFuZA==',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_produit': open('./console.jpg', 'rb'),
    'texte_produit': (None, '"Nintendo Switch Oled - Blanc"'),
}

r = requests.post('http://{address}:{port}/predict_dl'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route predict_dl authentifié OK")
    print("content:\n",content)
    status = "test route predict_dl authentifié OK"
else:
    print("\ntest route predict_dl authentifié NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route predict_dl authentifié NOK" 

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))


headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWxpY2U6d29uZGVybGFuZA==',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_produit': open('./console.jpg', 'rb'),
    'texte_produit': (None, 'console playstation'),
}

r = requests.post('http://{address}:{port}/predict_dl'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl avec un texte trop court OK")
    print("content:\n",content)
    status = "test route predict_dl avec un texte trop court OK"
else:
    print("\ntest route predict_dl avec un texte trop court NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route predict_dl avec un texte trop court NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))

headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWxpY2U6d29uZGVybGFuZA==',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_produit': open('./console.jpg', 'rb'),
    'texte_produit': (None, '1 1 1 1'),
}

r = requests.post('http://{address}:{port}/predict_dl'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl erreur dans la détection de la langue du texte OK")
    print("content:\n",content)
    status = "test route predict_dl erreur dans la détection de la langue du texte OK"
else:
    print("\ntest route predict_dl erreur dans la détection de la langue du texte NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route predict_dl erreur dans la détection de la langue du texte NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))



headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWxpY2U6d29uZGVybGFuZA==',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_produit': open('./img_bidon.jpg', 'rb'),
    'texte_produit': (None, 'image problématique sans objet'),
}

r = requests.post('http://{address}:{port}/predict_dl'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl erreur dans la détection d un objet dans l image OK")
    print("content:\n",content)
    status = "test route predict_dl erreur dans la détection d un objet dans l image OK"
else:
    print("\ntest route predict_dl erreur dans la détection d un objet dans l image NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route predict_dl erreur dans la détection d un objet dans l image NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))


#########################################
#partie admin ingénieur Machine Learning 
#########################################

headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46NGRtMU4=',
}

r = requests.get('http://{address}:{port}/login_admin'.format(address=api_address,port=api_port), headers=headers)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route login_admin OK")
    print("content:\n",content)
    status = "test route login_admin OK"
    if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content=content))
else:
    print("\ntest route login_admin NOK")
    status = "test route login_admin NOK"
    if os.environ.get('LOG') == str(1):
            with open('/log/api_test.log', 'a') as file:
                file.write(output.format(status=status,status_code=status_code, content="no meaningfull"))




files = {
    'file_weights': open('./tu_weights.hdf5', 'rb'),
}

r = requests.post('http://{address}:{port}/download_new_NN_weights'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route download_new_NN_weights authentifié OK")
    print("content:\n",content)
    status = "test route download_new_NN_weights authentifié OK"
else:
    print("\ntest route download_new_NN_weights authentifié NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route download_new_NN_weights authentifié NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))



headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46NGRtMU4=',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'file_weights': open('./console.jpg', 'rb'),
}

r = requests.post('http://{address}:{port}/download_new_NN_weights'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 409):
    print("\ntest route download_new_NN_weights format incorrect non hdf5 rejeté OK")
    print("content:\n",content)
    status = "\ntest route download_new_NN_weights format incorrect non hdf5 rejeté OK"
else:
    print("\ntest route download_new_NN_weights format incorrect non hdf5 NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route download_new_NN_weights format incorrect non hdf5 rejeté NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))



headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46NGRtMU4=',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'image_produit': open('./console.jpg', 'rb'),
    'texte_produit': (None, '"Nintendo Switch Oled - Blanc"'),
}

r = requests.post('http://{address}:{port}/predict_dl'.format(address=api_address,port=api_port), headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 401):
    print("\ntest route predict_dl avec user admin non autorisé OK")
    print("content:\n",content)
    status = "test route predict_dl avec user admin non autorisé OK"
else:
    print("\ntest route predict_dl avec user admin non autorisé NOK")
    print(status_code)
    print("content:\n",content)
    status = "test route predict_dl avec user admin non autorisé NOK"

# impression dans un fichier
if os.environ.get('LOG') == str(1):
    with open('/log/api_test.log', 'a') as file:
        file.write(output.format(status=status,status_code=status_code, content=content))

#compte rendu global du résultat de la suite de tests unitaires stockés dans le home linux de l'utilisateur
#on récupére date et heure
current_datetime = datetime.now()
# convertion en caractéres en remplacement du caractére espace genant
str_current_datetime = str(current_datetime)
str_current_datetime = re.sub(r" ", "_", str_current_datetime)

# create a file object along with extension
file_name = "log_" + str_current_datetime + ".txt"
#variable d'environnement fournie dans le docker-compose.yml
#fullname = '/home/examen_docker/CI_API_ML_SA/' + file_name
fullname = os.environ.get('LOCATION_RESULT_FILE') + file_name
shutil.move('/log/api_test.log', fullname)
