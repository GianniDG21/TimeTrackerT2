#subj.py

import time
import user
import dataM


def get_subjects():
    """Load or initialize subjects list"""
    try:
        loaded_subjects = dataM.load_subjects(user.act_user)
        if loaded_subjects is None:
            return {user.act_user: []}
        return loaded_subjects
    except Exception as e:
        print(f"Error loading subjects: {e}")
        return {user.act_user: []}


# Initialize global subjects list
subjects_list = get_subjects()


def add_subject():
    subject = input("Inserisci il nome della materia: ")
    if subject not in subjects_list[user.act_user]:
        subjects_list[user.act_user].append(subject)
        dataM.save_subjects(subjects_list)
        print(f"Materia '{subject}' aggiunta con successo.")
        return
    else:
        print(f"La materia '{subject}' esiste già per l'utente {user.act_user}.")
        return


def remove_subject():
    global subjects_list
    subjects_list = get_subjects()  # Refresh the list
    print("\nMaterie disponibili:")
    if user.act_user in subjects_list:
        for subject in subjects_list[user.act_user]:
            print(f"- {subject}")
    if not subjects_list.get(user.act_user, []):
        print("Nessuna materia disponibile per l'utente corrente.")
    print(f"Utente attuale: {user.act_user}")
    time.sleep(2)
    subject = input("Inserisci il nome della materia da rimuovere: ")
    if subject in subjects_list[user.act_user]:
        subjects_list[user.act_user].remove(subject)
        dataM.save_subjects(subjects_list)
        print(f"Materia '{subject}' rimossa con successo.")
        return
    else:
        print(f"La materia '{subject}' non esiste per l'utente {user.act_user}.")
        return


def list_subjects():
    global subjects_list
    subjects_list = get_subjects()  # Refresh the list
    print("\nMaterie disponibili:")
    if user.act_user in subjects_list:
        for subject in subjects_list[user.act_user]:
            print(f"- {subject}")
    if not subjects_list.get(user.act_user, []):
        print("Nessuna materia disponibile per l'utente corrente.")
    print(f"Utente attuale: {user.act_user}")
    time.sleep(2)
    manage_subjects()  # Return to menu instead of exiting


def manage_subjects():  # Funzione da associare al menu
    while True:  # Keep menu active
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
                print("Uscita dalla gestione materie.")
                return
            case _:
                print("Opzione non valida, riprova.")
        time.sleep(1)