"""
TimeTrackerT2 GUI v2.0 - Versione CustomTkinter (Exe Ready)
Applicazione moderna per il tracking del tempo di studio
Ottimizzata per compilazione PyInstaller/auto-py-to-exe
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
import pygame
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Setup per modalità exe e portable
if getattr(sys, 'frozen', False):
    # Eseguibile PyInstaller
    APP_DIR = Path(sys.executable).parent
else:
    # Codice Python normale
    APP_DIR = Path(__file__).parent

os.chdir(APP_DIR)  # Assicura che la working directory sia corretta
sys.path.insert(0, str(APP_DIR))  # Aggiungi directory app al path

# Import dei moduli esistenti con gestione errori
try:
    import user
    import dataM
    import subj
    from gui_windows import NewSessionWindow, SessionHistoryWindow, SubjectManagementWindow, TimerWindow
except ImportError as e:
    messagebox.showerror("Errore Moduli", f"Errore importando moduli: {e}\n\nEsegui setup_portable.py per riparare l'ambiente.")
    sys.exit(1)

# Configurazione CustomTkinter - Design Moderno
ctk.set_appearance_mode("dark")  # Modalità dark elegante
ctk.set_default_color_theme("blue")  # Tema blu con gradienti

class TimeTrackerApp:
    def __init__(self):
        self.app_dir = APP_DIR
        self.setup_portable_environment()
        
        self.window = ctk.CTk()
        self.window.title(f"TimeTrackerT - v1.1.0 GUI (Portable)")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # Inizializzazione pygame per i suoni
        try:
            pygame.mixer.init()
        except:
            print("Pygame mixer non disponibile. I suoni saranno disabilitati.")
        
        # Variabili per il timer
        self.timer_running = False
        self.timer_paused = False
        self.timer_thread = None
        self.total_seconds = 0
        self.elapsed_seconds = 0
        self.current_subject = ""
        
        self.setup_ui()
        
        # Centro la finestra
        self.center_window()
    
    def setup_portable_environment(self):
        """Configura l'ambiente per modalità portable"""
        # Assicura che i file di dati esistano
        data_files = {
            'sessions.json': '[]',
            'subjects.json': '{"Gianni": []}',
            'users.txt': 'Gianni\n'
        }
        
        for filename, default_content in data_files.items():
            file_path = self.app_dir / filename
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(default_content)
        
        # Configura pygame per modalità portable
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Pygame mixer non disponibile in modalità portable: {e}")
        
        # Log del setup portable
        print(f"📱 Modalità Portable attiva - Directory: {self.app_dir}")

    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia utente principale"""
        
        # Frame principale
        self.main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header con titolo e utente - Design moderno
        self.header_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=15,
            fg_color=("#1a1a2e", "#16213e"),
            border_width=1,
            border_color=("#0f3460", "#0f3460")
        )
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="⏱️ TimeTrackerT", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(side="left", padx=20, pady=15)
        
        # Info utente e modalità portable
        info_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        info_frame.pack(side="right", padx=20, pady=15)
        
        self.user_label = ctk.CTkLabel(
            info_frame, 
            text=f"👤 {user.act_user}", 
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.user_label.pack()
        
        portable_label = ctk.CTkLabel(
            info_frame, 
            text="💻 Portable Mode", 
            font=ctk.CTkFont(size=12),
            text_color=("#4ade80", "#22c55e")
        )
        portable_label.pack()
        
        # Frame per i pulsanti del menu principale - Design elegante
        self.menu_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=15,
            fg_color=("#0e1621", "#0e1621"),
            border_width=1,
            border_color=("#1a1a2e", "#1a1a2e")
        )
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Pulsanti del menu principale con icone
        self.create_menu_buttons()
        
        # Status bar - Design moderno
        self.status_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=10, 
            height=35,
            fg_color=("#1a1a2e", "#16213e"),
            border_width=1,
            border_color=("#0f3460", "#0f3460")
        )
        self.status_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text=f"📁 Portable Ready | 📱 Directory: {self.app_dir.name}", 
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=8)

    def create_menu_buttons(self):
        """Crea i pulsanti del menu principale"""
        
        # Grid layout per i pulsanti
        self.menu_frame.grid_rowconfigure((0, 1), weight=1)
        self.menu_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Pulsante Nuova Sessione - Gradient moderno
        self.new_session_btn = ctk.CTkButton(
            self.menu_frame,
            text="🚀 Nuova Sessione",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_new_session,
            height=80,
            corner_radius=15,
            fg_color=("#1f4e79", "#2563eb"),
            hover_color=("#1e40af", "#3b82f6"),
            border_width=1,
            border_color=("#3b82f6", "#60a5fa")
        )
        self.new_session_btn.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Storico Sessioni - Gradient verde
        self.history_btn = ctk.CTkButton(
            self.menu_frame,
            text="📊 Storico Sessioni",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_session_history,
            height=80,
            corner_radius=15,
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e"),
            border_width=1,
            border_color=("#22c55e", "#4ade80")
        )
        self.history_btn.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Analytics - WIP
        self.analytics_btn = ctk.CTkButton(
            self.menu_frame,
            text="📈 Analytics\n🚧 WIP",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_analytics,
            height=80,
            corner_radius=15,
            fg_color=("#404040", "#404040"),
            hover_color=("#505050", "#505050"),
            text_color=("#888888", "#888888")
        )
        self.analytics_btn.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Gestione Materie - Gradient viola
        self.subjects_btn = ctk.CTkButton(
            self.menu_frame,
            text="📚 Gestione Materie",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_subject_management,
            height=80,
            corner_radius=15,
            fg_color=("#7c2d92", "#a855f7"),
            hover_color=("#9333ea", "#c084fc"),
            border_width=1,
            border_color=("#c084fc", "#ddd6fe")
        )
        self.subjects_btn.grid(row=1, column=0, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Impostazioni - WIP
        self.settings_btn = ctk.CTkButton(
            self.menu_frame,
            text="⚙️ Impostazioni\n🚧 WIP",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_settings,
            height=80,
            corner_radius=15,
            fg_color=("#404040", "#404040"),
            hover_color=("#505050", "#505050"),
            text_color=("#888888", "#888888")
        )
        self.settings_btn.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Esci - Design elegante
        self.exit_btn = ctk.CTkButton(
            self.menu_frame,
            text="🚪 Esci",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.quit_app,
            height=80,
            corner_radius=15,
            fg_color="transparent",
            border_width=2,
            border_color=("#dc2626", "#ef4444"),
            text_color=("#dc2626", "#ef4444"),
            hover_color=("#dc2626", "#ef4444")
        )
        self.exit_btn.grid(row=1, column=2, padx=15, pady=15, sticky="nsew")

    def show_new_session(self):
        """Mostra la finestra per creare una nuova sessione"""
        self.new_session_window = NewSessionWindow(self)

    def show_session_history(self):
        """Mostra la finestra dello storico sessioni"""
        self.history_window = SessionHistoryWindow(self)

    def show_analytics(self):
        """Placeholder per Analytics - Work in Progress"""
        messagebox.showinfo("Analytics - WIP", "🚧 Funzionalità in sviluppo!\nSarai tu a implementarla! 💻")

    def show_subject_management(self):
        """Mostra la finestra di gestione materie"""
        self.subjects_window = SubjectManagementWindow(self)

    def show_settings(self):
        """Placeholder per Impostazioni - Work in Progress"""
        messagebox.showinfo("Impostazioni - WIP", "🚧 Funzionalità in sviluppo!\nPuoi implementarla quando vuoi! ⚙️")

    def quit_app(self):
        """Chiude l'applicazione"""
        if self.timer_running:
            result = messagebox.askyesno(
                "Timer in corso", 
                "C'è un timer in corso. Vuoi davvero uscire?"
            )
            if not result:
                return
        
        user.last_user = user.act_user
        self.window.quit()
        self.window.destroy()

    def update_status(self, message):
        """Aggiorna la status bar"""
        self.status_label.configure(text=message)

    def run(self):
        """Avvia l'applicazione"""
        self.window.protocol("WM_DELETE_WINDOW", self.quit_app)
        self.window.mainloop()

if __name__ == "__main__":
    app = TimeTrackerApp()
    app.run()