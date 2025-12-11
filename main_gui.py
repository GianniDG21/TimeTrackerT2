"""
TimeTrackerT2 GUI v2.0 - Versione CustomTkinter (Exe Ready) 
Applicazione moderna per il tracking del tempo di studio con gestione utenti
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

try:
    from gui_windows import NewSessionWindow, SessionHistoryWindow, SubjectManagementWindow, TimerWindow, StopwatchWindow, StopwatchSubjectSelectionWindow
    from gui_utils import StatsCalculator
    import dataM
    from user_manager import UserManager
except ImportError as e:
    print(f"Errore import moduli: {e}")
    sys.exit(1)

# Configurazione CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class TimeTrackerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Inizializza pygame per i suoni
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Errore inizializzazione audio: {e}")
            
        self.setup_window()
        
        # Selezione utente all'avvio
        self.current_user = self.select_user_on_startup()
        if not self.current_user:
            self.destroy()
            return
            
        self.create_main_interface()
        
        # Verifica se siamo in modalità portable
        self.check_portable_mode()
        
    def select_user_on_startup(self):
        """Gestisce selezione utente all'avvio"""
        try:
            return UserManager.get_current_user(self)
        except Exception as e:
            messagebox.showerror(
                "Errore", 
                f"Errore nella selezione utente: {e}"
            )
            return None

    def setup_window(self):
        """Configura la finestra principale"""
        self.title("TimeTrackerT2 v2.0")
        self.geometry("900x650")
        self.minsize(800, 600)
        
        # Gestione chiusura sicura
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centra la finestra
        self.center_window()
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.update_idletasks()
        width = 800
        height = 600
        pos_x = (self.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def create_main_interface(self):
        """Crea l'interfaccia principale"""
        # Frame principale
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.pack(fill="both", expand=True)
        
        # Header con titolo
        self.create_header()
        
        # Menu principale
        self.create_menu_buttons()
        
        # Footer
        self.create_footer()
        
    def create_header(self):
        """Crea header con titolo e utente"""
        self.header_frame = ctk.CTkFrame(self.main_frame, height=100, corner_radius=0)
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Titolo con nome utente
        title_text = f"⏱️ TimeTrackerT2 v2.0 - {self.current_user}"
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text=title_text,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#ffffff", "#f8fafc")
        )
        self.title_label.pack(expand=True)

    def create_menu_buttons(self):
        """Crea menu con pulsanti principali"""
        # Frame menu
        self.menu_frame = ctk.CTkFrame(self.main_frame, corner_radius=15)
        self.menu_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Grid layout
        self.menu_frame.grid_rowconfigure((0, 1), weight=1)
        self.menu_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Pulsante Nuova Sessione
        self.new_session_btn = ctk.CTkButton(
            self.menu_frame,
            text="Nuova Sessione",
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
        
        # Pulsante Storico Sessioni
        self.history_btn = ctk.CTkButton(
            self.menu_frame,
            text="Storico Sessioni",
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
        
        # Pulsante Timer  
        self.timer_btn = ctk.CTkButton(
            self.menu_frame,
            text="Cronometro",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_stopwatch,
            height=80,
            corner_radius=15,
            fg_color=("#c2410c", "#ea580c"),
            hover_color=("#ea580c", "#f97316"),
            border_width=1,
            border_color=("#f97316", "#fb923c")
        )
        self.timer_btn.grid(row=0, column=2, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Gestione Materie
        self.subjects_btn = ctk.CTkButton(
            self.menu_frame,
            text="Gestione Materie",
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
        
        # Pulsante Cambio Utente
        self.user_btn = ctk.CTkButton(
            self.menu_frame,
            text="Cambia Utente",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.show_change_user,
            height=80,
            corner_radius=15,
            fg_color=("#0f766e", "#14b8a6"),
            hover_color=("#0d9488", "#5eead4"),
            border_width=1,
            border_color=("#5eead4", "#99f6e4")
        )
        self.user_btn.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")
        
        # Pulsante Analytics
        self.analytics_btn = ctk.CTkButton(
            self.menu_frame,
            text="Analytics\nGrafici & Statistiche",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.show_analytics,
            height=80,
            corner_radius=15,
            fg_color=("#be185d", "#ec4899"),
            hover_color=("#db2777", "#f472b6"),
            border_width=1,
            border_color=("#f472b6", "#fbbf24")
        )
        self.analytics_btn.grid(row=1, column=2, padx=15, pady=15, sticky="nsew")

    def create_footer(self):
        """Crea footer con info"""
        self.info_frame = ctk.CTkFrame(self.main_frame, height=35, corner_radius=0)
        self.info_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        self.info_frame.pack_propagate(False)
        
        # Versione
        version_label = ctk.CTkLabel(
            self.info_frame,
            text="TimeTrackerT2",
            font=ctk.CTkFont(size=10)
        )
        version_label.pack(side="left", padx=10, pady=5)

    def check_portable_mode(self):
        """Verifica modalità portable"""
        portable_indicators = [
            Path("python_portable").exists(),
            Path("portable_python").exists(), 
            any(Path(f"Python{v}").exists() for v in ['39', '310', '311', '312'])
        ]
        
        if any(portable_indicators):
            portable_label = ctk.CTkLabel(
                self.info_frame,
                text="🎒 Modalità Portable Attiva",
                font=ctk.CTkFont(size=10),
                text_color=("#4ade80", "#22c55e")
            )
            portable_label.pack(side="left", padx=(10, 0))

    # === METODI FINESTRE ===
    
    def show_new_session(self):
        """Mostra finestra nuova sessione"""
        self.new_session_window = NewSessionWindow(self)

    def show_session_history(self):
        """Mostra finestra storico sessioni"""
        self.history_window = SessionHistoryWindow(self)

    def show_stopwatch(self):
        """Mostra finestra selezione materia per cronometro"""
        self.stopwatch_selection = StopwatchSubjectSelectionWindow(self)

    def show_subject_management(self):
        """Mostra finestra gestione materie"""
        self.subjects_window = SubjectManagementWindow(self)
        
    def show_change_user(self):
        """Mostra finestra cambio utente"""
        self.change_user()
        
    def change_user(self):
        """Cambia utente corrente"""
        try:
            new_user = UserManager.get_current_user(self)
            if new_user and new_user != self.current_user:
                self.current_user = new_user
                # Aggiorna titolo
                title_text = f"⏱️ TimeTrackerT2 v2.0 - {self.current_user}"
                self.title_label.configure(text=title_text)
                messagebox.showinfo("Utente Cambiato", f"Ora stai usando: {self.current_user}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore cambio utente: {e}")

    def show_analytics(self):
        """Mostra finestra analytics"""
        try:
            from gui_windows import AnalyticsWindow
            analytics_window = AnalyticsWindow(self)
        except Exception as e:
            messagebox.showerror("Errore Analytics", f"Errore apertura analytics: {e}")

    def show_settings(self):
        """Mostra impostazioni - WIP"""
        messagebox.showinfo("Impostazioni - WIP", "🚧 Funzionalità in sviluppo!\nSarai tu a implementarla! 💻")
        
    def on_closing(self):
        """Gestisce la chiusura sicura dell'applicazione"""
        try:
            # Verifica se ci sono timer attivi
            active_timers = []
            for attr_name in dir(self):
                if 'timer_window' in attr_name.lower():
                    window = getattr(self, attr_name, None)
                    if window and hasattr(window, 'winfo_exists'):
                        try:
                            if window.winfo_exists() and hasattr(window, 'is_running') and window.is_running:
                                active_timers.append(window)
                        except:
                            pass
            
            # Se ci sono timer attivi, chiedi conferma
            if active_timers:
                response = messagebox.askyesno(
                    "Timer Attivo", 
                    "⏱️ C'è un timer attivo!\n\nSei sicuro di voler chiudere?\nIl progresso non salvato andrà perso."
                )
                if not response:
                    return  # Non chiudere
            
            # Chiudi tutte le finestre secondarie
            for attr_name in dir(self):
                if attr_name.endswith('_window'):
                    window = getattr(self, attr_name, None)
                    if window and hasattr(window, 'winfo_exists'):
                        try:
                            if window.winfo_exists():
                                window.destroy()
                        except:
                            pass
            
            # Chiudi applicazione principale
            self.destroy()
            
        except Exception as e:
            print(f"Errore durante chiusura: {e}")
            # Forza chiusura in caso di errore
            try:
                self.destroy()
            except:
                import sys
                sys.exit(0)

    def run(self):
        """Avvia l'applicazione"""
        self.mainloop()

def main():
    """Funzione principale con gestione errori robusta"""
    try:
        # Verifica preliminari
        if not APP_DIR.exists():
            messagebox.showerror("Errore", "Directory applicazione non trovata!")
            return
            
        app = TimeTrackerApp()
        if app.current_user:  # Solo se l'utente è stato selezionato
            app.run()
        else:
            print("Nessun utente selezionato, chiusura applicazione.")
            
    except KeyboardInterrupt:
        print("\nChiusura forzata da utente.")
        
    except ImportError as e:
        messagebox.showerror(
            "Errore Moduli", 
            f"Modulo mancante: {e}\n\nVerifica che tutte le dipendenze siano installate:\n- customtkinter\n- pygame"
        )
        
    except Exception as e:
        print(f"Errore critico: {e}")
        messagebox.showerror(
            "Errore Critico", 
            f"Errore nell'avvio dell'applicazione:\n\n{type(e).__name__}: {e}\n\nRiavvia l'applicazione o contatta il supporto."
        )
        
    finally:
        # Pulizia finale
        try:
            import pygame
            pygame.mixer.quit()
        except:
            pass

if __name__ == "__main__":
    main()