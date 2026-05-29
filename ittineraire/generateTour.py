import math 


# Testing data
start = ["Tōkyō-to", 35.6768601, 139.7638947]
citiesList = [["Tōkyō-to", 35.6768601, 139.7638947],
              ["Ōsaka-shi", 34.6937569, 135.5014539],
              ["Kanazawa-shi", 36.561627, 136.6568822],
              ["Chiba-shi", 35.6070629, 140.1062653],
              ["Kyōto-shi", 35.0115754, 135.7681441]]


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

    
    while len(citiesList) > len(visited):
        nextCity, distance = nearestNeighbor(currentCity, listCities, visited)
        visited.append(nextCity[0])
        currentCity = nextCity
        totalDistance += distance

    totalDistance += distanceBetween2cities(currentCity, startCity)
    visited.append(startCity[0])
    
    for city in visited:
        print(city)

    print(f"Distance totale = {totalDistance}")


nearestNeighborPath(start, citiesList)



