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
    timer_script.avvia_timer(materia, int(durata))
    dataM.save_session(user.act_user, materia, int(durata))
    print("Sessione completata!")
    print(f"Vuoi fare una pausa? (s/n)")
    risposta = input().strip().lower()
    if risposta == "s":
        risposta = input("Di quanto tempo?")
        durata_pausa = int(risposta)
        timer_script.avvia_timer("PAUSA", durata_pausa)
        dataM.save_session(user.act_user, "PAUSA", durata_pausa)
    else:
        print("Nessuna pausa programmata.")
    time.sleep(2)  # Pausa per la visualizzazione


def start():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    print(f"Ok {user.act_user}, iniziamo una nuova sessione")
    materie_utente = dataM.load_subjects(user.act_user)
    print("Materie disponibili:")
    if materie_utente:
        for subject in materie_utente:
            print(f"- {subject}")
    materia = input("Scegli la materia per la sessione: ")
    if materia in materie_utente:
        print(f"Hai scelto la materia: {materia}")
        durata = input("Inserisci la durata della sessione (in minuti): ")
        start_session(materia, durata)
    else:
        print("Materia non trovata, riprova.")
        print("Prova ad aggiungere la materia dal menu principale.")
        time.sleep(2)

