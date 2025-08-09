#data.py
#File di managing dati
import json

#=====USER FUNCTIONS=====
def save_user(user_list):
    with open('users.txt', 'w') as f:
        for user in user_list:
            f.write(user + '\n')

def load_user():
    try:
        with open('users.txt', 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        return []
    
#=====SUBJECT FUNCTIONS=====
def save_subjects(subjects_list):
    try:
        if not subjects_list:
            print("La lista delle materie è vuota. Salvataggio annullato.")
            return
        with open('subjects.json', 'w') as f:
            json.dump(subjects_list, f)
    except Exception as e:
        print(f"Errore nel salvataggio delle materie: {e}")

def load_subjects(user):

    try:
        with open('subjects.json', 'r') as f:
            subjects = json.load(f)
            return subjects.get(user, [])
    except FileNotFoundError:
        return []
    
#=====SESSION FUNCTIONS=====
def save_session(user, materia, durata):
    session = {
        'user': user,
        'materia': materia,
        'durata': int(durata)
    }
    try:
        with open('sessions.json', 'a') as f:
            json.dump(session, f)
            f.write('\n')  # Aggiungi una nuova riga per ogni sessione
    except Exception as e:
        print(f"Errore nel salvataggio della sessione: {e}")