#user.py

user_base="Guest"
act_user=""

user_list=[]

last_user=""

def register_user(): #COMPLETA
    global user_list
    print("Benvenuto nella registrazione utente")
    new_user = input("Inserisci il nome del nuovo utente")
    if new_user in user_list:
        reply = input("Questo utente esiste gia', vuoi fare il login? (s/n)")
        if reply == 's':
            login_user()
        else:
            print("Ritorno alla procedura di registrazine")
            register_user()
    else:
        user_list.append(new_user)
        print(f"Utente {new_user} registrato correttamente")
            

def login_user():   #PLACEHOLDER
    print("Benvenuto nel login utenti\n")
    if user_list == []:
        print("Non ci sono utenti registrati, per favore procedi alla registrazione")
        import time
        time.sleep(2)
        register_user()
    else:
        for user in user_list:
            print(user)

def user_check():   #FUNZIONE PRINCIPALE
    if last_user=="" :
        reply = input("Sembra che questo sia un primo avvio, vuoi creare un nuovo utente? (s/n)")
        if reply == 's' :
            register_user()
        else :
            print("Continueremo come account Ospite")
    else:
        print(f"L'ultimo utente e' stato {last_user}")
        reply = input(f"Vuoi proeguire come {last_user}? (s/n)")
        if reply=='s':
            act_user = last_user
        else:
            login_user()
