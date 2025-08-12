#main
#=====IMPORTS=====
import user
import sessions
import subj

version = "1.0.2"

#=====FUNCTIONS=====
def menu():
    while True:
        print("Cosa vogliamo fare?\n")
        print("1. Nuova sessione") #BASE
        print("2. Storico sessioni") 
        print("3. Analytics") #Da implementare
        print("4. Gestione materie\n")
        print("5. Impostazioni") #Da implementare
        print("6. Esci\n")
        
        try:
            scelta = int(input("Inserisci il numero della tua scelta: "))
            match scelta:
                case 1:
                    print("Nuova sessione\n")
                    sessions.start()
                case 2:
                    print("Storico sessioni\n")
                    sessions.history()
                case 3:
                    print("Analytics\n") #da implementare
                case 4:
                    print("Gestione materie\n")
                    subj.manage_subjects()
                case 5:
                    print("Impostazioni\n") #da implementare
                case 6:
                    quit()
                case _:
                    print("Scelta non valida. Riprova.\n")
        except ValueError:
            print("Per favore inserisci un numero valido.\n")

def quit():
    print("Grazie per aver usato TimeTrackerT")
    user.last_user = user.act_user
    exit()

#=====INTRO CODICE======
print("Benvenuto in TimeTrackerT")
print(version)
print("Questa versione del codice e' esclusiva per Gianni")

menu()