#data.py
#File di managing dati
import json
import datetime

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
    """Load subjects from file"""
    try:
        with open('subjects.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {user: []}
    except json.JSONDecodeError:
        print("Error reading subjects from file.")
        return {user: []}
    
#=====SESSION FUNCTIONS=====
def _get_next_session_id():
    """Generate next available session ID"""
    try:
        with open('sessions.json', 'r') as f:
            sessions = [json.loads(line) for line in f if line.strip()]
            if sessions:
                max_id = max(session.get('id', 0) for session in sessions)
                return max_id + 1
            return 1
    except FileNotFoundError:
        return 1
    except json.JSONDecodeError:
        print("Warning: Corrupted sessions file. Starting from ID 1")
        return 1

def save_session(user, materia, durata):
    session = {
        'id': _get_next_session_id(),
        'user': user,
        'materia': materia,
        'durata': durata,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    try:
        with open('sessions.json', 'a') as f:
            json.dump(session, f)
            f.write('\n')  # Add newline for each session
        
        # Controllo automatico obiettivi raggiuti
        try:
            _check_goals_after_session(user)
        except Exception as goal_error:
            print(f"Errore controllo obiettivi: {goal_error}")
            # Non interrompere il salvataggio se c'è un errore negli obiettivi
        
        return True
    except Exception as e:
        print(f"Errore nel salvataggio della sessione: {e}")
        return False

def _check_goals_after_session(user):
    """Controlla se ci sono obiettivi appena raggiunti dopo una sessione"""
    try:
        from goals_manager import GoalsManager
        from tkinter import messagebox
        
        goals_manager = GoalsManager()
        completed_goals = goals_manager.check_completed_goals(user)
        
        # Mostra notifiche per ogni obiettivo completato
        for goal in completed_goals:
            materia = goal['materia']
            target_time = goals_manager.format_time(goal['tempo_target_minuti'])
            intervallo = goal['intervallo']
            
            # Notifica di congratulazioni
            messagebox.showinfo(
                "Obiettivo Raggiunto!",
                f"Congratulazioni!\\n\\n"
                f"Hai completato l'obiettivo:\\n"
                f"Materia: {materia}\\n"
                f"Tempo: {target_time}\\n"
                f"Intervallo: {intervallo}\\n\\n"
                f"Continua cosi!"
            )
            
    except ImportError:
        # goals_manager non disponibile, ignora silenziosamente
        pass
    except Exception as e:
        print(f"Errore nel controllo obiettivi: {e}")

def load_sessions(user):
    """Load sessions for a specific user"""
    try:
        with open('sessions.json', 'r') as f:
            sessions = [json.loads(line) for line in f if line.strip()]
            return [session for session in sessions if session.get('user') == user]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Error reading sessions from file.")
        return []