import math 
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from connexion import login

CITIESFILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json", "listCities.json")
TOURSFILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "json", "listTours.json")

def distanceBetween2cities(v1, v2):
    lat1 = math.radians(v1[1])
    long1 = math.radians(v1[2])
    lat2 = math.radians(v2[1])
    long2 = math.radians(v2[2])
    return 6378.197 * math.acos(math.sin(lat1) * math.sin(lat2) + math.cos(lat1) * math.cos(lat2) * math.cos(long2 - long1))

def nearestNeighbor(startCity, listCities, visited):
    i = 0
    minimum = 1000000
    nn = ""
    while i < len(listCities):
        if listCities[i][0] in visited:
            i += 1
        else:
            if distanceBetween2cities(startCity, listCities[i]) < minimum:
                minimum = distanceBetween2cities(startCity, listCities[i])
                nn = listCities[i]
            i += 1
    return nn, minimum

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
    return visited, totalDistance

def loadCities():
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
    return groupedCities, notgroupedcities

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
    return listHotelCities

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

def saveTour(visited, totalDistance):
    #ask if user wants to save the tour
    save = input("Do you want to save this tour? (yes/no) : ")
    if save != "yes":
        return

    #ask visibility
    visibility = input("Public or private? (public/private) : ")

    #load existing tours
    try:
        with open(TOURSFILE, "r", encoding='utf-8') as f:
            tours = json.load(f)
    except FileNotFoundError:
        tours = []

    #find user entry or create it
    userEntry = None
    for user in tours:
        if user["pseudo"] == login.currentUser:
            userEntry = user
            break
    if userEntry is None:
        userEntry = {"pseudo": login.currentUser, "tours": []}
        tours.append(userEntry)

    #create and append the new tour
    newTour = {
        "id": len(userEntry["tours"]) + 1,
        "villes": visited,
        "distance": round(totalDistance, 2),
        "visibility": visibility
    }
    userEntry["tours"].append(newTour)

    with open(TOURSFILE, "w", encoding='utf-8') as f:
        json.dump(tours, f, indent=4)

    print("Tour saved successfully")

def loadCitiesInFiles():
    data = loadCities()
    #find connected user
    user = next((u for u in data if u["pseudo"] == login.currentUser), None)
    if user is None:
        print("User not found")
        return
    #convert to [name, lat, long] format
    cities = [[v["nom"], v["lat"], v["long"]] for v in user["villes"]]
    if len(cities) < 2:
        print("Not enough cities to calculate a route")
        return

    startCity = cities[0]
    #group cities and find hotels
    citiesGrouped, citiesNotGrouped = groupCities(cities)
    hotelCitiesList = findHotelCity(citiesGrouped, cities) + citiesNotGrouped

    #generate the tour
    path, totalDistance = findPath(startCity, hotelCitiesList, citiesGrouped, cities)

    #display the tour
    hotelSet = set(hotelCitiesList)
    for element in path:
        if element in hotelSet:
            print(f"{element} (Hotel)")
        else:
            print(element)
    print(f"Total distance = {round(totalDistance, 2)} km")

    #save the tour
    saveTour(path, totalDistance)

if __name__ == "__main__":
    loadCitiesInFiles()