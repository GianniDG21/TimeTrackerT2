# TimeTrackerT - Versione GUI 🚀

## Novità v1.1.0 - Interfaccia Grafica Elegante

TimeTrackerT è stato completamente rinnovato con un'interfaccia grafica **elegante e moderna** basata su **CustomTkinter** con **gradienti avanzati** e **colori premium**.

### 🎯 Caratteristiche Principali

#### 🖥️ **Interfaccia Ultra-Moderna**
- **Design Dark Mode Premium** con **gradienti colorati** eleganti
- **Layout responsivo** che si adatta alle dimensioni della finestra
- **Pulsanti con gradienti** (blu, verde, viola) di ultima generazione
- **Bordi luminosi** e **effetti hover** sofisticati
- **Icone emoji** per una navigazione intuitiva
- **Finestre modali** con design coerente e moderno

#### ⏱️ **Timer Avanzato**
- **Timer visuale** con display grande e chiaro
- **Barra di progresso** per monitorare l'avanzamento
- **Controlli Pausa/Stop** facilmente accessibili
- **Notifica sonora** al completamento della sessione
- **Salvataggio automatico** del tempo effettivo

#### 📚 **Gestione Materie Migliorata**
- **Interfaccia drag-and-drop** per aggiungere materie
- **Pulsanti preset** per durate comuni (15, 25, 45, 60, 90 minuti)
- **Validazione input** per evitare errori
- **Conferme di sicurezza** per le operazioni critiche

#### 📊 **Statistiche Avanzate**
- **Storico sessioni** con visualizzazione moderna
- **Statistiche in tempo reale**: sessioni totali, ore studiate, materia preferita
- **Cards organizzate** per ogni sessione
- **Filtri e ordinamenti** per una migliore visualizzazione

### 🚀 Come Avviare

#### Metodo 1: Launcher Grafico (Consigliato)
```
Doppio clic su: AVVIA_GUI.bat
```

#### Metodo 2: Direttamente da Python
```bash
python main_gui.py
```

#### Metodo 3: CLI Classica (Ancora Disponibile)
```
Doppio clic su: APRIMI.bat
```

#### Metodo 4: Test Funzionalità
```bash
python test_gui.py
```

### 🛠️ Dipendenze Installate

L'applicazione utilizza le seguenti librerie moderne:

- **CustomTkinter** - Framework GUI moderno
- **Pillow** - Gestione immagini avanzata  
- **Pygame** - Gestione audio per notifiche
- **Tkinter** - Framework GUI base (già incluso in Python)

### 📁 Struttura File

```
TimeTrackerT2/
├── main_gui.py          # 🆕 Applicazione GUI principale
├── gui_windows.py       # 🆕 Finestre secondarie GUI
├── gui_analytics.py     # 🆕 Finestra analytics e grafici
├── gui_utils.py         # 🆕 Utilità e helper GUI
├── test_gui.py          # 🆕 Test funzionalità GUI
├── AVVIA_GUI.bat       # 🆕 Launcher GUI
├── main.py             # 📟 Versione CLI (ancora disponibile)
├── timer_script.py     # ⏱️ Timer CLI originale
├── dataM.py            # 💾 Gestione dati
├── user.py             # 👤 Gestione utenti
├── sessions.py         # 📊 Gestione sessioni CLI
├── subj.py             # 📚 Gestione materie CLI
├── subjects.json       # 📄 Database materie
├── sessions.json       # 📄 Database sessioni
└── users.txt          # 📄 Database utenti
```

### 🆚 Differenze GUI vs CLI

| Caratteristica | CLI | GUI |
|----------------|-----|-----|
| **Design** | Terminale nero | Interface moderna dark |
| **Usabilità** | Comandi da tastiera | Click e interfacce intuitive |
| **Timer** | Testo colorato | Display visuale + progress bar |
| **Notifiche** | Beep terminale | Popup + suono sistema |
| **Gestione Materie** | Menu testuale | Interfaccia drag-and-drop |
| **Storico** | Lista testuale | Cards organizzate |
| **Multitasking** | Blocca terminale | Finestre indipendenti |

### 🎮 Controlli GUI

#### Timer
- **▶️ Avvia**: Inizia automaticamente alla selezione
- **⏸️ Pausa**: Pausa/riprendi il timer
- **⏹️ Stop**: Ferma e salva la sessione

#### Gestione Materie
- **➕ Aggiungi**: Campo testo + Enter o pulsante
- **🗑️ Rimuovi**: Pulsante rosso su ogni materia
- **✏️ Modifica**: (In sviluppo per versioni future)

### 🔧 Configurazioni Avanzate

#### Temi Personalizzati
```python
# In main_gui.py, linea 13-14
ctk.set_appearance_mode("dark")    # "dark" o "light" 
ctk.set_default_color_theme("blue") # "blue", "green", "dark-blue"
```

#### Durate Timer Preset
```python
# In gui_windows.py, NewSessionWindow, linea 82
durations = [15, 25, 45, 60, 90]  # Modifica questi valori
```

### 🐛 Risoluzione Problemi

#### L'applicazione non si avvia
1. Verifica che Python 3.11+ sia installato
2. Controlla che le dipendenze siano installate: `pip list`
3. Prova a eseguire: `python -c "import customtkinter; print('OK')"`

#### Errori di importazione
```bash
pip install customtkinter pillow pygame
```

#### Il timer non produce suoni
- Il sistema audio potrebbe essere disabilitato
- Pygame mixer potrebbe non essere inizializzato
- Controlla le impostazioni audio di sistema

### 🚀 Versioni Future

#### v1.2.0 - Analytics (Pronto per lo Sviluppo! 🚧)
- 📊 **Analytics personalizzabile** - Implementa le tue statistiche!
- 📅 **Calendari di studio** - Visualizza i tuoi progressi
- 🎯 **Sistema obiettivi** - Crea i tuoi traguardi  
- 📈 **Confronto performance** - Analizza la tua crescita
- 💻 **Codice base pronto** - Struttura già preparata per te!

#### v1.3.0 - Personalizzazione (Pianificata)
- 🎨 Temi personalizzati
- ⚙️ Impostazioni avanzate
- 🔔 Notifiche personalizzabili
- 🏆 Sistema achievement

### 👨‍💻 Sviluppo

**Autore**: Gianni  
**Versione CLI**: 1.0.2  
**Versione GUI**: 1.1.0  
**Data**: Dicembre 2025

### 📞 Supporto

Per problemi o suggerimenti:
1. Controlla questo README
2. Verifica la console per errori
3. Prova prima la versione CLI per verificare i dati

---

**Buono studio con TimeTrackerT! 🎓📚**