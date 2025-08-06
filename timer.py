import time
import os
from termcolor import colored

def avvia_timer(materia, durata_minuti):

    secondi_totali = durata_minuti * 60

    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Ottiene la larghezza del terminale per centrare il titolo
        larghezza_terminale = os.get_terminal_size().columns
        # Stampa il titolo centrato e in grassetto
        print(colored(materia.center(larghezza_terminale), 'cyan', attrs=['bold']))
        print("-" * larghezza_terminale) # Aggiunge una linea di separazione

        while secondi_totali > 0:
            # Calcola minuti e secondi rimanenti
            minuti, secondi = divmod(secondi_totali, 60)
            
            # Formatta il tempo rimanente
            tempo_formattato = f"{minuti:02d}:{secondi:02d}"

            # Logica per il cambio di colore
            percentuale_rimanente = secondi_totali / (durata_minuti * 60)
            colore = 'white' # Colore di base
            if percentuale_rimanente < 0.5:
                colore = 'yellow' # Giallo quando si è a metà
            if percentuale_rimanente < 0.2:
                colore = 'green' # Verde quando sta per scadere

            # Stampa il timer colorato e centrato
            print(colored(tempo_formattato.center(larghezza_terminale), colore), end='\r')
            
            # Attende un secondo
            time.sleep(1)
            
            # Decrementa il tempo
            secondi_totali -= 1

    except KeyboardInterrupt:
        print("\nTimer interrotto dall'utente.")
        return # Esce dalla funzione se l'utente preme Ctrl+C

    # Messaggio di fine timer
    print(colored("\nIl tempo è scaduto! Ottimo lavoro!".center(larghezza_terminale), 'green', attrs=['bold']))

