import json
import sys
sys.path.append(".")
from connexion import login

def deleteCity():
    ville = input("Enter city name to delete : ")
    #loading json
    with open("json/listCities.json", "r") as f:
        cities = json.load(f)
    #verification of logged user
    for user in cities :
        if user["pseudo"] == login.currentUser:
            newCities = []
            #create a new list by removing the selected city
            for element in user["villes"]:
                if element["nom"].lower() != ville.lower() : 
                    newCities.append(element)
            #if old list equals new list
            if len(newCities) == len(user["villes"]):
                print("City not found")
            #add new list to correct place in the json
            else : 
                user["villes"] = newCities
                print("City was delete")
    #update json
    with open("json/listCities.json", "w") as f:
        json.dump(cities, f)