#!/usr/bin/env python3
"""
Build Script Ultra-Semplificato per macOS - TimeTrackerT2 v2.0
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🍎 Build macOS ultra-semplificato...")
    
    # Verifica che main_gui.py esista
    if not Path("main_gui.py").exists():
        print("❌ main_gui.py non trovato")
        sys.exit(1)
    
    # Crea directory release
    Path("release").mkdir(exist_ok=True)
    
    # PyInstaller comando minimo
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',
        '--windowed', 
        '--name=TimeTrackerT2_v2.0',
        '--distpath=release',
        'main_gui.py'
    ]
    
    print(f"Comando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ Build completata!")
        
        exe_path = Path("release/TimeTrackerT2_v2.0")
        if exe_path.exists():
            print(f"📦 Eseguibile: {exe_path}")
        else:
            print("❌ Eseguibile non trovato")
            sys.exit(1)
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()