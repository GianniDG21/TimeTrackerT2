#!/usr/bin/env python3
"""
Build Script Semplificato per macOS - TimeTrackerT2 v2.0
Utilizza PyInstaller per creare eseguibile macOS
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def log(message):
    """Stampa con prefisso per debug"""
    print(f"🍎 {message}")

def main():
    """Build principale per macOS"""
    
    # Directory di lavoro
    root_dir = Path(__file__).parent.parent
    release_dir = root_dir / "release" 
    
    log("Avvio build macOS...")
    log(f"Directory root: {root_dir}")
    
    # Crea directory release se non esiste
    release_dir.mkdir(exist_ok=True)
    
    # Assicura che esistano i file JSON necessari
    json_files = {
        'subjects.json': '[]',
        'sessions.json': '[]', 
        'user_config.json': '{}',
        'goals.json': '[]',
        'progress_notes.json': '{}'
    }
    
    for filename, default_content in json_files.items():
        file_path = root_dir / filename
        if not file_path.exists():
            with open(file_path, 'w') as f:
                f.write(default_content)
            log(f"Creato {filename}")
    
    # Verifica che main_gui.py esista
    main_file = root_dir / "main_gui.py"
    if not main_file.exists():
        log(f"❌ File main_gui.py non trovato in {root_dir}")
        sys.exit(1)
    
    # Comando PyInstaller semplificato
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                        # Eseguibile singolo
        '--windowed',                       # Nessuna console
        '--name=TimeTrackerT2_v2.0',       # Nome app
        f'--distpath={release_dir}',        # Directory output
        '--clean',                          # Pulizia build precedenti
        '--noconfirm',                      # Non chiedere conferma
        # Data files essenziali
        '--add-data=subjects.json:.',
        '--add-data=sessions.json:.',
        '--add-data=user_config.json:.',
        # Moduli nascosti per CustomTkinter
        '--hidden-import=customtkinter',
        '--hidden-import=pygame',
        '--collect-all=customtkinter',
        # File principale
        str(main_file)
    ]
    
    log("Esecuzione PyInstaller...")
    log(f"Comando: {' '.join(cmd)}")
    
    # Cambia directory di lavoro
    os.chdir(root_dir)
    
    # Esegui PyInstaller
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        log("✅ Build completata con successo!")
        
        # Verifica output
        app_path = release_dir / "TimeTrackerT2_v2.0"
        if app_path.exists():
            size_mb = app_path.stat().st_size / (1024 * 1024)
            log(f"📦 Eseguibile creato: {app_path}")
            log(f"📊 Dimensione: {size_mb:.1f} MB")
            
            # Se richiesto, crea anche DMG (opzionale)
            if '--dmg' in sys.argv:
                create_dmg(app_path, release_dir)
                
        else:
            log("❌ Eseguibile non trovato dopo il build")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        log(f"❌ Errore PyInstaller:")
        log(f"STDOUT: {e.stdout}")
        log(f"STDERR: {e.stderr}")
        sys.exit(1)

def create_dmg(app_path, release_dir):
    """Crea file DMG per distribuzione"""
    log("💿 Creazione file DMG...")
    
    dmg_path = release_dir / "TimeTrackerT2_v2.0_macOS.dmg"
    
    # Rimuovi DMG esistente
    if dmg_path.exists():
        dmg_path.unlink()
    
    cmd = [
        'hdiutil', 'create',
        '-volname', 'TimeTracker T2',
        '-srcfolder', str(app_path),
        '-ov', '-format', 'UDZO',
        str(dmg_path)
    ]
    
    try:
        subprocess.run(cmd, check=True)
        log(f"✅ DMG creato: {dmg_path}")
    except subprocess.CalledProcessError:
        log("⚠️ Impossibile creare DMG (hdiutil non disponibile)")

if __name__ == "__main__":
    main()