import json
import bcrypt


def save():
    with open("json/users.json","w") as f:
        json.dump(users, f)



def load():
    global users
    try:
        with open("json/users.json", "r") as f:
            users = json.load(f)
    except FileNotFoundError:
        users = []

def hashPassword(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def checkPassword(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'),hashed.encode('utf-8'))

def login():
    global currentUser #var global pr retenir quel user est connecté
    load()
    #savoir si elle a deja un compte ou non
    while True : 
        alreadyAccount = input("Do you already have an account? :")
        if alreadyAccount == "yes" :
            while True :
                find = False
                pseudo = input("Enter your pseudo :")
                password = input("Enter your password :")
                for element in users :
                    #verif si les infos correspondent à ce qu'il y a dans la liste
                    if pseudo == element["pseudo"] and checkPassword(password, element["password"]):
                        currentUser = pseudo
                        print("Connexion réussi")
                        find = True
                        break
                if not find:
                    print("Invalid pseudo or password")
                else :
                    break
            break
        
        elif alreadyAccount == "no": #si pas de compte on redirige pr en créer un
            createAccount()
            break

        else : 
            print("The answer must be simply yes or no.")


def createAccount():
    global users
    load()
    #choix du pseudo et password
    pseudo = input("Choose a pseudo : ")
    password = input("Choose a password : ")
    #appeler hashMdp()
    password = hashPassword(password)

    data = {"pseudo" : pseudo, "password" : password}
    users.append(data)
    save()

login()