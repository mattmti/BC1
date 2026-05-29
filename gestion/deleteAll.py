import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from connexion import login

CITIES_FILE = os.path.join(ROOT, "json", "listCities.json")


def DeleteEveryCity():
    with open(CITIES_FILE, "r") as f:
        cities = json.load(f)

    for user in cities:
        if user["pseudo"] == login.currentUser:
            user["villes"] = []
            with open(CITIES_FILE, "w") as f:
                json.dump(cities, f)
            print(f"Toutes les villes de '{login.currentUser}' ont été supprimées.")
            return

    print(f"Utilisateur '{login.currentUser}' introuvable.")

