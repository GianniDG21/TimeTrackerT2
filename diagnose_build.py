"""
Diagnosi Build TimeTrackerT2
Verifica problemi e rilancia build se necessario
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_dependencies():
    """Verifica dipendenze per il build"""
    print("🔍 Verifica dipendenze build...")
    
    required = ['pyinstaller', 'auto-py-to-exe']
    missing = []
    
    for dep in required:
        try:
            importlib.util.find_spec(dep.replace('-', '_'))
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - MANCANTE")
            missing.append(dep)
    
    if missing:
        print(f"\n📦 Installazione dipendenze mancanti...")
        for dep in missing:
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', dep], check=True)
                print(f"✅ {dep} installato")
            except subprocess.CalledProcessError:
                print(f"❌ Errore installando {dep}")
                return False
    
    return True

def clean_build_dirs():
    """Pulisce directory di build precedenti"""
    print("\n🧹 Pulizia directory build...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"✅ Pulito {dir_name}/")
    
    # Rimuovi file spec precedenti
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"✅ Rimosso {spec_file}")

def create_simple_build():
    """Crea build semplice con PyInstaller"""
    print("\n🚀 Avvio build PyInstaller...")
    
    # Comando PyInstaller ottimizzato
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--onefile',                    # File unico
        '--windowed',                   # Senza console
        '--name=TimeTrackerT2_v2.0',   # Nome eseguibile
        '--distpath=release',           # Directory output
        '--workpath=build_temp',        # Directory temporanea
        '--specpath=.',                 # File spec nella root
        '--add-data=subjects.json;.',   # Includi file dati
        '--hidden-import=customtkinter',
        '--hidden-import=pygame',
        '--hidden-import=tkinter',
        '--hidden-import=PIL',
        '--collect-all=customtkinter',
        'main_gui.py'                   # File principale
    ]
    
    print(f"🔧 Comando: {' '.join(cmd[:5])} ...")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Build completato con successo!")
        
        # Verifica output
        exe_path = Path('release') / 'TimeTrackerT2_v2.0.exe'
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"📦 File creato: {exe_path} ({size_mb:.1f} MB)")
            return True
        else:
            print("❌ File .exe non trovato dopo build")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Errore build: {e}")
        print(f"📝 Output: {e.stdout}")
        print(f"📝 Errori: {e.stderr}")
        return False

def main():
    print("🔧 DIAGNOSI E BUILD TIMETRACKERT2")
    print("=" * 50)
    
    # 1. Verifica e installa dipendenze
    if not check_dependencies():
        print("❌ Impossibile risolvere dipendenze")
        input("Premi Enter per uscire...")
        return False
    
    # 2. Pulisci build precedenti  
    clean_build_dirs()
    
    # 3. Esegui build
    if create_simple_build():
        print("\n" + "=" * 50)
        print("🎉 BUILD COMPLETATO!")
        print("=" * 50)
        print()
        print("📁 Il tuo file si trova in:")
        print("   📦 release/TimeTrackerT2_v2.0.exe")
        print()
        print("🚀 Puoi ora distribuire questo file singolo!")
        print("   • Non richiede installazione")  
        print("   • Non richiede Python")
        print("   • Completamente portable")
        
        input("\nPremi Enter per aprire cartella release...")
        
        # Apri cartella release
        try:
            os.startfile('release')
        except:
            pass
            
        return True
    else:
        print("\n❌ Build fallito!")
        print("\n🔧 Soluzioni possibili:")
        print("   1. Verifica che main_gui.py sia presente")
        print("   2. Installa: pip install pyinstaller auto-py-to-exe")
        print("   3. Esegui come amministratore")
        print("   4. Controlla antivirus (potrebbe bloccare)")
        
        input("Premi Enter per uscire...")
        return False

if __name__ == "__main__":
    main()