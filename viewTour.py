import json

def viewPublicTours():
    #load tours from json file
    try:
        with open("json/listTours.json", "r", encoding='utf-8') as f:
            tours = json.load(f)
    except FileNotFoundError:
        print("No public tours found")
        return

    found = False
    #display all public tours
    for user in tours:
        for tour in user["tours"]:
            if tour["visibility"] == "public":
                print(f"{user['pseudo']} - Tour {tour['id']} - {tour['distance']} km")
                print(" -> ".join(tour["villes"]))
                found = True

    if not found:
        print("No public tours found")