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
        """Configura la finestra principale con stile Aero elegante"""
        self.title("⏱️ TimeTrackerT2 Pro v2.0")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Gestione chiusura sicura
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Centra la finestra
        self.center_window()
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.update_idletasks()
        width = 1200
        height = 800
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
        """Crea header con effetto glass Aero elegante"""
        self.header_frame = ctk.CTkFrame(
            self.main_frame, 
            height=120, 
            corner_radius=0,
            fg_color=("#1a237e", "#1565c0"),  # Gradient blue Aero
            border_width=2,
            border_color=("#3f51b5", "#42a5f5")
        )
        self.header_frame.pack(fill="x", padx=0, pady=0)
        self.header_frame.pack_propagate(False)
        
        # Container interno con effetto glass
        glass_frame = ctk.CTkFrame(
            self.header_frame,
            fg_color=("#e3f2fd", "#263238"),  # Glass effect colors
            corner_radius=8,
            border_width=1,
            border_color=("#90caf9", "#455a64")
        )
        glass_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Titolo principale
        title_text = f"⚡ TimeTrackerT2 Pro"
        self.title_label = ctk.CTkLabel(
            glass_frame,
            text=title_text,
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=("#ffffff", "#e3f2fd")
        )
        self.title_label.pack(pady=(10, 0))
        
        # Sottotitolo con utente
        subtitle_text = f"🚀 Benvenuto {self.current_user} - v2.0 Advanced Edition"
        self.subtitle_label = ctk.CTkLabel(
            glass_frame,
            text=subtitle_text,
            font=ctk.CTkFont(size=16, weight="normal"),
            text_color=("#bbdefb", "#90caf9")
        )
        self.subtitle_label.pack(pady=(0, 10))

    def create_menu_buttons(self):
        """Crea menu con design Aero cards elegante"""
        # Frame menu principale con gradient background
        self.menu_frame = ctk.CTkFrame(
            self.main_frame, 
            corner_radius=20,
            fg_color=("#f5f7fa", "#1a1b23"),  # Background neutro elegante
            border_width=2,
            border_color=("#e0e7ff", "#374151")
        )
        self.menu_frame.pack(fill="both", expand=True, padx=25, pady=20)
        
        # Grid layout 3x3 per migliore organizzazione
        self.menu_frame.grid_rowconfigure((0, 1, 2), weight=1)
        self.menu_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # === PRIMA RIGA - FUNZIONI PRINCIPALI ===
        
        # Card Nuova Sessione - Primaria
        self.new_session_btn = ctk.CTkButton(
            self.menu_frame,
            text="🎯 Nuova Sessione\n\nAvvia studio",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_new_session,
            height=120,
            corner_radius=18,
            fg_color=("#2563eb", "#1d4ed8"),  # Blu Aero primario
            hover_color=("#1d4ed8", "#2563eb"),
            border_width=2,
            border_color=("#60a5fa", "#93c5fd"),
            text_color=("#ffffff", "#f8fafc")
        )
        self.new_session_btn.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Card Cronometro - Azione rapida
        self.timer_btn = ctk.CTkButton(
            self.menu_frame,
            text="⏱️ Cronometro\n\nTimer libero",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_stopwatch,
            height=120,
            corner_radius=18,
            fg_color=("#dc2626", "#b91c1c"),  # Rosso elegante
            hover_color=("#b91c1c", "#dc2626"),
            border_width=2,
            border_color=("#f87171", "#fca5a5"),
            text_color=("#ffffff", "#fef2f2")
        )
        self.timer_btn.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        # Card Storico - Visualizzazione dati
        self.history_btn = ctk.CTkButton(
            self.menu_frame,
            text="📊 Storico\n\nTutte le sessioni",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_session_history,
            height=120,
            corner_radius=18,
            fg_color=("#059669", "#047857"),  # Verde professionale
            hover_color=("#047857", "#059669"),
            border_width=2,
            border_color=("#34d399", "#6ee7b7"),
            text_color=("#ffffff", "#f0fdfa")
        )
        self.history_btn.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")

        # === SECONDA RIGA - TRACCIAMENTO AVANZATO ===
        
        # Card Obiettivi - Gestione goals
        self.goals_btn = ctk.CTkButton(
            self.menu_frame,
            text="🎯 Obiettivi\n\nMete e progressi",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_goals,
            height=120,
            corner_radius=18,
            fg_color=("#d97706", "#b45309"),  # Arancione ambizioso
            hover_color=("#b45309", "#d97706"),
            border_width=2,
            border_color=("#fbbf24", "#fcd34d"),
            text_color=("#ffffff", "#fffbeb")
        )
        self.goals_btn.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        
        # Card Registro Argomenti - NUOVO
        self.notes_btn = ctk.CTkButton(
            self.menu_frame,
            text="📝 Registro Argomenti\n\nTempo per argomento",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_notes,
            height=120,
            corner_radius=18,
            fg_color=("#7c3aed", "#6d28d9"),  # Viola creativo
            hover_color=("#6d28d9", "#7c3aed"),
            border_width=2,
            border_color=("#a78bfa", "#c4b5fd"),
            text_color=("#ffffff", "#faf5ff")
        )
        self.notes_btn.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
        
        # Card Analytics - Dati avanzati  
        self.analytics_btn = ctk.CTkButton(
            self.menu_frame,
            text="📈 Analytics\n\nGrafici e statistiche",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_analytics,
            height=120,
            corner_radius=18,
            fg_color=("#be185d", "#a21caf"),  # Rosa analitico
            hover_color=("#a21caf", "#be185d"),
            border_width=2,
            border_color=("#f472b6", "#f9a8d4"),
            text_color=("#ffffff", "#fdf2f8")
        )
        self.analytics_btn.grid(row=1, column=2, padx=20, pady=20, sticky="nsew")

        # === TERZA RIGA - CONFIGURAZIONE ===
        
        # Card Gestione Materie
        self.subjects_btn = ctk.CTkButton(
            self.menu_frame,
            text="📚 Materie\n\nGestisci argomenti",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_subject_management,
            height=120,
            corner_radius=18,
            fg_color=("#0891b2", "#0e7490"),  # Cyan accademico
            hover_color=("#0e7490", "#0891b2"),
            border_width=2,
            border_color=("#22d3ee", "#67e8f9"),
            text_color=("#ffffff", "#ecfeff")
        )
        self.subjects_btn.grid(row=2, column=0, padx=20, pady=20, sticky="nsew")
        
        # Card Cambio Utente
        self.user_btn = ctk.CTkButton(
            self.menu_frame,
            text="👤 Utente\n\nCambia profilo",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_change_user,
            height=120,
            corner_radius=18,
            fg_color=("#0d9488", "#0f766e"),  # Teal user
            hover_color=("#0f766e", "#0d9488"),
            border_width=2,
            border_color=("#5eead4", "#99f6e4"),
            text_color=("#ffffff", "#f0fdfa")
        )
        self.user_btn.grid(row=2, column=1, padx=20, pady=20, sticky="nsew")
        
        # Card Impostazioni
        self.settings_btn = ctk.CTkButton(
            self.menu_frame,
            text="⚙️ Impostazioni\n\nConfigurazione",
            font=ctk.CTkFont(size=18, weight="bold"),
            command=self.show_settings,
            height=120,
            corner_radius=18,
            fg_color=("#6b7280", "#4b5563"),  # Grigio neutro
            hover_color=("#4b5563", "#6b7280"),
            border_width=2,
            border_color=("#9ca3af", "#d1d5db"),
            text_color=("#ffffff", "#f9fafb")
        )
        self.settings_btn.grid(row=2, column=2, padx=20, pady=20, sticky="nsew")

    def create_footer(self):
        """Crea footer elegante con stile glass Aero"""
        self.info_frame = ctk.CTkFrame(
            self.main_frame, 
            height=60, 
            corner_radius=0,
            fg_color=("#e0e7ff", "#1e293b"),  # Background elegante
            border_width=1,
            border_color=("#c7d2fe", "#475569")
        )
        self.info_frame.pack(fill="x", side="bottom", padx=0, pady=0)
        self.info_frame.pack_propagate(False)
        
        # Container glass interno
        glass_container = ctk.CTkFrame(
            self.info_frame,
            fg_color=("#f8fafc", "#334155"),
            corner_radius=8,
            border_width=1,
            border_color=("#cbd5e1", "#64748b")
        )
        glass_container.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Frame sinistra - Info versione
        left_frame = ctk.CTkFrame(glass_container, fg_color="transparent")
        left_frame.pack(side="left", padx=10)
        
        version_label = ctk.CTkLabel(
            left_frame,
            text="🚀 TimeTrackerT2 Pro v2.0 | Sistema Avanzato di Gestione Studio",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#4f46e5", "#8b5cf6")
        )
        version_label.pack(pady=5)
        
        # Frame centro - Status
        center_frame = ctk.CTkFrame(glass_container, fg_color="transparent") 
        center_frame.pack(side="left", expand=True, padx=20)
        
        status_label = ctk.CTkLabel(
            center_frame,
            text=f"✨ Utente Attivo: {self.current_user} | 📊 Sistema Note Argomenti Attivo",
            font=ctk.CTkFont(size=12),
            text_color=("#6b7280", "#9ca3af")
        )
        status_label.pack(pady=5)
        
        # Frame destra - Info addizionali
        right_frame = ctk.CTkFrame(glass_container, fg_color="transparent")
        right_frame.pack(side="right", padx=10)
        
        info_label = ctk.CTkLabel(
            right_frame,
            text="💡 Aero UI Design | ⚡ Performance Optimized",
            font=ctk.CTkFont(size=12),
            text_color=("#059669", "#10b981")
        )
        info_label.pack(pady=5)

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
                text="Modalita' Portable Attiva",
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
    
    def show_goals(self):
        """Mostra finestra gestione obiettivi"""
        try:
            from gui_windows import GoalsWindow
            goals_window = GoalsWindow(self)
        except Exception as e:
            messagebox.showerror("Errore Obiettivi", f"Errore apertura obiettivi: {e}")

    def show_notes(self):
        """Mostra finestra Registro Argomenti"""
        try:
            from gui_windows import NotesWindow
            notes_window = NotesWindow(self)
        except Exception as e:
            messagebox.showerror("Errore Registro Argomenti", f"Errore apertura registro: {e}")
            print(f"Traceback completo: {e}")
            import traceback
            traceback.print_exc()
        
    def show_settings(self):
        """Mostra impostazioni - WIP"""
        messagebox.showinfo("Impostazioni - WIP", "Funzionalita' in sviluppo!\nSarai tu a implementarla!")
        
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