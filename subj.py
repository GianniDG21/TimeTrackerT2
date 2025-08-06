#subj.py

import user
import data

subjects_list = {user.act_user: []}


def add_subject():
    subject = input("Inserisci il nome della materia: ")
    if subject not in subjects_list[user.act_user]:
        subjects_list[user.act_user].append(subject)
        data.save_subjects(subjects_list)
        print(f"Materia '{subject}' aggiunta con successo.")
    else:
        print(f"La materia '{subject}' esiste già per l'utente {user.act_user}.")

def remove_subject():
    subject = input("Inserisci il nome della materia da rimuovere: ")
    if subject in subjects_list[user.act_user]:
        subjects_list[user.act_user].remove(subject)
        data.save_subjects(subjects_list)
        print(f"Materia '{subject}' rimossa con successo.")
    else:
        print(f"La materia '{subject}' non esiste per l'utente {user.act_user}.")

def list_subjects():
    print("Materie disponibili:")
    for subject in subjects_list[user.act_user]:
        print(f"- {subject}")

def manage_subjects():  #Funzione da associare al menu
    while True:
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
                break
            case _:
                print("Opzione non valida, riprova.")