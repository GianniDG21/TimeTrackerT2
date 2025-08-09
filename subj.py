#subj.py

import time
import user
import dataM
import main

subjects_list = {user.act_user: []}


def add_subject():
    subject = input("Inserisci il nome della materia: ")
    if subject not in subjects_list[user.act_user]:
        subjects_list[user.act_user].append(subject)
        dataM.save_subjects(subjects_list)
        print(f"Materia '{subject}' aggiunta con successo.")
    else:
        print(f"La materia '{subject}' esiste già per l'utente {user.act_user}.")
    main.menu()  # Torna al menu principale dopo l'aggiunta

def remove_subject():
    subject = input("Inserisci il nome della materia da rimuovere: ")
    if subject in subjects_list[user.act_user]:
        subjects_list[user.act_user].remove(subject)
        dataM.save_subjects(subjects_list)
        print(f"Materia '{subject}' rimossa con successo.")
    else:
        print(f"La materia '{subject}' non esiste per l'utente {user.act_user}.")

def list_subjects():
    print("Materie disponibili:")
    for subject in subjects_list[user.act_user]:
        print(f"- {subject}")
    if not subjects_list[user.act_user]:
        print("Nessuna materia disponibile per l'utente corrente.")
    time.sleep(2)  # Pausa per la visualizzazione
    main.menu()  # Torna al menu principale dopo la visualizzazione

def manage_subjects():  #Funzione da associare al menu
        print("\nGestione Materie:")
        print("1. Aggiungi Materia")
        print("2. Rimuovi Materia")
        print("3. Elenca Materie")
        print("4. Esci")
        choice = input("Scegli un'opzione: ")

        match choice:
            case '1':
                add_subject()
            case '2':
                remove_subject()
            case '3':
                list_subjects()
            case '4':
                main.quit()
            case _:
                print("Opzione non valida, riprova.")