import subprocess
import sys
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time

class AdvancedRestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.debounce_timer = None
        self.ignored_paths = {
            '__pycache__',
            '.git', 
            'node_modules',
            'build',
            'dist',
            '.pytest_cache'
        }
        self.start_app()
    
    def should_ignore(self, path):
        """Controlla se il path deve essere ignorato"""
        return any(ignored in path for ignored in self.ignored_paths)
    
    def start_app(self):
        """Avvia l'app con output migliorato"""
        if self.process:
            print("🔄 Terminando processo precedente...")
            self.process.terminate()
            self.process.wait(timeout=5)
        
        print("🚀 Avviando TimeTrackerT2...")
        print("💡 Usa F5 nell'app per reload rapido senza restart!")
        
        # Avvia con buffer di output
        self.process = subprocess.Popen(
            [sys.executable, "main_gui.py"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
    
    def on_modified(self, event):
        if event.is_directory or self.should_ignore(event.src_path):
            return
            
        # Solo file Python e JSON
        if not event.src_path.endswith(('.py', '.json')):
            return
        
        file_name = os.path.basename(event.src_path)
        print(f"📝 Modificato: {file_name}")
        
        # Debounce: aspetta 1 secondo per evitare restart multipli
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        self.debounce_timer = threading.Timer(1.0, self.start_app)
        self.debounce_timer.start()

if __name__ == "__main__":
    import threading
    
    print("🔥 Dev Server Avanzato per TimeTrackerT2")
    print("📁 Monitoring:", os.getcwd())
    print("⚡ Auto-restart su modifiche file .py e .json")
    print("🎯 Usa F5 nell'app per reload veloce!")
    print("🛑 Ctrl+C per fermare")
    print("-" * 50)
    
    handler = AdvancedRestartHandler()
    observer = Observer()
    observer.schedule(handler, ".", recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Fermando dev server...")
        observer.stop()
        if handler.process:
            handler.process.terminate()
        print("✅ Dev server fermato!")
    
    observer.join()