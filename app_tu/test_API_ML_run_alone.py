import requests
from requests.auth import HTTPBasicAuth


headers = {
    'accept': 'application/json',
}

r = requests.get('http://localhost:8000/status', headers=headers)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 401):
    print("\ntest route status sans etre authentifié accés refusé OK")
    print("content:\n",content)
else:
    print("\ntest route status sans etre authentifié accés refusé NOK")
    print(status_code)
    print("content:\n",content)

#########################
# utilisateur applicatif
#########################

basic = HTTPBasicAuth('alice', 'wonderland')

list_url = ['http://localhost:8000/login_utilisateur','http://localhost:8000/status','http://localhost:8000/list_27_classes']
list_route = ['login_utilisateur','status','list_27_classes']
for url , route in zip(list_url,list_route):
    r = requests.get(url, auth=basic)

    # statut de la requête
    status_code = r.status_code
    content = r.content
    if (status_code == 200):
        print("\ntest {0} OK".format(route))
        print("content:\n",content)
    else:
        print("\ntest {0} NOK".format(route))

list_url = ['http://localhost:8000/architecture_model','http://localhost:8000/performance_model','http://localhost:8000/heatmap_model']
list_route = ['architecture_model','performance_model','heatmap_model']
for url , route in zip(list_url,list_route):
    r = requests.get(url, auth=basic)

    # statut de la requête
    status_code = r.status_code
    content = r.content
    if (status_code == 200):
        print("\ntest {0} OK".format(route))
        #print("content:\n",content)
    else:
        print("\ntest {0} NOK".format(route))


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

r = requests.post('http://localhost:8000/predict_dl', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route predict_dl authentifié OK")
    print("content:\n",content)
else:
    print("\ntest route predict_dl authentifié NOK")
    print(status_code)
    print("content:\n",content)


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

r = requests.post('http://localhost:8000/predict_dl', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl avec un texte trop court OK")
    print("content:\n",content)
else:
    print("\ntest route predict_dl avec un texte trop court NOK")
    print(status_code)
    print("content:\n",content)


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

r = requests.post('http://localhost:8000/predict_dl', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl erreur dans la détection de la langue du texte OK")
    print("content:\n",content)
else:
    print("\ntest route predict_dl erreur dans la détection de la langue du texte NOK")
    print(status_code)
    print("content:\n",content)


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

r = requests.post('http://localhost:8000/predict_dl', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 400):
    print("\ntest route predict_dl erreur dans la détection d un objet dans l image OK")
    print("content:\n",content)
else:
    print("\ntest route predict_dl erreur dans la détection d un objet dans l image NOK")
    print(status_code)
    print("content:\n",content)



#########################################
#partie admin ingénieur Machine Learning 
#########################################

headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46NGRtMU4=',
}

r = requests.get('http://localhost:8000/login_admin', headers=headers)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route login_admin OK")
    print("content:\n",content)
else:
    print("\ntest route login_admin NOK")


files = {
    'file_weights': open('./tu_weights.hdf5', 'rb'),
}

r = requests.post('http://localhost:8000/download_new_NN_weights', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 200):
    print("\ntest route download_new_NN_weights authentifié OK")
    print("content:\n",content)
else:
    print("\ntest route download_new_NN_weights authentifié NOK")
    print(status_code)
    print("content:\n",content)

headers = {
    'accept': 'application/json',
    'Authorization': 'Basic YWRtaW46NGRtMU4=',
    # requests won't add a boundary if this header is set when you pass files=
    # 'Content-Type': 'multipart/form-data',
}

files = {
    'file_weights': open('./console.jpg', 'rb'),
}

r = requests.post('http://localhost:8000/download_new_NN_weights', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 409):
    print("\ntest route download_new_NN_weights format incorrect non hdf5 rejeté OK")
    print("content:\n",content)
else:
    print("\ntest route download_new_NN_weights format incorrect non hdf5 NOK")
    print(status_code)
    print("content:\n",content)



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

r = requests.post('http://localhost:8000/predict_dl', headers=headers, files=files)
# statut de la requête
status_code = r.status_code
content = r.content
if (status_code == 401):
    print("\ntest route predict_dl avec user admin non autorisé OK")
    print("content:\n",content)
else:
    print("\ntest route predict_dl avec user admin non autorisé NOK")
    print(status_code)
    print("content:\n",content)
