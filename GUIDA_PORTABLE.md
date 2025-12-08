# 🚀 TimeTrackerT2 - Guida Portable

## 💼 Modalità Portable Attiva!

TimeTrackerT2 è ora **completamente portable**! Puoi copiare l'intera cartella ovunque e funzionerà perfettamente.

## 🔧 Setup Iniziale (Una Volta Sola)

### Metodo Automatico (Consigliato)
```bash
# Esegui il setup automatico
python setup_portable.py
```

### Metodo Manuale
```bash
# Installa solo le dipendenze necessarie
pip install customtkinter pygame termcolor pywin32
```

## 🚀 Avvio Quotidiano

### Windows
```bash
# Doppio clic su:
AVVIA_GUI_PORTABLE.bat
```

### Alternativa Manuale
```bash
python main_gui.py
```

## 📁 Struttura Portable

```
TimeTrackerT2_Portable/
├── 🐍 main_gui.py              # App principale
├── 🪟 gui_windows.py           # Finestre GUI  
├── 🛠️ gui_utils.py             # Utilità
├── 💾 dataM.py, user.py, subj.py # Moduli core
├── 📊 sessions.json            # I tuoi dati sessioni
├── 📚 subjects.json            # Le tue materie  
├── 👤 users.txt                # Info utente
├── 🚀 AVVIA_GUI_PORTABLE.bat   # Launcher Windows
├── ⚙️ setup_portable.py        # Setup automatico
└── 📖 GUIDA_PORTABLE.md        # Questa guida
```

## 💡 Vantaggi Modalità Portable

### ✅ **Portabilità Totale**
- 📱 Copia su USB e usa ovunque
- ☁️ Sincronizza via Dropbox/OneDrive  
- 💻 Funziona su qualsiasi PC Windows
- 🔒 I tuoi dati viaggiano con te

### ✅ **Zero Installazione**
- 🚫 Non richiede installazione nel sistema
- 🔧 Setup automatico delle dipendenze
- 🐍 Supporta Python portable o di sistema
- ⚡ Avvio rapido con un click

### ✅ **Dati Locali**
- 💾 Tutti i dati nella cartella dell'app
- 🔄 Backup semplice = copia cartella
- 📈 Nessuna perdita dati spostando l'app
- 🛡️ Privacy: dati sempre con te

## 🔧 Python Portable (Opzionale)

Per funzionare su PC **senza Python installato**:

### Download Python Portable
1. **Sito ufficiale**: https://www.python.org/downloads/windows/
   - Scarica "Windows embeddable package"
   - Estrai in cartella `python/`

2. **WinPython**: https://winpython.github.io/
   - Download e installa in `python/`
   - Più completo, include molte librerie

### Struttura con Python Portable
```
TimeTrackerT2_Portable/
├── 📁 python/                  # Python portable
│   ├── python.exe
│   ├── Lib/
│   └── Scripts/
├── 🐍 *.py                     # App files
├── 📊 *.json                   # Dati
└── 🚀 AVVIA_GUI_PORTABLE.bat   # Launcher
```

## 🆘 Risoluzione Problemi

### ❌ "Python non trovato"
**Soluzioni**:
1. Installa Python di sistema: https://python.org
2. Scarica Python portable in cartella `python/`
3. Esegui `setup_portable.py`

### ❌ "Modulo non trovato"
**Soluzioni**:
```bash
python setup_portable.py
```

### ❌ "Errore permessi"
**Soluzioni**:
- Esegui come amministratore
- Sposta in cartella con permessi scrittura (es: Desktop)
- Controlla antivirus (potrebbe bloccare)

### ❌ "App non si avvia"
**Debug**:
```bash
# Esegui da terminale per vedere errori
python main_gui.py
```

## 🎯 Casi d'Uso Portable

### 🎓 **Studenti**
- 💻 Usa su PC università e casa
- 📱 Porta su chiavetta USB
- 📊 Dati sempre sincronizzati

### 💼 **Professionisti**
- 🏢 PC ufficio e casa
- ✈️ Laptop in viaggio  
- ☁️ Backup su cloud automatico

### 👥 **Condivisione**
- 📤 Invia cartella completa ad amici
- 🎁 Regalo già pronto all'uso
- 🔧 Zero setup per destinatario

## ⚙️ Personalizzazione Portable

### 🎨 Modificare Colori
Edita `main_gui.py`, cerca "fg_color" per cambiare colori gradienti.

### 📊 Backup Automatico  
I file `.json` contengono tutti i tuoi dati. Copiali regolarmente!

### 🔄 Aggiornamenti
Sostituisci solo i file `.py`, mantieni i `.json` per conservare i dati.

## 📞 Supporto Portable

**Problemi?** 
1. Esegui `python setup_portable.py`
2. Verifica tutti i file `.py` siano presenti
3. Prova `python main_gui.py` da terminale
4. Controlla che la cartella abbia permessi di scrittura

---

## 🎉 **Buon Lavoro con TimeTrackerT2 Portable!**

La tua produttività ora viaggia con te! ✈️📱💻