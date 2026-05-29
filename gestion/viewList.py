import json
import sys
sys.path.append(".")
from connexion import login

def viewList():
    #load cities from json file
    try:
        with open("json/listCities.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No cities found")
        return

    #find the connected user and display his cities
    for user in data:
        if user["pseudo"] == login.currentUser:
            if len(user["villes"]) == 0:
                print("Your city list is empty")
            else:
                #print each city name
                for ville in user["villes"]:
                    print(ville["nom"])
            return
    
    print("No cities found")