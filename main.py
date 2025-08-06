#main
#=====IMPORTS=====
import user
import sessions

version = "1.0.2"

#=====FUNCTIONS=====
def menu():
    print("Cosa vogliamo fare?\n")
    print("1. Nuova sessione") #BASE
    print("2. Storico sessioni") #Da implementare
    print("3. Analytics") #Da implementare
    print("4. Aggiungi materia\n") #Da implementare
    print("5. Impostazioni") #Da implementare
    scelta = input("Inserisci il numero della tua scelta: ")
    match scelta:
        case 1:
            print("Nuova sessione\n")
            sessions.start()
        case 2:
            print("Storico sessioni\n") #da implementare
            #session.history() 
        case 3:
            print("Analytics\n") #da implementare
        case 4:
            print("Aggiungi materia\n") #da implementare
        case 5:
            print("Impostazioni\n") #da implementare
def quit():
    print("Grazie per aver usato TimeTrackerT")
    user.last_user = user.act_user
    exit()
#=====INTRO CODICE======
print("Benvenuto in TimeTrackerT")
print(version)
user.user_check()

#=====MAIN LOOP=====
menu()

scelta = input("Vuoi uscire? (s/n) ")
if scelta == 's':
    quit()
else:
    menu()