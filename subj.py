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

