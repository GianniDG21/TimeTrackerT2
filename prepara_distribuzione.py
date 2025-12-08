"""
TimeTrackerT2 v2.0 - Preparazione Distribuzione Vergine
Pulisce i dati personali e prepara la versione per distribuzione
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

class DistributionPreparer:
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.backup_dir = self.app_dir / "backup_data_personali"
        self.version = "2.0"
        
        # Dati di esempio per la distribuzione
        self.sample_sessions = [
            {
                "id": 1,
                "user": "Demo",
                "materia": "Python",
                "durata": 25,
                "timestamp": "2024-12-08 09:00:00"
            },
            {
                "id": 2,
                "user": "Demo", 
                "materia": "JavaScript",
                "durata": 30,
                "timestamp": "2024-12-08 14:30:00"
            }
        ]
        
        self.sample_subjects = {
            "Demo": ["Python", "JavaScript", "GoLang", "React", "Database"]
        }
        
    def backup_personal_data(self):
        """Backup dei dati personali prima della pulizia"""
        print("💾 Backup dati personali...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        self.backup_dir.mkdir()
        
        files_to_backup = ['sessions.json', 'subjects.json', 'users.txt']
        
        for filename in files_to_backup:
            source = self.app_dir / filename
            if source.exists():
                dest = self.backup_dir / f"{filename}.backup"
                shutil.copy2(source, dest)
                print(f"✅ Backup: {filename}")
        
        print(f"📁 Backup salvato in: {self.backup_dir}")
    
    def create_clean_data(self):
        """Crea dati puliti per la distribuzione"""
        print("\n🧹 Creazione dati vergini...")
        
        # Sessions.json con dati di esempio
        sessions_path = self.app_dir / "sessions.json"
        with open(sessions_path, 'w', encoding='utf-8') as f:
            json.dump(self.sample_sessions, f, indent=2, ensure_ascii=False)
        print("✅ sessions.json - dati di esempio")
        
        # Subjects.json con materie di esempio
        subjects_path = self.app_dir / "subjects.json"
        with open(subjects_path, 'w', encoding='utf-8') as f:
            json.dump(self.sample_subjects, f, indent=2, ensure_ascii=False)
        print("✅ subjects.json - materie di esempio")
        
        # Users.txt generico
        users_path = self.app_dir / "users.txt"
        with open(users_path, 'w', encoding='utf-8') as f:
            f.write("Demo\n")
        print("✅ users.txt - utente demo")
    
    def update_version_info(self):
        """Aggiorna le informazioni di versione"""
        print("\n🔢 Aggiornamento versione a 2.0...")
        
        # Aggiorna main_gui.py
        main_gui_path = self.app_dir / "main_gui.py"
        if main_gui_path.exists():
            content = main_gui_path.read_text(encoding='utf-8')
            content = content.replace("v1.1.0", f"v{self.version}")
            content = content.replace("TimeTrackerT - v1.1.0 GUI (Portable)", f"TimeTrackerT v{self.version} - Portable Edition")
            main_gui_path.write_text(content, encoding='utf-8')
            print("✅ main_gui.py aggiornato")
    
    def check_auto_py_to_exe(self):
        """Verifica se auto-py-to-exe è installato"""
        try:
            subprocess.run([sys.executable, "-m", "auto_py_to_exe", "--version"], 
                         capture_output=True, check=True)
            return True
        except:
            return False
    
    def install_auto_py_to_exe(self):
        """Installa auto-py-to-exe"""
        print("📦 Installazione auto-py-to-exe...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "auto-py-to-exe"], 
                         check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore installando auto-py-to-exe: {e}")
            return False
    
    def create_build_config(self):
        """Crea configurazione per auto-py-to-exe"""
        config = {
            "version": "auto-py-to-exe-configuration_v1.0",
            "pyinstallerOptions": [
                {
                    "optionDest": "onefile",
                    "value": True
                },
                {
                    "optionDest": "console",
                    "value": False
                },
                {
                    "optionDest": "icon_file",
                    "value": str(self.app_dir / "icon.ico") if (self.app_dir / "icon.ico").exists() else ""
                },
                {
                    "optionDest": "name",
                    "value": f"TimeTrackerT2_v{self.version}"
                },
                {
                    "optionDest": "ascii",
                    "value": False
                },
                {
                    "optionDest": "clean_build",
                    "value": True
                },
                {
                    "optionDest": "strip",
                    "value": False
                },
                {
                    "optionDest": "noupx",
                    "value": False
                }
            ],
            "nonPyinstallerOptions": {
                "increaseRecursionLimit": True,
                "manualArguments": "--hidden-import=customtkinter --hidden-import=pygame --hidden-import=termcolor --hidden-import=tkinter --collect-data=customtkinter"
            }
        }
        
        config_path = self.app_dir / "build_config.json"
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        return config_path
    
    def create_build_instructions(self):
        """Crea istruzioni per la build"""
        instructions = f"""# 🚀 TimeTrackerT2 v{self.version} - Istruzioni Build

## 📋 Preparazione Completata!

### ✅ Operazioni Eseguite:
- 💾 Backup dati personali in `backup_data_personali/`
- 🧹 Dati vergini creati con esempi
- 🔢 Versione aggiornata a {self.version}
- 📦 Auto-py-to-exe configurato

### 🔧 Build Eseguibile:

#### Metodo 1: Auto-py-to-exe GUI (Consigliato)
```bash
# Avvia l'interfaccia grafica
python -m auto_py_to_exe

# Configurazione consigliata:
- Script Location: main_gui.py
- One File: ✅ (Checked)
- Console Window: ❌ (Unchecked) 
- Icon: icon.ico (se presente)
- Additional Files: Nessuno (tutto integrato)
- Advanced Options:
  - Hidden Imports: customtkinter,pygame,termcolor,tkinter
  - Name: TimeTrackerT2_v{self.version}
```

