import time
import os
from termcolor import colored
from datetime import datetime

if os.name == 'nt':
    import msvcrt

def avvia_timer(materia, durata_minuti):
    secondi_totali = durata_minuti * 60
    secondi_trascorsi = 0
    timer_paused = False
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        larghezza_terminale = os.get_terminal_size().columns
        print(colored(materia.center(larghezza_terminale), 'cyan', attrs=['bold']))
        print("-" * larghezza_terminale)
        
        # Comandi mostrati una sola volta all'inizio
        comandi = "[p] Pausa/Riprendi | [q] Esci"
        print(colored(comandi.center(larghezza_terminale), 'white'))
        print("-" * larghezza_terminale)

        start_time = time.time()
        while secondi_totali > 0:
            minuti, secondi = divmod(secondi_totali, 60)
            tempo_formattato = f"{minuti:02d}:{secondi:02d}"
            
            # Mostra timer e stato, senza ripetere i comandi
            stato = "IN PAUSA" if timer_paused else "IN CORSO"
            display = f"{tempo_formattato} [{stato}]"
            print(colored(display.center(larghezza_terminale), 'white'), end='\r')
            
            # Gestione input
            if os.name == 'nt':  # Windows
                if msvcrt.kbhit():
                    key = msvcrt.getch().decode('utf-8').lower()
                    if key == 'p':
                        timer_paused = not timer_paused
                        stato_msg = "Timer in pausa" if timer_paused else "Timer ripreso"
                        print(colored(f"\n{stato_msg}".center(larghezza_terminale), 'yellow'))
                    elif key == 'q':
                        raise KeyboardInterrupt

            # Aggiornamento timer solo se non in pausa
            if not timer_paused:
                time.sleep(1)
                secondi_totali -= 1
                secondi_trascorsi += 1
            else:
                time.sleep(0.1)

    except KeyboardInterrupt:
        tempo_effettivo = int(secondi_trascorsi / 60)
        print(colored(f"\nSessione interrotta. Durata effettiva: {tempo_effettivo} minuti".center(larghezza_terminale), 'red'))
        return tempo_effettivo

    tempo_effettivo = durata_minuti
    print(colored("\nIl tempo è scaduto! Ottimo lavoro!".center(larghezza_terminale), 'green', attrs=['bold']))
    return tempo_effettivo