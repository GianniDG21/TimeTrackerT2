"""
TimeTrackerT2 Portable Setup
Configura automaticamente l'ambiente portable con tutte le dipendenze
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

class PortableSetup:
    def __init__(self):
        self.app_dir = Path(__file__).parent
        self.portable_python = None
        self.required_packages = [
            'customtkinter',
            'pygame',
            'termcolor',
            'pywin32'
        ]
    
    def check_python_portable(self):
        """Verifica se Python portable è disponibile"""
        possible_paths = [
            self.app_dir / "python" / "python.exe",
            self.app_dir / "portable_python" / "python.exe",
            self.app_dir / "Python39" / "python.exe",
            self.app_dir / "Python310" / "python.exe",
            self.app_dir / "Python311" / "python.exe",
            self.app_dir / "Python312" / "python.exe"
        ]
        
        for path in possible_paths:
            if path.exists():
                self.portable_python = str(path)
                return True
        return False
    
    def use_system_python(self):
        """Usa Python di sistema se disponibile"""
        self.portable_python = sys.executable
        return True
    
    def check_package(self, package_name):
        """Verifica se un package è installato"""
        try:
            spec = importlib.util.find_spec(package_name)
            return spec is not None
        except ImportError:
            return False
    
    def install_package(self, package_name):
        """Installa un package usando pip"""
        try:
            cmd = [self.portable_python, "-m", "pip", "install", package_name, "--user"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Errore installando {package_name}: {e.stderr}")
            return False
        except Exception as e:
            print(f"❌ Errore generico installando {package_name}: {str(e)}")
            return False
    
    def setup_environment(self):
        """Configura l'ambiente portable"""
        print("🚀 TimeTrackerT2 - Setup Portable")
        print("=" * 50)
        
        # 1. Trova Python
        if not self.check_python_portable():
            print("📦 Python portable non trovato, uso Python di sistema...")
            if not self.use_system_python():
                print("❌ Python non disponibile!")
                return False
        
        print(f"✅ Python trovato: {self.portable_python}")
        
        # 2. Verifica e installa dipendenze
        print("\n📚 Verifica dipendenze...")
        missing_packages = []
        
        for package in self.required_packages:
            if self.check_package(package):
                print(f"✅ {package}")
            else:
                print(f"❌ {package} - MANCANTE")
                missing_packages.append(package)
        
        # 3. Installa dipendenze mancanti
        if missing_packages:
            print(f"\n🔧 Installazione di {len(missing_packages)} package mancanti...")
            
            for package in missing_packages:
                print(f"📦 Installando {package}...")
                if self.install_package(package):
                    print(f"✅ {package} installato con successo")
                else:
                    print(f"❌ Errore installando {package}")
                    return False
        
        # 4. Crea file dati se non esistono
        self.setup_data_files()
        
        print("\n🎉 Setup completato con successo!")
        print("\n🚀 Puoi ora avviare TimeTrackerT2 con:")
        print("   • AVVIA_GUI_PORTABLE.bat")
        print("   • python main_gui.py")
        
        return True
    
    def setup_data_files(self):
        """Crea file dati se non esistono"""
        print("\n📊 Setup file dati...")
        
        data_files = {
            'sessions.json': '[]',
            'subjects.json': '{}',
            'users.txt': 'Gianni\n'
        }
        
        for filename, default_content in data_files.items():
            file_path = self.app_dir / filename
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(default_content)
                print(f"✅ Creato {filename}")
            else:
                print(f"✅ {filename} già presente")
    
    def create_portable_launcher(self):
        """Crea il launcher portable"""
        launcher_content = """@echo off
title TimeTrackerT2 - Portable Edition
cls
echo.
echo 🚀 TimeTrackerT2 - Avvio Portable
echo ================================
cd /d "%~dp0"

REM Trova Python
set PYTHON_EXE=
if exist "%~dp0python\\python.exe" set PYTHON_EXE=%~dp0python\\python.exe
if exist "%~dp0portable_python\\python.exe" set PYTHON_EXE=%~dp0portable_python\\python.exe
if exist "%~dp0Python39\\python.exe" set PYTHON_EXE=%~dp0Python39\\python.exe
if exist "%~dp0Python310\\python.exe" set PYTHON_EXE=%~dp0Python310\\python.exe
if exist "%~dp0Python311\\python.exe" set PYTHON_EXE=%~dp0Python311\\python.exe
if exist "%~dp0Python312\\python.exe" set PYTHON_EXE=%~dp0Python312\\python.exe

if "%PYTHON_EXE%"=="" (
    echo 📦 Usando Python di sistema...
    set PYTHON_EXE=python
)

echo ✅ Python: %PYTHON_EXE%
echo 🎯 Avviando TimeTrackerT2...
echo.

"%PYTHON_EXE%" main_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Errore nell'avvio dell'applicazione
    echo 🔧 Esegui setup_portable.py per riparare l'ambiente
    pause
)
"""
        
        launcher_path = self.app_dir / "AVVIA_GUI_PORTABLE.bat"
        with open(launcher_path, 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        print(f"✅ Launcher creato: AVVIA_GUI_PORTABLE.bat")

def main():
    setup = PortableSetup()
    
    if setup.setup_environment():
        setup.create_portable_launcher()
        
        print("\n" + "="*50)
        print("🎯 TIMETRACKERT2 - PORTABLE READY!")
        print("="*50)
        print()
        print("📁 STRUTTURA PORTABLE:")
        print("   TimeTrackerT2/")
        print("   ├── 🐍 *.py                 # App files")
        print("   ├── 📊 *.json               # Dati app")
        print("   ├── 🚀 AVVIA_GUI_PORTABLE.bat")
        print("   └── ⚙️  setup_portable.py")
        print()
        print("🔧 UTILIZZO:")
        print("   1. Copia tutta la cartella dove vuoi")
        print("   2. Esegui AVVIA_GUI_PORTABLE.bat")
        print("   3. I tuoi dati viaggiano con l'app!")
        print()
        print("💡 OPZIONE PYTHON PORTABLE:")
        print("   Scarica Python portable e mettilo in /python/")
        print("   per funzionare su PC senza Python installato")
        
        input("\nPremi Enter per continuare...")
        return True
    else:
        print("❌ Setup fallito!")
        input("Premi Enter per uscire...")
        return False

if __name__ == "__main__":
    main()