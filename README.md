# TimeTrackerT2 v2.0

**Applicazione moderna per il tracking del tempo di studio con interfaccia CustomTkinter**

## 🚀 Avvio Rapido

### **Metodo 1: Eseguibile Portable (Raccomandato)**
```bash
# Scarica ed esegui
./release/TimeTrackerT2_v2.0.exe
```

### **Metodo 2: Codice Sorgente**
```bash
# Avvio normale
python main_gui.py

# Avvio portable
./AVVIA_GUI_PORTABLE.bat
```

## 📁 Struttura Progetto

```
TimeTrackerT2/
├── 📱 main_gui.py              # Applicazione principale GUI
├── 🔧 gui_windows.py           # Finestre secondarie
├── 🛠️ gui_utils.py             # Utilità GUI
├── 💾 dataM.py                 # Gestione dati JSON
├── 📊 sessions.json            # Dati sessioni
├── 📚 subjects.json            # Materie di studio
├── 👤 users.txt                # Utenti
├── 🔊 sounds/                  # Audio notifiche
├── 📦 release/                 # Eseguibile distribuibile
│   └── TimeTrackerT2_v2.0.exe # File finale per distribuzione
├── 📜 scripts/                 # Script di build e setup
│   ├── auto_build.py           # Build automatico
│   ├── diagnose_build.py       # Diagnosi problemi
│   └── setup_portable.py      # Setup ambiente portable
└── 📖 docs/                    # Documentazione
```

## ⚡ Caratteristiche

- ✅ **Interfaccia moderna** con CustomTkinter
- ✅ **Timer Pomodoro** con pausa/ripresa
- ✅ **Gestione materie** personalizzabile
- ✅ **Storico sessioni** dettagliato
- ✅ **Audio notifiche** integrate
- ✅ **Completamente portable** 
- ✅ **Dark theme elegante** con gradienti
- ✅ **Analytics WIP** (Work In Progress)

## 🔧 Sviluppo

### **Setup Ambiente**
```bash
# Setup portable
python scripts/setup_portable.py

# Avvio sviluppo
python main_gui.py
```

### **Build Distribuzione**
```bash
# Build automatico
./BUILD_RELEASE.bat

# Build manuale
python scripts/auto_build.py
```

## 📋 Requisiti

- **Runtime**: Windows 7/8/10/11
- **Sviluppo**: Python 3.9+, CustomTkinter, Pygame
- **Build**: PyInstaller, auto-py-to-exe

## 📄 Licenza

Progetto personale - TimeTracker moderno per studenti

---
*Creato con ❤️ in Python + CustomTkinter*