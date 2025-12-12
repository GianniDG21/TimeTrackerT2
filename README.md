# TimeTrackerT2 v2.0

**Applicazione moderna per il tracking del tempo di studio con interfaccia CustomTkinter**

## ⚠️ DISCLAIMER IMPORTANTE

> **ATTENZIONE: Progetto Sperimentale in Fase di Sviluppo**
> 
> Il front-end del progetto e alcune sezioni del back-end sono state **create tramite Agenti AI**.
> 
> **Caratteristiche attuali (V2.0):**
> - Presenza **VOLUTA** di errori strutturali per scopi sperimentali
> - **OMISSIONE INTENZIONALE** di principi e best-practice (DRY, SOLID)
> - Architettura monolitica per test metodologici
>
> **Metriche attuali:**
> - ~5,500+ righe di codice totali
> - 18 file Python principali  
> - 3,302 righe concentrate in `gui_windows.py` (file monolitico)
>
> **Obiettivi del refactoring V3.0:**
> - 📈 Manutenibilità: +400%
> - 🧪 Testabilità: +300% 
> - 🔧 Estensibilità: +250%
> - 🐛 Debugging: +200%

## 🚀 Installazione e Avvio

### **Metodo 1: Eseguibile Portable (Consigliato)**
```bash
# Download ed esecuzione diretta
./release/TimeTrackerT2_v2.0.exe
```

### **Metodo 2: Codice Sorgente**
```bash
# Avvio standard
python main_gui.py

# Avvio portable
./AVVIA_GUI_PORTABLE.bat
```

## ✨ Funzionalità

- 🎨 **Interfaccia moderna** con CustomTkinter
- ⏱️ **Timer Pomodoro** con controlli pausa/ripresa
- 📚 **Gestione materie** completamente personalizzabile
- 📊 **Storico sessioni** con analisi dettagliate
- 🔊 **Notifiche audio** integrate
- 💼 **Versione portable** senza installazione
- 🌙 **Tema scuro** con gradienti eleganti
- 📈 **Sistema Analytics** (in sviluppo)

## 🛠️ Sviluppo

### **Configurazione Ambiente**
```bash
# Setup ambiente portable
python scripts/setup_portable.py

# Avvio modalità sviluppo
python main_gui.py
```

### **Creazione Build**
```bash
# Build automatizzato
./BUILD_RELEASE.bat

# Build manuale
python scripts/auto_build.py
```

## 📋 Requisiti di Sistema

### **Runtime**
- Windows 7/8/10/11 (64-bit)

### **Sviluppo** 
- Python 3.9+
- CustomTkinter
- Pygame
- PyInstaller / auto-py-to-exe

## 📄 Licenza

Progetto personale per sperimentazione metodologica - TimeTracker educativo

---
*Sviluppato con Python + CustomTkinter | Progetto sperimentale V2.0*