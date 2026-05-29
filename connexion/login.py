import json
import bcrypt
import os

currentUser = None

def save():
    #save users list to json
    with open("json/users.json","w") as f:
        json.dump(users, f)

def load():
    #load users list from json
    global users
    try:
        with open(_USERS_FILE, "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

def hashPassword(password):
    #hash password using bcrypt
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def checkPassword(password, hashed):
    #compare plain password with hashed password
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def login():
    global currentUser #global variable to store the connected user
    load()
    while True:
        alreadyAccount = input("Do you already have an account? :")
        if alreadyAccount == "yes":
            while True:
                find = False
                pseudo = input("Enter your pseudo :")
                password = input("Enter your password :")
                for element in users:
                    # Check if credentials match with JSON data
                    if pseudo == element["pseudo"] and checkPassword(password, element["password"]):
                        currentUser = pseudo
                        print("Connexion enabled")
                        find = True
                        break
                if not find:
                    print("Invalid pseudo or password")
                else:
                    break
            break

        elif alreadyAccount == "no": #no account redirect to createAccount()
            createAccount()
            break

        else:
            print("The answer must be simply yes or no.")

def createAccount():
    global users
    load()
    #ask user to choose a pseudo and password
    pseudo = input("Choose a pseudo : ")
    password = input("Choose a password : ")
    #hash the password before storing
    password = hashPassword(password)
    data = {"pseudo": pseudo, "password": password}
    users.append(data)
    save()
