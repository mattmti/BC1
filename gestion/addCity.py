from dotenv import load_dotenv
import os
import sys
import requests
import json

sys.path.insert(0, r'..')
import connexion.login as auth

load_dotenv()

apiKey = os.getenv("API_Key")
currentUser = auth.currentUser

CITIES_FILE = r'..\json\listCities.json'


def getCityCoords(ville):
    reponse = requests.get(
        url="https://maps.googleapis.com/maps/api/geocode/json",
        params={"address": ville, "key": apiKey}
    )
    data = reponse.json()
    if data["status"] == "ZERO_RESULTS":
        print(f"This city {ville} doesn't exist")
        return None
    return {
        "nom": ville,
        "lat": data["results"][0]["geometry"]["location"]["lat"],
        "long": data["results"][0]["geometry"]["location"]["lng"]
    }


def loadCities():
    with open(CITIES_FILE, "r", encoding='utf-8') as f:
        return json.load(f)


def saveCities(data):
    with open(CITIES_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)

            



def isCityPresent(villes, ville):
    return any(v["nom"].lower() == ville.lower() for v in villes)


def addCity(ville):
    coords = getCityCoords(ville)
    data = loadCities()
    userEntry = getUserEntry(data, currentUser)
    if isCityPresent(userEntry["villes"], ville):
        print("This city is already in the list")
    else:
        userEntry["villes"].append(coords)
        saveCities(data)
        print(f"{ville} added to your list")
        return userEntry["villes"]


def getUserEntry(data, pseudo):
    userEntry=next((element for element in data if element.get("pseudo")==pseudo), None)
    if userEntry==None:
        userEntry = {"pseudo": pseudo, "villes": []}
        data.append(userEntry)
    return userEntry





ville = input("Enter the name of the city: ")
addCity(ville)
