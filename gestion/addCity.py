from dotenv import load_dotenv
import os
import requests
import json
from connexion import login

load_dotenv()

apiKey = os.getenv("API_Key")

CITIES_FILE = "json/listCities.json"


def getCityCoords(ville):
    # Call Google Geocoding API to get latitude and longitude of the city
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
    # Load the cities list from the JSON file
    with open(CITIES_FILE, "r", encoding='utf-8') as f:
        return json.load(f)


def saveCities(data):
    # Save the updated cities list to the JSON file
    with open(CITIES_FILE, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def isCityPresent(villes, ville):
    # Check if a city already exists in the list (case-insensitive)
    return any(v["nom"].lower() == ville.lower() for v in villes)


def getUserEntry(data, pseudo):
    # Find the user entry matching the pseudo, or create a new one
    userEntry = next((element for element in data if element.get("pseudo") == pseudo), None)
    if userEntry is None:
        userEntry = {"pseudo": pseudo, "villes": []}
        data.append(userEntry)
    return userEntry


def addCity(ville):
    # Get coordinates from the API
    coords = getCityCoords(ville)
    data = loadCities()
    userEntry = getUserEntry(data, login.currentUser)
    # Prevent adding a duplicate city
    if isCityPresent(userEntry["villes"], ville):
        print("This city is already in the list")
    else:
        userEntry["villes"].append(coords)
        saveCities(data)
        print(f"{ville} added to your list")
        return userEntry["villes"]
