#user.py

#MOMENTANEAMENTE DISATTIVATO

import dataM
global act_user
global last_user

user_base="Gianni"
act_user="Gianni"

user_list=[]

last_user="Gianni"

def register_user(): #COMPLETA
    global user_list
    print("Benvenuto nella registrazione utente")
    new_user = input("Inserisci il nome del nuovo utente ")
    if new_user in dataM.load_user():
        reply = input("Questo utente esiste gia', vuoi fare il login? (s/n)")
        if reply == 's':
            login_user()
        else:
            print("Procederemo con account Ospite")
            act_user = user_base
    else:
        user_list.append(new_user)
        dataM.save_user(user_list)
        print(f"Utente {new_user} registrato correttamente")
            

def login_user():   #COMPLETA
    print("Benvenuto nel login utenti\n")
    dataM.load_user()
    if dataM.load_user == []:
        print("Nessun utente registrato, procedo con la registrazione")
        register_user()
    else:
        for user in dataM.load_user():
            print(f"Utente registrato: {user}")
        login = input("Inserisci il nome utente per il login: ")
        if login in dataM.load_user():
            act_user = login
            print(f"Login effettuato come {act_user}")
        else:
            print("Utente non trovato, procedo con la registrazione")
            register_user()

def user_check():   #FUNZIONE PRINCIPALE
    if last_user=="" :
        reply = input("Sembra che questo sia un primo avvio, vuoi creare un nuovo utente? (s/n)")
        if reply == 's' :
            register_user()
        else :
            print("Continueremo come account Ospite")
            global act_user
            act_user = user_base
    else:
        print(f"L'ultimo utente e' stato {last_user}")
        reply = input(f"Vuoi proeguire come {last_user}? (s/n)")
        if reply=='s':
            act_user = last_user
        else:
            login_user()
