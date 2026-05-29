import json
from connexion import login

CITIES_FILE = "json/listCities.json"


def DeleteEveryCity():
    # Load the cities list from the JSON file
    with open(CITIES_FILE, "r") as f:
        cities = json.load(f)

    # Find the connected user and clear their city list
    for user in cities:
        if user["pseudo"] == login.currentUser:
            user["villes"] = []
            with open(CITIES_FILE, "w") as f:
                json.dump(cities, f)
            print(f"All cities of '{login.currentUser}' have been deleted.")
            return

    print(f"User '{login.currentUser}' not found.")
