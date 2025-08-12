#new_session.py

import time
import user
import timer_script
import dataM


def start_session(materia, durata):
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"Sessione in avvio.")
    print(f"Materia: {materia}")
    print(f"Durata: {durata} minuti")
        # Il timer ora restituisce la durata effettiva
    durata_effettiva = timer_script.avvia_timer(materia, int(durata))
    
    # Salva la sessione con la durata effettiva
    if dataM.save_session(user.act_user, materia, durata_effettiva):
        print(f"Sessione salvata con successo! Durata effettiva: {durata_effettiva} minuti")
    else:
        print("Errore nel salvataggio della sessione.")
    print(f"Vuoi fare una pausa? (s/n)")
    risposta = input().strip().lower()
    if risposta == "s":
        risposta = input("Di quanto tempo?")
        durata_pausa = int(risposta)
        durata_effettiva = timer_script.avvia_timer(materia, int(durata_pausa))
    
    # Salva la sessione con la durata effettiva
        if dataM.save_session(user.act_user, materia, durata_effettiva):
            print(f"Sessione salvata con successo! Durata effettiva: {durata_effettiva} minuti")
        else:
            print("Errore nel salvataggio della sessione.")
    else:
        print("Nessuna pausa programmata.")
    time.sleep(2)  # Pausa per la visualizzazione


def start():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"Ok {user.act_user}, iniziamo una nuova sessione")
    materie_utente = dataM.load_subjects(user.act_user).get(user.act_user, [])
    print("Materie disponibili per il tuo utente:")
    if materie_utente:
        # Ensure materie_utente is a list of subjects
        if isinstance(materie_utente, dict):
            subjects = list(materie_utente.values())
        else:
            subjects = materie_utente
        for subject in subjects:
            print(f"- {subject}")
    else:
        print("Nessuna materia trovata per questo utente.")
        time.sleep(2)
        return
    materia = input("Scegli la materia per la sessione: ")
    if materia in materie_utente:
        print(f"Hai scelto la materia: {materia}")
        durata = input("Inserisci la durata della sessione (in minuti): ")
        start_session(materia, durata)
    else:
        print("Materia non trovata, riprova.")
        print("Prova ad aggiungere la materia dal menu principale.")
        time.sleep(2)

def history():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"Storico sessioni per l'utente: {user.act_user}")
    sessions = dataM.load_sessions(user.act_user)
    if sessions:
        for session in sessions:
            print(f"ID: {session['id']}, Materia: {session['materia']}, Durata: {session['durata']} minuti, Timestamp: {session['timestamp']}")
    else:
        print("Nessuna sessione trovata.")
    return