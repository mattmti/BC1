import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import login

CITIES_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json", "listCities.json")


def deleteCity():
    ville = input("Enter city name to delete : ")

    with open(CITIES_FILE, "r") as f:
        cities = json.load(f)

    for user in cities:
        if user["pseudo"] == login.currentUser:
            newCities = [e for e in user["villes"] if e["nom"].lower() != ville.lower()]

            if len(newCities) == len(user["villes"]):
                print("City not found")
            else:
                user["villes"] = newCities
                with open(CITIES_FILE, "w") as f:
                    json.dump(cities, f)
                print("City was deleted")
            return

    print(f"User '{login.currentUser}' not found")


deleteCity()
