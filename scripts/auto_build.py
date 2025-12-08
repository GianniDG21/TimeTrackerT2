#!/usr/bin/env python3
"""
Distribuzione Automatica TimeTrackerT2 v2.0
Script completo per la preparazione e build dell'eseguibile
"""

import os
import sys
import subprocess
import shutil
import json
from pathlib import Path
from datetime import datetime

class AutoBuild:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.dist_dir = self.root_dir / "dist"
        self.build_dir = self.root_dir / "build"
        
    def log(self, message):
        """Stampa messaggio con timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def check_dependencies(self):
        """Verifica che tutte le dipendenze siano installate"""
        self.log("Verifica dipendenze...")
        
        required_packages = [
            'customtkinter',
            'pygame', 
            'auto-py-to-exe',
            'pyinstaller'
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace('-', '_'))
                self.log(f"✓ {package} installato")
            except ImportError:
                missing_packages.append(package)
                self.log(f"✗ {package} mancante")
                
        if missing_packages:
            self.log("Installazione dipendenze mancanti...")
            for package in missing_packages:
                subprocess.run([sys.executable, '-m', 'pip', 'install', package], 
                             check=True)
                self.log(f"✓ {package} installato")
                
    def clean_build_dirs(self):
        """Pulisce directory di build precedenti"""
        self.log("Pulizia directory di build...")
        
        for directory in [self.dist_dir, self.build_dir]:
            if directory.exists():
                shutil.rmtree(directory)
                self.log(f"✓ Rimossa {directory}")
                
    def prepare_virgin_version(self):
        """Prepara la versione vergine senza dati personali"""
        self.log("Preparazione versione vergine...")
        
        # Pulisce i file di dati
        data_files = [
            'sessions.json',
            'subjects.json', 
            'users.txt',
            'data/sessions.json'
        ]
        
        for file_path in data_files:
            full_path = self.root_dir / file_path
            if full_path.exists():
                # Crea backup
                backup_path = full_path.with_suffix(full_path.suffix + '.bak')
                shutil.copy2(full_path, backup_path)
                self.log(f"✓ Backup creato: {backup_path}")
                
                # Resetta il file
                if file_path.endswith('.json'):
                    if 'sessions' in file_path:
                        with open(full_path, 'w') as f:
                            json.dump([], f)
                    elif 'subjects' in file_path:
                        with open(full_path, 'w') as f:
                            json.dump(['Matematica', 'Italiano', 'Inglese'], f)
                else:  # users.txt
                    with open(full_path, 'w') as f:
                        f.write('Utente Demo\n')
                        
                self.log(f"✓ File pulito: {file_path}")
                
    def create_spec_file(self):
        """Crea file .spec per PyInstaller con configurazione ottimizzata"""
        self.log("Creazione file .spec...")
        
        spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sounds', 'sounds'),
        ('sessions.json', '.'),
        ('subjects.json', '.'),
        ('users.txt', '.'),
        ('data', 'data'),
    ],
    hiddenimports=[
        'customtkinter',
        'pygame',
        'tkinter',
        'tkinter.ttk',
        'threading',
        'json',
        'datetime',
        'pathlib',
        'PIL',
        'PIL._tkinter_finder'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'scipy',
        'pandas'
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TimeTrackerT2_v2.0',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
        
        spec_path = self.root_dir / "TimeTrackerT2.spec"
        with open(spec_path, 'w', encoding='utf-8') as f:
            f.write(spec_content)
            
        self.log(f"✓ File .spec creato: {spec_path}")
        return spec_path
        
    def build_executable(self, spec_path):
        """Costruisce l'eseguibile usando PyInstaller"""
        self.log("Avvio build eseguibile...")
        
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            '--noconfirm', 
            str(spec_path)
        ]
        
        self.log(f"Comando: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, cwd=self.root_dir, 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.log("✓ Build completata con successo!")
                
                # Trova l'eseguibile
                exe_path = self.dist_dir / "TimeTrackerT2_v2.0.exe"
                if exe_path.exists():
                    size_mb = exe_path.stat().st_size / (1024 * 1024)
                    self.log(f"✓ Eseguibile creato: {exe_path}")
                    self.log(f"✓ Dimensione: {size_mb:.1f} MB")
                    return exe_path
                else:
                    self.log("✗ Eseguibile non trovato!")
                    return None
            else:
                self.log("✗ Errore durante la build!")
                self.log(f"STDOUT: {result.stdout}")
                self.log(f"STDERR: {result.stderr}")
                return None
                
        except Exception as e:
            self.log(f"✗ Errore: {e}")
            return None
            
    def create_release_package(self, exe_path):
        """Crea il pacchetto finale di rilascio"""
        self.log("Creazione pacchetto di rilascio...")
        
        release_dir = self.root_dir / "release"
        if release_dir.exists():
            shutil.rmtree(release_dir)
        release_dir.mkdir()
        
        # Copia eseguibile
        release_exe = release_dir / "TimeTrackerT2_v2.0.exe"
        shutil.copy2(exe_path, release_exe)
        
        # Crea README per la release
        readme_content = """# TimeTrackerT2 v2.0 - Portable Edition

## Installazione
1. Scarica TimeTrackerT2_v2.0.exe
2. Esegui il file - nessuna installazione richiesta!
3. L'applicazione creerà automaticamente i file necessari

## Caratteristiche
- ✅ Interfaccia moderna e elegante
- ✅ Timer con pausa/ripresa
- ✅ Gestione materie di studio
- ✅ Storico sessioni
- ✅ Audio notifiche
- ✅ Completamente portable
- ✅ Nessuna installazione richiesta

## Requisiti di Sistema
- Windows 7/8/10/11 (x64)
- Nessuna dipendenza aggiuntiva

## Supporto
Per problemi o suggerimenti, apri una issue su GitHub.

---
Creato con ❤️ in Python + CustomTkinter
"""
        
        readme_path = release_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        self.log(f"✓ Pacchetto creato in: {release_dir}")
        self.log(f"✓ Eseguibile: {release_exe}")
        self.log(f"✓ README: {readme_path}")
        
        return release_dir
        
    def restore_backups(self):
        """Ripristina i file originali dai backup"""
        self.log("Ripristino file originali...")
        
        backup_files = list(self.root_dir.glob("*.bak"))
        for backup_file in backup_files:
            original_file = backup_file.with_suffix('')
            shutil.copy2(backup_file, original_file)
            backup_file.unlink()
            self.log(f"✓ Ripristinato: {original_file}")
            
    def run(self):
        """Esegue l'intero processo di build"""
        self.log("=== AVVIO BUILD TIMETRACKERT2 V2.0 ===")
        
        try:
            # 1. Verifica dipendenze
            self.check_dependencies()
            
            # 2. Pulisce build precedenti
            self.clean_build_dirs()
            
            # 3. Prepara versione vergine
            self.prepare_virgin_version()
            
            # 4. Crea file .spec
            spec_path = self.create_spec_file()
            
            # 5. Build eseguibile
            exe_path = self.build_executable(spec_path)
            
            if exe_path:
                # 6. Crea pacchetto finale
                release_dir = self.create_release_package(exe_path)
                
                self.log("=== BUILD COMPLETATA CON SUCCESSO! ===")
                self.log(f"📦 Pacchetto: {release_dir}")
                self.log("🚀 Pronto per la distribuzione!")
            else:
                self.log("=== BUILD FALLITA! ===")
                
        except Exception as e:
            self.log(f"=== ERRORE CRITICO: {e} ===")
            
        finally:
            # 7. Ripristina file originali
            self.restore_backups()
            
        self.log("=== PROCESSO TERMINATO ===")

if __name__ == "__main__":
    builder = AutoBuild()
    builder.run()