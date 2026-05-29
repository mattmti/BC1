from connexion import login
from gestion import viewList, addCity, deleteCity, deleteAll
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
        print("7. Logout")
        choice = input("Choice : ")
        if choice == "1":
            viewList.viewList()
        elif choice == "2":
            ville = input("Enter city name : ")
            addCity.addCity(ville)
        elif choice == "3":
            generateTour.loadCitiesInFiles(login.currentUser)
        elif choice == "4":
            viewMyTour.viewMyTours()
        elif choice == "5":
            deleteCity.deleteCity()
        elif choice == "6":
            deleteAll.DeleteEveryCity()
        elif choice == "7":
            login.currentUser = None
            break
        else:
            print("Invalid choice")

mainMenu()
