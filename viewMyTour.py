import json
import sys
sys.path.append(".")
from connexion import login

def viewMyTours():
    #load tours from json file
    try:
        with open("json/listTours.json", "r", encoding='utf-8') as f:
            tours = json.load(f)
    except FileNotFoundError:
        print("No tours found")
        return

    #find connected user and display his tours
    for user in tours:
        if user["pseudo"] == login.currentUser:
            if len(user["tours"]) == 0:
                print("You have no tours")
            else:
                for tour in user["tours"]:
                    print(f"Tour {tour['id']} - {tour['distance']} km - {tour['visibility']}")
                    print(" -> ".join(tour["villes"]))
            return

    print("You have no tours")