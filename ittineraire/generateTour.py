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

    # We add the startCity because we need to go back to it at the end of the tour
    totalDistance += distanceBetween2cities(currentCity, startCity)
    visited.append(startCity[0])
    
    for city in visited:
        print(city)

    print(f"Distance totale = {totalDistance}")

def loadCities():
    # Load and return the list of cities from the JSON file
    with open(CITIESFILE, "r", encoding='utf-8') as f:
        return json.load(f)




def groupCities(listCities):
    groupedCities = []
    notgroupedcities = []
    for i in range(len(listCities)):
        newList = [listCities[i][0]]
        for j in range(len(listCities)):
            if listCities[i] != listCities[j]:
                if distanceBetween2cities(listCities[i], listCities[j]) <= 50:
                    newList.append(listCities[j][0])
        if len(newList) >= 2 and not any(set(newList) == set(existing) for existing in groupedCities):
            groupedCities.append(newList)
        elif len(newList) == 1:
            notgroupedcities.append(listCities[i][0])

    return(groupedCities, notgroupedcities)


citiesGrouped, citiesNotGrouped = (groupCities(citiesList))


def findHotelCity(listGroupedCities, listCities):
    listHotelCities = []
    for i in range(len(listGroupedCities)):
        minimum = 1000000
        hotelCity = ""
        for j in range(len(listGroupedCities[i])):
            sum = 0
            for k in range(len(listGroupedCities[i])):
                if listGroupedCities[i][j] != listGroupedCities[i][k]:
                    ville1 = None
                    ville2 = None
                    for element in listCities:
                        if element[0] == listGroupedCities[i][j]:
                            ville1 = element
                        elif element[0] == listGroupedCities[i][k]:
                            ville2 = element
                    if ville1 and ville2:
                        sum += distanceBetween2cities(ville1, ville2)
        if sum < minimum:
            minimum = sum
            hotelCity = listGroupedCities[i][j]
        listHotelCities.append(hotelCity)
    
    return(listHotelCities)

hotelCitiesList = findHotelCity(citiesGrouped, citiesList) + citiesNotGrouped

#print(citiesGrouped)
#print(hotelCitiesList)



def distanceInGroupedCities(listGroupedCities, listHotelCities, listCities):
    totalDistance = 0
    for i in range(len(listGroupedCities)):
        hotelCity = listHotelCities[i]
        for j in range(len(listGroupedCities[i])):
            if listGroupedCities[i][j] != hotelCity:
                ville1 = None
                ville2 = None
                for element in listCities:
                    if element[0] == hotelCity:
                        ville1 = element
                    elif element[0] == listGroupedCities[i][j]:
                        ville2 = element
                if ville1 and ville2:
                    totalDistance += distanceBetween2cities(ville1, ville2) * 2

    return totalDistance

#print(distanceInGroupedCities(citiesGrouped, hotelCitiesList, citiesList))


def getCoords(city, listCities):
    for element in listCities:
        if element[0] == city:
            return element


def findPath(startCity, listHotelCities, listGroupedCities, listCities):
    totalDistance = 0
    currentCity = startCity
    visitedForTravel = [startCity[0]]
    visitedCities = [startCity[0]]
    visitedSights = set([startCity[0]])

    def getGroup(cityName):
        for group in listGroupedCities:
            if cityName in group:
                return group
        return None

    def processGroup(city):
        nonlocal totalDistance, currentCity
        group = getGroup(city[0])
        if group is None:
            return
        for memberName in group:
            if memberName not in visitedSights and memberName != city[0]:
                memberCity = getCoords(memberName, listCities)
                if memberCity:
                    dist = distanceBetween2cities(currentCity, memberCity)
                    totalDistance += dist
                    visitedCities.append(memberName)
                    visitedSights.add(memberName)
                    visitedForTravel.append(memberName)

                    dist_back = distanceBetween2cities(memberCity, city)
                    totalDistance += dist_back
                    visitedCities.append(city[0])
                    currentCity = city

    processGroup(currentCity)

    remainingHotels = [city for city in listHotelCities if city not in visitedSights]

    while remainingHotels:
        minimum = 1000000
        nextHotelCity = None
        for hotelName in remainingHotels:
            hotelCoords = getCoords(hotelName, listCities)
            if hotelCoords:
                dist = distanceBetween2cities(currentCity, hotelCoords)
                if dist < minimum:
                    minimum = dist
                    nextHotelCity = hotelCoords

        if nextHotelCity is None:
            break

        totalDistance += minimum
        currentCity = nextHotelCity
        visitedCities.append(currentCity[0])
        visitedSights.add(currentCity[0])
        visitedForTravel.append(currentCity[0])
        remainingHotels.remove(currentCity[0])

        processGroup(currentCity)

    dist_home = distanceBetween2cities(currentCity, startCity)
    totalDistance += dist_home
    visitedCities.append(startCity[0])

    return visitedCities, totalDistance

path, totalDistance = findPath(start, hotelCitiesList, citiesGrouped, citiesList)

hotelSet = set(hotelCitiesList)

for element in path:
    if element in hotelSet:
        print(f"{element} (Hôtel)")
    else:
        print(element)

#print(f"Distance totale = {totalDistance}km")

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
