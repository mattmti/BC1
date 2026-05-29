import math 
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import login

# Path to the JSON file containing the list of cities
CITIESFILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json", "listCities.json")


def distanceBetween2cities(v1, v2):
    # We convert in radians
    lat1 = math.radians(v1[1])
    long1 = math.radians(v1[2])
    lat2 = math.radians(v2[1])
    long2 = math.radians(v2[2])

    # Formula for calculating the distance between two cities
    return(6378.197 * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1)))


def nearestNeighbor(startCity, listCities, visited):
    i = 0
    minimum = 1000000 # We use 1,000,000 to make sure we wouldn't run into any minimum issues
    nn = "" # nn is for nearest neighbor
    while i < len(listCities):
        # We check to see if the city has already been visited, and if so, we skip it
        if listCities[i][0] in visited:
            i += 1
        else:
            # We replace the minimum if the distance is lower 
            if distanceBetween2cities(startCity, listCities[i]) < minimum:
                minimum = distanceBetween2cities(startCity, listCities[i])
                nn = listCities[i]
            i += 1
    return(nn, minimum)


def nearestNeighborPath(startCity, listCities):
    visited = [startCity[0]]
    currentCity = startCity
    totalDistance = 0

    
    while len(listCities) > len(visited):
        nextCity, distance = nearestNeighbor(currentCity, listCities, visited)
        visited.append(nextCity[0])
        currentCity = nextCity
        totalDistance += distance

    totalDistance += distanceBetween2cities(currentCity, startCity)
    visited.append(startCity[0])
    
    for city in visited:
        print(city)

    print(f"Distance totale = {totalDistance}")

def loadCities():
    # Load and return the list of cities from the JSON file
    with open(CITIESFILE, "r", encoding='utf-8') as f:
        return json.load(f)


def loadCitiesInFiles(pseudo):
    data = loadCities()
    
    # Find the user matching the given pseudo
    user = next((u for u in data if u["pseudo"] == pseudo), None)
    if user is None:
        print(f"Pseudo '{pseudo}' not found.")
        return

    # Convert the city data to the format [name, lat, long]
    cities = [[v["nom"], v["lat"], v["long"]] for v in user["villes"]]
    
    # At least 2 cities are required to calculate a route
    if len(cities) < 2:
        print("Not enough cities to calculate a route.")
        return

    # Start the route from the first city in the list
    startCity = cities[0]
    nearestNeighborPath(startCity, cities)




if __name__ == "__main__":
    loadCitiesInFiles(login.currentUser)