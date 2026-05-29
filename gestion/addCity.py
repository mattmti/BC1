from dotenv import load_dotenv
import os
import requests
import json


load_dotenv()


API_Key= os.getenv("API_Key")

resultat=[]

ville=input("entrez nom de ville : ")

def getVilles(ville):
    villePresente=False
    reponse=requests.get(url="https://maps.googleapis.com/maps/api/geocode/json", params={"address": ville, "key":API_Key})
    data=reponse.json()
    if data["status"]=="ZERO_RESULTS":
        print(f"la ville ", ville ,"n'existe pas")
    elif data["status"]=="OK":
        coordonées={
            ###"pseudo": currentUser,
            "nom": ville,
            "lat": data["results"][0]["geometry"]["location"]["lat"],
            "long": data["results"][0]["geometry"]["location"]["lng"]
            }
    with open('..\json\listCities.json', "r", encoding='utf-8') as fichier:
        resultat = json.load(fichier)
        
        
    '''print(data["status"])
    print(data)'''  
    
    for element in resultat:
        if element["nom"].lower()== ville.lower():
            villePresente=True
            break
    
    if villePresente==True:
        print("La ville est déja presente dans la liste")
    else:
        resultat.append(coordonées)
        with open(r'..\json\listCities.json', 'w') as fichier:
            json.dump(resultat, fichier, indent=4)
        return(resultat)
    
        
        
print(getVilles(ville))
