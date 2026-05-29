import json
import sys
sys.path.append(".")
from connexion import login

def changeVisibility():
    try:
        with open("json/listTours.json", "r", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No tours found")
        return

    #find current user's tours
    userTours = None
    for user in data:
        if user["pseudo"] == login.currentUser:
            userTours = user["tours"]
            break

    if userTours is None or len(userTours) == 0:
        print("You have no tours")
        return

    #display all tours with their id and visibility
    print("Your tours:")
    for tour in userTours:
        villes = " -> ".join(tour["villes"])
        print(f"  ID {tour['id']} | {tour['visibility']} | {villes}")

    #choose tour id
    tourId = input("Enter the tour ID to modify: ")
    if not tourId.isdigit():
        print("Invalid ID")
        return
    tourId = int(tourId)

    selectedTour = None
    for tour in userTours:
        if tour["id"] == tourId:
            selectedTour = tour
            break

    if selectedTour is None:
        print("Tour not found")
        return

    #choose new visibility
    print(f"Current visibility: {selectedTour['visibility']}")
    print("1. Public")
    print("2. Private")
    choice = input("Choice : ")

    if choice == "1":
        selectedTour["visibility"] = "public"
    elif choice == "2":
        selectedTour["visibility"] = "private"
    else:
        print("Invalid choice")
        return

    #save to JSON
    with open("json/listTours.json", "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Tour {tourId} is now {selectedTour['visibility']}")