#### Metodo 2: PyInstaller Diretto
```bash
pyinstaller --onefile --windowed --name="TimeTrackerT2_v{self.version}" --hidden-import=customtkinter --hidden-import=pygame --hidden-import=tkinter main_gui.py
```

### 📁 File Risultante:
- `dist/TimeTrackerT2_v{self.version}.exe` - Eseguibile finale
- Dimensione stimata: ~80-120 MB
- Avvio: Doppio click, nessuna installazione richiesta

### 🎯 Caratteristiche Distribuzione:
- ✅ Singolo file eseguibile
- ✅ Nessuna installazione Python richiesta
- ✅ Dati di esempio inclusi
- ✅ User-friendly per tutti
- ✅ Portable al 100%

### 🔄 Ripristino Dati Personali:
Per ripristinare i tuoi dati dopo la build:
```bash
python ripristina_dati_personali.py
```

### 📦 Distribuzione:
L'eseguibile finale può essere distribuito così com'è!
Non servono file aggiuntivi o installazioni.
"""
        
        instructions_path = self.app_dir / "ISTRUZIONI_BUILD.md"
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions)
        
        print(f"📖 Istruzioni create: {instructions_path}")
    
    def create_restore_script(self):
        """Crea script per ripristinare i dati personali"""
        restore_script = f'''"""
Ripristino Dati Personali - TimeTrackerT2
Ripristina i dati personali dopo la preparazione distribuzione
"""

import shutil
from pathlib import Path

def restore_personal_data():
    app_dir = Path(__file__).parent
    backup_dir = app_dir / "backup_data_personali"
    
    if not backup_dir.exists():
        print("❌ Backup non trovato!")
        return False
    
    print("🔄 Ripristino dati personali...")
    
    files_to_restore = [
        ('sessions.json.backup', 'sessions.json'),
        ('subjects.json.backup', 'subjects.json'), 
        ('users.txt.backup', 'users.txt')
    ]
    
    for backup_file, target_file in files_to_restore:
        backup_path = backup_dir / backup_file
        target_path = app_dir / target_file
        
        if backup_path.exists():
            shutil.copy2(backup_path, target_path)
            print(f"✅ Ripristinato: {{target_file}}")
        else:
            print(f"⚠️  Backup non trovato: {{backup_file}}")
    
    print("🎉 Ripristino completato!")
    return True

if __name__ == "__main__":
    restore_personal_data()
    input("Premi Enter per uscire...")
'''
        
        restore_path = self.app_dir / "ripristina_dati_personali.py"
        with open(restore_path, 'w', encoding='utf-8') as f:
            f.write(restore_script)
        
        print(f"🔄 Script ripristino creato: {restore_path}")
    
    def prepare_distribution(self):
        """Prepara la distribuzione completa"""
        print("🎁 TimeTrackerT2 v2.0 - Preparazione Distribuzione Vergine")
        print("=" * 60)
        
        # 1. Backup dati personali
        self.backup_personal_data()
        
        # 2. Crea dati puliti
        self.create_clean_data()
        
        # 3. Aggiorna versione
        self.update_version_info()
        
        # 4. Verifica/installa auto-py-to-exe
        if not self.check_auto_py_to_exe():
            print("\n📦 Auto-py-to-exe non trovato, installazione...")
            if not self.install_auto_py_to_exe():
                print("❌ Errore installando auto-py-to-exe")
                return False
        
        print("✅ Auto-py-to-exe disponibile")
        
        # 5. Crea configurazione build
        config_path = self.create_build_config()
        print(f"✅ Configurazione build: {config_path}")
        
        # 6. Crea istruzioni e script di ripristino
        self.create_build_instructions()
        self.create_restore_script()
        
        print("\n" + "=" * 60)
        print("🎉 PREPARAZIONE DISTRIBUZIONE COMPLETATA!")
        print("=" * 60)
        print()
        print(f"📍 PROSSIMI PASSI:")
        print(f"   1. Esegui: python -m auto_py_to_exe")
        print(f"   2. Carica: main_gui.py come script")
        print(f"   3. Seleziona: One File + No Console")
        print(f"   4. Build: Ottieni TimeTrackerT2_v{self.version}.exe")
        print()
        print(f"📁 Il tuo backup è in: backup_data_personali/")
        print(f"📖 Leggi: ISTRUZIONI_BUILD.md per dettagli")
        
        return True

def main():
    preparer = DistributionPreparer()
    
    print("⚠️  ATTENZIONE: Questa operazione sostituirà i tuoi dati attuali con dati di esempio!")
    print("I tuoi dati saranno salvati in backup.")
    
    response = input("\nContinuare? (s/n): ")
    if response.lower() not in ['s', 'y', 'si', 'yes']:
        print("Operazione annullata.")
        return
    
    if preparer.prepare_distribution():
        print("\n✨ Versione vergine 2.0 pronta per la distribuzione!")
        
        # Chiedi se avviare auto-py-to-exe
        response = input("\nVuoi avviare auto-py-to-exe ora? (s/n): ")
        if response.lower() in ['s', 'y', 'si', 'yes']:
            print("🚀 Avvio auto-py-to-exe...")
            try:
                subprocess.run([sys.executable, "-m", "auto_py_to_exe"])
            except Exception as e:
                print(f"❌ Errore avviando auto-py-to-exe: {e}")
    else:
        print("❌ Preparazione fallita!")
    
    input("\nPremi Enter per uscire...")

if __name__ == "__main__":
    main()