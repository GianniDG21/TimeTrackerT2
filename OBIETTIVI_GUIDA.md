# 🎯 Sistema Obiettivi - Guida Utente

## Panoramica
Il sistema Obiettivi ti permette di impostare target di studio per materie specifiche e monitorare il tuo progresso in tempo reale.

## Come Accedere
1. Apri TimeTrackerT2
2. Clicca sul bottone **"Obiettivi"** nel menu principale

## Creare un Nuovo Obiettivo

### Passo 1: Seleziona la Materia
- Scegli una materia dal menu a tendina
- Se non vedi le materie, vai prima in "Gestione Materie" per crearle

### Passo 2: Imposta il Tempo Target
- **Ore**: Inserisci il numero di ore (es: 2)
- **Minuti**: Inserisci i minuti aggiuntivi (es: 30 per 2h 30min)
- Minimo: 1 minuto

### Passo 3: Scegli l'Intervallo
- **Giorno**: L'obiettivo si resetta ogni giorno alle 00:00
- **Settimana**: L'obiettivo si resetta ogni Lunedì
- **Mese**: L'obiettivo si resetta il 1° di ogni mese

### Passo 4: Crea l'Obiettivo
- Clicca "Crea Obiettivo"
- Riceverai una conferma del successo

## Monitoraggio del Progresso

### Visualizzazione
- **Lista Obiettivi**: Tutti i tuoi obiettivi sono visualizzati sulla destra
- **Barra di Progresso**: Mostra visivamente quanto hai completato
- **Percentuale**: Indica il progresso numerico
- **Colori di Stato**:
  - 🔘 **Grigio**: 0-49% (Appena iniziato)
  - 🟠 **Arancione**: 50-74% (A metà strada)  
  - 🟡 **Giallo**: 75-99% (Quasi completato)
  - 🟢 **Verde**: 100%+ (Completato)

### Informazioni Visualizzate
- **Materia**: Nome della materia studiata
- **Obiettivo**: Tempo target e intervallo (es: "2h 30min / settimana")
- **Progresso**: Tempo già studiato (es: "Progresso: 1h 15min")
- **Status**: Percentuale di completamento o "COMPLETATO"

## Notifiche Automatiche

### Quando Raggiungi un Obiettivo
- Apparirà automaticamente una finestra di congratulazioni
- La notifica appare immediatamente dopo aver salvato una sessione che completa l'obiettivo
- L'obiettivo diventerà verde nella lista

### Quando Vengono Mostrate
- Dopo ogni sessione di studio salvata (manuale o cronometro)
- All'apertura della finestra Obiettivi (controllo retroattivo)

## Gestione degli Obiettivi

### Eliminare un Obiettivo
1. Trova l'obiettivo nella lista
2. Clicca il pulsante **"Elimina"** in basso a destra del widget
3. Conferma l'eliminazione

### Modifica degli Obiettivi
- Attualmente non è possibile modificare un obiettivo esistente
- Per cambiarlo: elimina quello vecchio e creane uno nuovo

## Calcolo del Progresso

### Come Funziona
- Il sistema analizza automaticamente tutte le tue sessioni di studio
- Filtra per la materia specifica dell'obiettivo
- Considera solo le sessioni nell'intervallo di tempo attuale
- Somma tutto il tempo studiato per quella materia

### Esempi Pratici

**Obiettivo Giornaliero**: 2 ore di Matematica
- Conta solo le sessioni di Matematica di oggi
- Se oggi hai studiato 1h 30min → 75% completato

**Obiettivo Settimanale**: 5 ore di Fisica  
- Conta tutte le sessioni di Fisica da Lunedì ad oggi
- Se questa settimana hai fatto 3h 45min → 75% completato

**Obiettivo Mensile**: 20 ore di Storia
- Conta tutte le sessioni di Storia dal 1° del mese ad oggi
- Se questo mese hai fatto 15 ore → 75% completato

## Consigli per l'Uso

### Obiettivi Realistici
- Inizia con obiettivi piccoli e raggiungibili
- Es: 1 ora al giorno per una materia nuova
- Aumenta gradualmente quando diventa routine

### Combinazioni Efficaci
- **Obiettivi giornalieri**: Per abitudini quotidiane (30min/giorno)
- **Obiettivi settimanali**: Per materie principali (5h/settimana)  
- **Obiettivi mensili**: Per progetti a lungo termine (20h/mese)

### Monitoraggio
- Controlla regolarmente i tuoi progressi
- La finestra Obiettivi ti dà una vista completa di tutti i target
- Usa i colori come guida visiva rapida

## Risoluzione Problemi

### "Nessuna materia disponibile"
- Vai in "Gestione Materie" e crea almeno una materia
- Riapri la finestra Obiettivi

### Il progresso non si aggiorna
- Il progresso viene calcolato in tempo reale dalle sessioni salvate
- Assicurati che le sessioni siano salvate correttamente
- Riapri la finestra Obiettivi per forzare l'aggiornamento

### Obiettivi non si completano
- Verifica che la materia dell'obiettivo corrisponda esattamente a quella delle sessioni
- Controlla che le sessioni siano nell'intervallo di tempo corretto
- Gli obiettivi giornalieri si resettano a mezzanotte

## File di Configurazione
- Gli obiettivi sono salvati in `goals.json`
- Non modificare questo file manualmente
- In caso di problemi, elimina il file e ricrea gli obiettivi

---

**💡 Suggerimento**: Usa gli obiettivi come motivazione per mantenere costanza nello studio. Celebra ogni traguardo raggiunto!