"""
TimeTrackerT2 - Verifica Portable
Script di verifica e diagnostica per la versione portable
"""

import os
import sys
from pathlib import Path
import subprocess

def check_portable_status():
    """Verifica lo stato dell'installazione portable"""
    
    print("🔍 TimeTrackerT2 - Verifica Portable")
    print("=" * 50)
    
    app_dir = Path(__file__).parent
    print(f"📁 Directory App: {app_dir}")
    
    # 1. Controlla file essenziali
    essential_files = [
        'main_gui.py',
        'gui_windows.py', 
        'dataM.py',
        'user.py',
        'subj.py',
        'setup_portable.py',
        'AVVIA_GUI_PORTABLE.bat'
    ]
    
    print("\n📋 File Essenziali:")
    missing_files = []
    for file in essential_files:
        if (app_dir / file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - MANCANTE")
            missing_files.append(file)
    
    # 2. Controlla file dati
    data_files = ['sessions.json', 'subjects.json', 'users.txt']
    
    print("\n📊 File Dati:")
    for file in data_files:
        path = app_dir / file
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file} ({size} bytes)")
        else:
            print(f"⚠️ {file} - Sarà creato al primo avvio")
    
    # 3. Controlla Python
    print("\n🐍 Python:")
    python_portable_paths = [
        app_dir / "python" / "python.exe",
        app_dir / "portable_python" / "python.exe"
    ]
    
    python_found = False
    for path in python_portable_paths:
        if path.exists():
            print(f"✅ Python Portable: {path}")
            python_found = True
            break
    
    if not python_found:
        try:
            result = subprocess.run([sys.executable, '--version'], 
                                  capture_output=True, text=True)
            print(f"✅ Python Sistema: {sys.executable}")
            print(f"   Versione: {result.stdout.strip()}")
        except:
            print("❌ Python non trovato!")
    
    # 4. Controlla dipendenze
    print("\n📦 Dipendenze:")
    dependencies = ['customtkinter', 'pygame', 'termcolor']
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep} - NON INSTALLATO")
    
    # 5. Test funzionalità portable
    print("\n🧪 Test Portable:")
    
    # Test working directory
    original_cwd = os.getcwd()
    os.chdir(app_dir)
    
    try:
        # Test import moduli locali
        sys.path.insert(0, str(app_dir))
        import dataM, user
        print("✅ Import moduli locali")
        
        # Test caricamento dati
        sessions = dataM.load_sessions(user.act_user)
        subjects = dataM.load_subjects(user.act_user)
        print(f"✅ Caricamento dati ({len(sessions)} sessioni)")
        
    except Exception as e:
        print(f"❌ Test moduli: {e}")
    finally:
        os.chdir(original_cwd)
    
    # 6. Riepilogo
    print("\n" + "=" * 50)
    if missing_files:
        print("❌ PROBLEMI RILEVATI:")
        for file in missing_files:
            print(f"   • File mancante: {file}")
        print("\n🔧 Risoluzione:")
        print("   1. Scarica i file mancanti")
        print("   2. Esegui: python setup_portable.py")
    else:
        print("✅ PORTABLE STATUS: OK!")
        print("🚀 Pronto per l'uso!")
        print("\n💡 Per avviare:")
        print("   • Windows: AVVIA_GUI_PORTABLE.bat")
        print("   • Manuale: python main_gui.py")
    
    print("\n📱 Modalità Portable Attiva - I tuoi dati viaggiano con te!")
    
    return len(missing_files) == 0

if __name__ == "__main__":
    try:
        is_ready = check_portable_status()
        
        print(f"\n🎯 Status: {'PRONTO' if is_ready else 'SETUP RICHIESTO'}")
        
        if not is_ready:
            response = input("\n❓ Vuoi eseguire il setup automatico? (s/n): ")
            if response.lower() in ['s', 'y', 'si', 'yes']:
                print("\n🔧 Esecuzione setup...")
                subprocess.run([sys.executable, 'setup_portable.py'])
    
    except KeyboardInterrupt:
        print("\n\n👋 Verifica interrotta dall'utente")
    except Exception as e:
        print(f"\n❌ Errore durante verifica: {e}")
    
    input("\nPremi Enter per uscire...")