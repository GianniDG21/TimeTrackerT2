#main
#=====IMPORTS=====
import user
import sessions
import subj

version = "1.0.2"

#=====FUNCTIONS=====
def menu():
    print("Cosa vogliamo fare?\n")
    print("1. Nuova sessione") #BASE
    print("2. Storico sessioni") #Da implementare
    print("3. Analytics") #Da implementare
    print("4. Gestione materie\n")
    print("5. Impostazioni") #Da implementare
    print("6. Esci\n")
    scelta = int(input("Inserisci il numero della tua scelta: "))
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
            print("Gestione materie\n")
            subj.manage_subjects()
        case 5:
            print("Impostazioni\n") #da implementare
        case 6:
            quit()
def quit():
    print("Grazie per aver usato TimeTrackerT")
    user.last_user = user.act_user
    exit()
#=====INTRO CODICE======
print("Benvenuto in TimeTrackerT")
print(version)
print("Questa versione del codice e' esclusiva per Gianni")

menu()