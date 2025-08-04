#user.py

user_base="Guest"
act_user=""

user_list=[]

last_user=""

def register_user()
    pass

def user_check():
    if last_user=="" :
        reply = input("Sembra che questo sia un primo avvio, vuoi creare un nuovo utente? (s/n)")
        if reply == 's' :
            register_user()
        else :
            print("Continueremo come account Ospite")
    else:
        