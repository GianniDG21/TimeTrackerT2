#new_session.py

import user
import subj
import data

def start(): 
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"Ok {user.act_user}, iniziamo una nuova sessione")
    materie_utente = data.load_subjects(user.act_user)
    print("Materie disponibili:")
    if materie_utente:
        # 2. Itera sulla lista che hai appena caricato
        for subject in materie_utente:
            print(f"- {subject}")
    else:
        print("Nessuna materia trovata.")