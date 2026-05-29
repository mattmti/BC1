from connexion import login
from gestion import viewList, addCity, deleteCity, deleteAll, changeVisibility
from ittineraire import generateTour
import viewMyTour
import viewTour

def mainMenu():
    while True:
        print("1. Login / Create account")
        print("2. View public tours")
        choice = input("Choice : ")
        if choice == "1":
            login.login()
            connectedMenu()
            break
        elif choice == "2":
            viewTour.viewPublicTours()
        else:
            print("Invalid choice")

def connectedMenu():
    while True:
        print("1. View my cities")
        print("2. Add a city")
        print("3. Generate a tour")
        print("4. View my tours")
        print("5. Delete a city")
        print("6. Delete all cities")
        print("7. Change tour visibility")
        print("8. Logout")
        choice = input("Choice : ")
        if choice == "1":
            viewList.viewList()
        elif choice == "2":
            while True:
                ville = input("Add one more City or no: ")
                if ville.lower() == "no":
                    break
                if not ville.replace(" ", "").isalpha():
                    print(" Invalid input: please enter letters only.")
                    continue
                ###print(f"City added: {ville}")
                addCity.addCity(ville)
        elif choice == "3":
            generateTour.loadCitiesInFiles()
        elif choice == "4":
            viewMyTour.viewMyTours()
        elif choice == "5":
            deleteCity.deleteCity()
        elif choice == "6":
            deleteAll.DeleteEveryCity()
        elif choice == "7":
            changeVisibility.changeVisibility()
        elif choice == "8":
            login.currentUser = None
            break
        else:
            print("Invalid choice")

mainMenu()
