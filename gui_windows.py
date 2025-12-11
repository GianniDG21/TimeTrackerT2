"""
Finestre secondarie per TimeTrackerT GUI - Design Aero Moderno
Include: NewSessionWindow, SessionHistoryWindow, SubjectManagementWindow, TimerWindow
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import threading
import time
import pygame
from datetime import datetime

# Import dei moduli esistenti
import dataM
# import subj # Rimosso - ora gestito da dataM
# import user # Rimosso - ora gestito da user_manager
from gui_utils import StatsCalculator, UIHelpers, DataValidator


class AeroStyleMixin:
    """Mixin class per stili Aero consistenti"""
    
    @staticmethod
    def get_aero_colors():
        """Ritorna palette colori Aero standard"""
        return {
            'primary_blue': ("#2563eb", "#1d4ed8"),
            'success_green': ("#059669", "#047857"),
            'danger_red': ("#dc2626", "#b91c1c"),
            'warning_orange': ("#d97706", "#b45309"),
            'purple_creative': ("#7c3aed", "#6d28d9"),
            'pink_analytics': ("#be185d", "#a21caf"),
            'cyan_academic': ("#0891b2", "#0e7490"),
            'teal_user': ("#0d9488", "#0f766e"),
            'gray_neutral': ("#6b7280", "#4b5563"),
            'glass_bg': ("#f8fafc", "#334155"),
            'card_bg': ("#ffffff", "#1e293b"),
            'border_light': ("#e2e8f0", "#475569"),
            'text_primary': ("#1f2937", "#f8fafc"),
            'text_secondary': ("#6b7280", "#9ca3af")
        }
    
    @staticmethod
    def create_aero_header(parent, title, icon="🎯", color_key="primary_blue"):
        """Crea header Aero standardizzato"""
        colors = AeroStyleMixin.get_aero_colors()
        
        header_frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            height=80,
            fg_color=colors[color_key],
            border_width=2,
            border_color=colors['border_light']
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#ffffff", "#f8fafc")
        )
        title_label.pack(expand=True)
        
        return header_frame
    
    @staticmethod
    def create_aero_card(parent, title, icon="📋", color_key="glass_bg", width=None):
        """Crea card Aero standardizzata"""
        colors = AeroStyleMixin.get_aero_colors()
        
        # Parametri della card
        card_params = {
            'corner_radius': 16,
            'fg_color': colors['card_bg'],
            'border_width': 2,
            'border_color': colors[color_key]
        }
        
        # Aggiungi width solo se specificato
        if width is not None:
            card_params['width'] = width
        
        card_frame = ctk.CTkFrame(parent, **card_params)
        
        if width is not None:
            card_frame.pack_propagate(False)
        
        # Header della card
        card_header = ctk.CTkFrame(
            card_frame,
            corner_radius=12,
            height=50,
            fg_color=colors[color_key],
            border_width=0
        )
        card_header.pack(fill="x", padx=15, pady=(15, 10))
        card_header.pack_propagate(False)
        
        header_title = ctk.CTkLabel(
            card_header,
            text=f"{icon} {title}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#ffffff", "#f8fafc")
        )
        header_title.pack(expand=True)
        
        # Content area
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        return card_frame, content_frame
    
    def setup_aero_styling(self):
        """Configura stile Aero coerente per la finestra"""
        self.colors = self.get_aero_colors()
        
        # Applica tema scuro/chiaro globale
        if hasattr(self, 'window') and self.window:
            self.window.configure(fg_color=self.colors['glass_bg'])
            
        return self.colors

class NewSessionWindow(AeroStyleMixin):
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app)
        self.window.title("🎯 Nuova Sessione di Studio")
        self.window.geometry("700x650")
        self.window.resizable(True, True)
        self.window.minsize(650, 600)
        
        # Styling Aero coerente
        self.setup_aero_styling()
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Rende la finestra modale
        self.window.transient(main_app)
        self.window.grab_set()
        
        # Gestione chiusura sicura
        self.window.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia con design Aero moderno e scrollabile"""
        
        # Frame principale con gradient Aero
        main_frame = ctk.CTkFrame(
            self.window, 
            corner_radius=20,
            fg_color=("#f8fafc", "#1e293b"),
            border_width=2,
            border_color=("#e2e8f0", "#475569")
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header con titolo glass effect
        header_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=16,
            height=80,
            fg_color=("#e3f2fd", "#263238"),
            border_width=1,
            border_color=("#90caf9", "#455a64")
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        header_frame.grid_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎯 Nuova Sessione di Studio",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=("#1565c0", "#42a5f5")
        )
        title_label.pack(expand=True)
        
        # Scrollable frame per contenuto
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            corner_radius=16,
            fg_color=("#ffffff", "#1e293b"),
            scrollbar_fg_color=("#e2e8f0", "#475569")
        )
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # === CARD SELEZIONE MATERIA ===
        self.create_subject_card(scroll_frame)
        
        # === CARD DURATA ===
        self.create_duration_card(scroll_frame)
        
        # === CARD NOTE ARGOMENTO ===
        self.create_notes_card(scroll_frame)
        
        # === CARD AZIONI ===
        self.create_action_card(scroll_frame)
    
    def create_subject_card(self, parent):
        """Crea card per selezione materia con design Aero"""
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=("#ffffff", "#1e293b"),
            border_width=2,
            border_color=("#3b82f6", "#60a5fa")
        )
        card_frame.pack(fill="x", pady=15, padx=10)
        
        # Header card
        header = ctk.CTkFrame(
            card_frame,
            corner_radius=12,
            height=50,
            fg_color=("#3b82f6", "#1d4ed8"),
            border_width=0
        )
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="📚 Materia di Studio",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#ffffff", "#f8fafc")
        )
        title.pack(expand=True)
        
        # Content
        content = ctk.CTkFrame(card_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Carica materie
        self.load_subjects()
        
        self.subject_combo = ctk.CTkComboBox(
            content,
            values=self.subjects_list,
            font=ctk.CTkFont(size=16),
            width=400,
            height=40,
            corner_radius=12,
            border_width=2,
            border_color=("#e2e8f0", "#475569")
        )
        self.subject_combo.pack(pady=10)
        
        if self.subjects_list:
            self.subject_combo.set(self.subjects_list[0])
    
    def create_duration_card(self, parent):
        """Crea card per durata con presets Aero"""
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=("#ffffff", "#1e293b"),
            border_width=2,
            border_color=("#059669", "#10b981")
        )
        card_frame.pack(fill="x", pady=15, padx=10)
        
        # Header card
        header = ctk.CTkFrame(
            card_frame,
            corner_radius=12,
            height=50,
            fg_color=("#059669", "#047857"),
            border_width=0
        )
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="⏱️ Durata Sessione",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#ffffff", "#f0fdfa")
        )
        title.pack(expand=True)
        
        # Content
        content = ctk.CTkFrame(card_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Entry durata
        self.duration_entry = ctk.CTkEntry(
            content,
            placeholder_text="Inserisci durata in minuti",
            font=ctk.CTkFont(size=16),
            width=300,
            height=40,
            justify="center",
            corner_radius=12,
            border_width=2
        )
        self.duration_entry.pack(pady=10)
        
        # Preset buttons con design pills
        preset_label = ctk.CTkLabel(
            content,
            text="Durate rapide:",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=("#6b7280", "#9ca3af")
        )
        preset_label.pack(pady=(10, 5))
        
        preset_frame = ctk.CTkFrame(content, fg_color="transparent")
        preset_frame.pack(pady=(0, 10))
        
        durations = [15, 25, 30, 45, 60, 90]
        colors = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#3b82f6", "#8b5cf6"]
        
        for i, duration in enumerate(durations):
            btn = ctk.CTkButton(
                preset_frame,
                text=f"{duration}min",
                width=70,
                height=35,
                corner_radius=18,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color=colors[i % len(colors)],
                hover_color=colors[i % len(colors)],
                command=lambda d=duration: self.set_duration(d)
            )
            btn.pack(side="left", padx=5)
    
    def create_notes_card(self, parent):
        """Crea card per note argomento opzionali"""
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=("#ffffff", "#1e293b"),
            border_width=2,
            border_color=("#7c3aed", "#a78bfa")
        )
        card_frame.pack(fill="x", pady=15, padx=10)
        
        # Header card
        header = ctk.CTkFrame(
            card_frame,
            corner_radius=12,
            height=50,
            fg_color=("#7c3aed", "#6d28d9"),
            border_width=0
        )
        header.pack(fill="x", padx=15, pady=(15, 10))
        header.pack_propagate(False)
        
        title = ctk.CTkLabel(
            header,
            text="📝 Argomento di Studio (Opzionale)",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=("#ffffff", "#faf5ff")
        )
        title.pack(expand=True)
        
        # Content
        content = ctk.CTkFrame(card_frame, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=(0, 20))
        
        # Helper text
        helper = ctk.CTkLabel(
            content,
            text="💡 Specifica l'argomento per tracciare il tempo dedicato",
            font=ctk.CTkFont(size=12),
            text_color=("#6b7280", "#9ca3af")
        )
        helper.pack(pady=(5, 10))
        
        # Entry per note
        self.notes_entry = ctk.CTkEntry(
            content,
            placeholder_text="es. Capitolo 3 - Basi di Dati, Derivate parziali, etc.",
            font=ctk.CTkFont(size=16),
            width=500,
            height=40,
            corner_radius=12,
            border_width=2
        )
        self.notes_entry.pack(pady=5)
    
    def create_action_card(self, parent):
        """Crea card azioni con pulsanti Aero"""
        card_frame = ctk.CTkFrame(
            parent,
            corner_radius=16,
            fg_color=("#f8fafc", "#1e293b"),
            border_width=2,
            border_color=("#e2e8f0", "#475569")
        )
        card_frame.pack(fill="x", pady=15, padx=10)
        
        # Content con pulsanti
        content = ctk.CTkFrame(card_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Pulsante principale - Timer (ora principale)
        self.timer_btn = ctk.CTkButton(
            content,
            text="⏲️ Avvia con Timer",
            font=ctk.CTkFont(size=20, weight="bold"),
            width=300,
            height=60,
            corner_radius=30,
            fg_color=("#2563eb", "#1d4ed8"),
            hover_color=("#1d4ed8", "#2563eb"),
            border_width=3,
            border_color=("#60a5fa", "#93c5fd"),
            command=self.start_with_timer
        )
        self.timer_btn.pack(pady=(0, 15))
        
        # Pulsanti secondari in riga
        secondary_frame = ctk.CTkFrame(content, fg_color="transparent")
        secondary_frame.pack(fill="x", pady=(0, 10))
        
        # Registrazione manuale (ora secondaria)
        self.start_session_btn = ctk.CTkButton(
            secondary_frame,
            text="🚀 Registra Manualmente",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=140,
            height=45,
            corner_radius=22,
            fg_color=("#dc2626", "#b91c1c"),
            hover_color=("#b91c1c", "#dc2626"),
            command=self.start_session
        )
        self.start_session_btn.pack(side="left", padx=(0, 10))
        
        # Annulla
        cancel_btn = ctk.CTkButton(
            secondary_frame,
            text="❌ Annulla",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=140,
            height=45,
            corner_radius=22,
            fg_color=("#6b7280", "#4b5563"),
            hover_color=("#4b5563", "#6b7280"),
            command=self.safe_close
        )
        cancel_btn.pack(side="right")

    def load_subjects(self):
        """Carica le materie dell'utente"""
        try:
            subjects_data = dataM.load_subjects(self.main_app.current_user)
            self.subjects_list = subjects_data.get(self.main_app.current_user, [])
            
            if not self.subjects_list:
                messagebox.showwarning(
                    "Nessuna Materia", 
                    "Non hai ancora aggiunto delle materie.\nVai in 'Gestione Materie' per aggiungerne."
                )
                self.subjects_list = ["Nessuna materia disponibile"]
        except Exception as e:
            print(f"Errore nel caricamento materie: {e}")
            self.subjects_list = ["Errore nel caricamento"]

    def set_duration(self, minutes):
        """Imposta la durata usando i pulsanti preset"""
        self.duration_entry.delete(0, tk.END)
        self.duration_entry.insert(0, str(minutes))
        
    def start_with_timer(self):
        """Avvia sessione con timer integrato"""
        subject = self.subject_combo.get()
        duration_text = self.duration_entry.get().strip()
        
        # Validazione input
        if not subject or subject == "Nessuna materia disponibile":
            messagebox.showerror("Errore", "Seleziona una materia valida!")
            return
        
        if not duration_text:
            messagebox.showerror("Errore", "Inserisci la durata della sessione!")
            return
        
        try:
            duration = int(duration_text)
            if duration <= 0:
                raise ValueError("La durata deve essere positiva")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci una durata valida in minuti!")
            return
            
        # Chiudi questa finestra
        self.window.destroy()
        
        # Apri finestra timer con i dati
        timer_window = TimerWindow(self.main_app, subject, duration)

    def start_session(self):
        """Salva una sessione completata manualmente"""
        subject = self.subject_combo.get()
        duration_text = self.duration_entry.get().strip()
        note_text = self.notes_entry.get().strip()
        
        # Validazione input
        if not subject or subject == "Nessuna materia disponibile":
            messagebox.showerror("Errore", "Seleziona una materia valida!")
            return
        
        if not duration_text:
            messagebox.showerror("Errore", "Inserisci la durata della sessione!")
            return
        
        try:
            duration = int(duration_text)
            if duration <= 0:
                raise ValueError("La durata deve essere positiva")
        except ValueError:
            messagebox.showerror("Errore", "Inserisci una durata valida in minuti!")
            return
        
        # Salva sessione manuale
        try:
            success = dataM.save_session(self.main_app.current_user, subject, duration, note_text)
            
            if success:
                success_msg = f"Sessione manuale salvata!\n\nMateria: {subject}\nDurata: {duration} minuti"
                if note_text:
                    success_msg += f"\nArgomento: {note_text}"
                messagebox.showinfo("Successo", success_msg)
                self.window.destroy()
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio della sessione!")
                
        except Exception as e:
            print(f"Errore sessione manuale: {e}")
            messagebox.showerror("Errore", f"Errore nel salvataggio!\n\nDettagli: {e}")
            
    def start_manual_session(self):
        """Avvia sessione manuale (salva direttamente)"""
        self.start_session()
        
    def safe_close(self):
        """Chiude la finestra in modo sicuro"""
        try:
            self.window.destroy()
        except Exception as e:
            print(f"Errore chiusura NewSessionWindow: {e}")

class SessionHistoryWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app)
        self.window.title("� Storico Sessioni di Studio")
        self.window.geometry("1000x750")
        self.window.resizable(True, True)
        self.window.minsize(900, 650)
        
        # Setup stile Aero
        self.setup_aero_styling()
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.window.transient(main_app)
        self.window.grab_set()
        
        # Gestione chiusura sicura
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        
        self.setup_ui()
        self.center_window()
        self.load_sessions()
    
    def setup_aero_styling(self):
        """Configura stile Aero coerente"""
        self.colors = {
            'primary': ("#059669", "#047857"),
            'secondary': ("#f8fafc", "#334155"), 
            'accent': ("#10b981", "#34d399"),
            'card_bg': ("#ffffff", "#1e293b"),
            'header_bg': ("#e6fffa", "#0f2027"),
            'text_primary': ("#1f2937", "#f8fafc"),
            'text_secondary': ("#6b7280", "#9ca3af")
        }

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia"""
        
        # Frame principale
        main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="Storico Sessioni",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # Frame per le statistiche
        stats_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        stats_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Caricamento statistiche...",
            font=ctk.CTkFont(size=14)
        )
        self.stats_label.pack(pady=15)
        
        # Frame scrollabile per le sessioni
        self.sessions_frame = ctk.CTkScrollableFrame(
            main_frame, 
            corner_radius=10,
            label_text="📈 Sessioni Recenti"
        )
        self.sessions_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Pulsante chiudi
        close_btn = ctk.CTkButton(
            main_frame,
            text="✅ Chiudi",
            command=self.window.destroy,
            height=40,
            width=120
        )
        close_btn.pack(pady=(0, 15))

    def load_sessions(self):
        """Carica e mostra le sessioni"""
        try:
            sessions = dataM.load_sessions(self.main_app.current_user)
            
            if not sessions:
                no_sessions_label = ctk.CTkLabel(
                    self.sessions_frame,
                    text="Nessuna sessione trovata",
                    font=ctk.CTkFont(size=16)
                )
                no_sessions_label.pack(pady=50)
                self.stats_label.configure(text="Nessuna statistica disponibile")
                return
            
            # Calcola statistiche
            total_sessions = len(sessions)
            total_minutes = sum(s.get('durata', 0) for s in sessions)
            total_hours = total_minutes / 60
            
            # Materie più studiate
            subject_stats = {}
            for session in sessions:
                subject = session.get('materia', 'Sconosciuto')
                subject_stats[subject] = subject_stats.get(subject, 0) + session.get('durata', 0)
            
            top_subject = max(subject_stats.keys(), key=subject_stats.get) if subject_stats else "N/A"
            
            # Aggiorna statistiche
            stats_text = f"Sessioni totali: {total_sessions} | Tempo totale: {total_hours:.1f} ore | Materia preferita: {top_subject}"
            self.stats_label.configure(text=stats_text)
            
            # Mostra le ultime 20 sessioni
            recent_sessions = sessions[-20:] if len(sessions) > 20 else sessions
            recent_sessions.reverse()  # Più recenti prima
            
            for session in recent_sessions:
                self.create_session_card(session)
                
        except Exception as e:
            print(f"Errore nel caricamento sessioni: {e}")
            error_label = ctk.CTkLabel(
                self.sessions_frame,
                text="Errore nel caricamento delle sessioni",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )
            error_label.pack(pady=50)

    def create_session_card(self, session):
        """Crea una card per ogni sessione"""
        
        card_frame = ctk.CTkFrame(self.sessions_frame, corner_radius=8)
        card_frame.pack(fill="x", padx=5, pady=5)
        
        # Info sessione
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=10)
        
        # Materia e durata con emoji
        subject_name = session.get('materia', 'N/A')
        duration = session.get('durata', 0)
        emoji = UIHelpers.get_subject_emoji(subject_name)
        formatted_duration = UIHelpers.format_duration(duration)
        
        subject_duration = ctk.CTkLabel(
            info_frame,
            text=f"{emoji} {subject_name} - ⏱️ {formatted_duration}",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        subject_duration.pack(anchor="w")
        
        # Timestamp
        timestamp_formatted = UIHelpers.format_timestamp(session.get('timestamp', ''))
        timestamp = ctk.CTkLabel(
            info_frame,
            text=f"📅 {timestamp_formatted}",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        timestamp.pack(anchor="w")

class SubjectManagementWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app)
        self.window.title("Gestione Materie")
        self.window.geometry("650x550")
        self.window.resizable(True, True)
        self.window.minsize(600, 500)
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.window.transient(main_app)
        self.window.grab_set()
        
        self.setup_ui()
        self.center_window()
        self.load_subjects()

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia"""
        
        # Frame principale
        main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(2, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="Gestione Materie",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 20))
        
        # Frame per aggiungere materia
        add_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        add_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        add_label = ctk.CTkLabel(
            add_frame,
            text="➕ Aggiungi Nuova Materia",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        add_label.pack(pady=(15, 5))
        
        input_frame = ctk.CTkFrame(add_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        self.subject_entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Nome della materia...",
            font=ctk.CTkFont(size=14),
            height=35
        )
        self.subject_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        add_btn = ctk.CTkButton(
            input_frame,
            text="➕ Aggiungi",
            command=self.add_subject,
            height=35,
            width=100,
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e")
        )
        add_btn.pack(side="right")
        
        # Bind Enter key
        self.subject_entry.bind("<Return>", lambda e: self.add_subject())
        
        # Frame scrollabile per le materie esistenti
        self.subjects_frame = ctk.CTkScrollableFrame(
            main_frame, 
            corner_radius=10,
            label_text="📖 Materie Esistenti"
        )
        self.subjects_frame.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Pulsante chiudi
        close_btn = ctk.CTkButton(
            main_frame,
            text="✅ Chiudi",
            command=self.window.destroy,
            height=40,
            width=120
        )
        close_btn.pack(pady=(0, 15))

    def load_subjects(self):
        """Carica e mostra le materie"""
        # Pulisce il frame
        for widget in self.subjects_frame.winfo_children():
            widget.destroy()
        
        try:
            subjects_data = dataM.load_subjects(self.main_app.current_user)
            subjects_list = subjects_data.get(self.main_app.current_user, [])
            
            if not subjects_list:
                no_subjects_label = ctk.CTkLabel(
                    self.subjects_frame,
                    text="Nessuna materia trovata\nAggiungi la tua prima materia usando il campo sopra",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                no_subjects_label.pack(pady=50)
                return
            
            for subject in subjects_list:
                self.create_subject_card(subject)
                
        except Exception as e:
            print(f"Errore nel caricamento materie: {e}")
            error_label = ctk.CTkLabel(
                self.subjects_frame,
                text="Errore nel caricamento delle materie",
                font=ctk.CTkFont(size=16),
                text_color="red"
            )
            error_label.pack(pady=50)

    def create_subject_card(self, subject):
        """Crea una card per ogni materia"""
        
        card_frame = ctk.CTkFrame(self.subjects_frame, corner_radius=8)
        card_frame.pack(fill="x", padx=5, pady=5)
        
        content_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=15, pady=10)
        
        # Nome materia con emoji appropriato
        emoji = UIHelpers.get_subject_emoji(subject)
        subject_label = ctk.CTkLabel(
            content_frame,
            text=f"{emoji} {subject}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subject_label.pack(side="left", anchor="w")
        
        # Pulsante rimuovi
        remove_btn = ctk.CTkButton(
            content_frame,
            text="🗑️ Rimuovi",
            command=lambda s=subject: self.remove_subject(s),
            height=30,
            width=80,
            fg_color="red",
            hover_color="darkred"
        )
        remove_btn.pack(side="right")

    def add_subject(self):
        """Aggiunge una nuova materia"""
        subject_name = self.subject_entry.get().strip()
        
        # Validazione usando DataValidator
        is_valid, result = DataValidator.validate_subject_name(subject_name)
        if not is_valid:
            messagebox.showerror("Errore", result)
            return
        
        subject_name = result  # Nome validato e pulito
        
        try:
            # Carica materie esistenti
            subjects_data = dataM.load_subjects(self.main_app.current_user)
            subjects_list = subjects_data.get(self.main_app.current_user, [])
            
            if subject_name in subjects_list:
                messagebox.showwarning("Attenzione", "Questa materia esiste già!")
                return
            
            # Aggiungi la nuova materia
            subjects_list.append(subject_name)
            subjects_data[self.main_app.current_user] = subjects_list
            
            # Salva
            dataM.save_subjects(subjects_data)
            
            # Pulisci input e ricarica
            self.subject_entry.delete(0, tk.END)
            self.load_subjects()
            
            messagebox.showinfo("Successo", f"Materia '{subject_name}' aggiunta con successo!")
            
        except Exception as e:
            print(f"Errore nell'aggiunta materia: {e}")
            messagebox.showerror("Errore", "Errore nell'aggiunta della materia!")

    def remove_subject(self, subject):
        """Rimuove una materia"""
        result = messagebox.askyesno(
            "Conferma", 
            f"Vuoi davvero rimuovere la materia '{subject}'?"
        )
        
        if not result:
            return
        
        try:
            # Carica materie esistenti
            subjects_data = dataM.load_subjects(self.main_app.current_user)
            subjects_list = subjects_data.get(self.main_app.current_user, [])
            
            if subject in subjects_list:
                subjects_list.remove(subject)
                subjects_data[self.main_app.current_user] = subjects_list
                
                # Salva
                dataM.save_subjects(subjects_data)
                
                # Ricarica
                self.load_subjects()
                
                messagebox.showinfo("Successo", f"Materia '{subject}' rimossa con successo!")
            
        except Exception as e:
            print(f"Errore nella rimozione materia: {e}")
            messagebox.showerror("Errore", "Errore nella rimozione della materia!")

class TimerWindow:
    def __init__(self, main_app, subject, duration_minutes):
        self.main_app = main_app
        self.subject = subject
        self.duration_minutes = duration_minutes
        self.total_seconds = duration_minutes * 60
        self.elapsed_seconds = 0
        self.is_paused = False
        self.is_running = False
        self.timer_thread = None
        
        self.window = ctk.CTkToplevel(main_app)
        self.window.title(f"Timer - {subject}")
        self.window.geometry("700x550")
        self.window.resizable(True, True)
        self.window.minsize(600, 500)
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.window.transient(main_app)
        self.window.grab_set()
        
        # Gestione chiusura sicura del timer
        self.window.protocol("WM_DELETE_WINDOW", self.on_timer_close)
        
        self.setup_ui()
        self.center_window()
        
        # Avvia automaticamente il timer
        self.start_timer()

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia del timer"""
        
        # Frame principale
        main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Materia
        subject_label = ctk.CTkLabel(
            main_frame,
            text=f"📚 {self.subject}",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        subject_label.pack(pady=(30, 20))
        
        # Timer display
        self.timer_label = ctk.CTkLabel(
            main_frame,
            text=self.format_time(self.total_seconds),
            font=ctk.CTkFont(size=72, weight="bold")
        )
        self.timer_label.pack(pady=20)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="▶️ IN CORSO",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="green"
        )
        self.status_label.pack(pady=10)
        
        # Progress bar
        self.progress_bar = ctk.CTkProgressBar(
            main_frame,
            width=400,
            height=20
        )
        self.progress_bar.pack(pady=20)
        self.progress_bar.set(0)
        
        # Pulsanti controllo
        control_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        control_frame.pack(pady=20)
        
        self.pause_btn = ctk.CTkButton(
            control_frame,
            text="⏸️ Pausa",
            command=self.toggle_pause,
            height=50,
            width=120,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#ea580c", "#f97316"),
            hover_color=("#dc2626", "#ef4444")
        )
        self.pause_btn.pack(side="left", padx=10)
        
        stop_btn = ctk.CTkButton(
            control_frame,
            text="⏹️ Stop",
            command=self.stop_timer,
            height=50,
            width=120,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#dc2626", "#ef4444"),
            hover_color=("#991b1b", "#dc2626")
        )
        stop_btn.pack(side="left", padx=10)

    def format_time(self, seconds):
        """Formatta i secondi in MM:SS"""
        minutes, secs = divmod(seconds, 60)
        return f"{minutes:02d}:{secs:02d}"

    def start_timer(self):
        """Avvia il timer"""
        self.is_running = True
        self.timer_thread = threading.Thread(target=self.timer_worker, daemon=True)
        self.timer_thread.start()

    def timer_worker(self):
        """Worker del timer (eseguito in thread separato)"""
        while self.is_running and self.total_seconds > 0:
            if not self.is_paused:
                time.sleep(1)
                self.total_seconds -= 1
                self.elapsed_seconds += 1
                
                # Aggiorna UI nel thread principale
                self.window.after(0, self.update_ui)
            else:
                time.sleep(0.1)
        
        if self.is_running and self.total_seconds <= 0:
            # Timer completato
            self.window.after(0, self.timer_finished)

    def update_ui(self):
        """Aggiorna l'interfaccia utente"""
        self.timer_label.configure(text=self.format_time(self.total_seconds))
        
        # Aggiorna progress bar
        progress = self.elapsed_seconds / (self.duration_minutes * 60)
        self.progress_bar.set(progress)
        
        # Aggiorna status
        if self.is_paused:
            self.status_label.configure(text="⏸️ IN PAUSA", text_color="orange")
        else:
            self.status_label.configure(text="▶️ IN CORSO", text_color="green")

    def toggle_pause(self):
        """Alterna pausa/riprendi"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.pause_btn.configure(text="▶️ Riprendi")
        else:
            self.pause_btn.configure(text="⏸️ Pausa")

    def stop_timer(self):
        """Ferma il timer"""
        result = messagebox.askyesno(
            "Conferma", 
            "Vuoi davvero fermare il timer?\nLa sessione verrà salvata con il tempo trascorso."
        )
        
        if result:
            self.is_running = False
            self.save_session()
            self.window.destroy()

    def timer_finished(self):
        """Chiamato quando il timer finisce"""
        self.is_running = False
        
        # Suono di notifica
        try:
            # Sistema beep
            import winsound
            winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
        except:
            print("\a")  # Fallback beep
        
        # Mostra messaggio
        messagebox.showinfo(
            "Timer Completato!", 
            f"Ottimo lavoro! 🎉\nHai completato {self.duration_minutes} minuti di {self.subject}!"
        )
        
        # Salva sessione
        self.save_session()
        
        # Chiudi finestra
        self.window.destroy()

    def save_session(self):
        """Salva la sessione nel database"""
        try:
            effective_duration = int(self.elapsed_seconds / 60)
            if effective_duration < 1:
                effective_duration = 1  # Minimo 1 minuto
            
            # Mostra finestra per aggiungere nota argomento
            note_dialog = NoteDialog(self.window, self.subject, effective_duration)
            self.window.wait_window(note_dialog.dialog)
            
            note_text = note_dialog.note_text if hasattr(note_dialog, 'note_text') else ""
            
            success = dataM.save_session(self.main_app.current_user, self.subject, effective_duration, note_text)
            
            if success:
                success_msg = f"Sessione salvata con successo!\n\nMateria: {self.subject}\nDurata: {effective_duration} minuti"
                if note_text:
                    success_msg += f"\nArgomento: {note_text}"
                messagebox.showinfo("Sessione Completata", success_msg)
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio della sessione!")
                
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            messagebox.showerror("Errore", f"Errore nel salvataggio della sessione!\n\nDettagli: {e}")
            
    def on_timer_close(self):
        """Gestisce chiusura timer con conferma se attivo"""
        try:
            if self.is_running:
                response = messagebox.askyesnocancel(
                    "Timer Attivo",
                    "⏱️ Il timer è ancora attivo!\n\nVuoi salvare la sessione parziale?"
                )
                if response is True:  # Sì, salva
                    self.save_session()
                    self.window.destroy()
                elif response is False:  # No, non salvare
                    self.window.destroy()
                # None = Annulla, non fare niente
            else:
                self.window.destroy()
        except Exception as e:
            print(f"Errore chiusura timer: {e}")
            self.window.destroy()

class StopwatchSubjectSelectionWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app)
        self.window.title("📚 Selezione Materia - Cronometro")
        self.window.geometry("500x400")
        self.window.resizable(True, True)
        self.window.minsize(450, 350)
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.window.transient(main_app)
        self.window.grab_set()
        
        # Gestione chiusura sicura
        self.window.protocol("WM_DELETE_WINDOW", lambda: self.window.destroy())
        
        self.setup_ui()
        self.center_window()
        self.load_subjects()

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia di selezione materia"""
        
        # Frame principale
        main_frame = ctk.CTkFrame(
            self.window, 
            corner_radius=15,
            fg_color=("#0e1621", "#0e1621"),
            border_width=1,
            border_color=("#1a1a2e", "#1a1a2e")
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="⏱️ Cronometro",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=(30, 10))
        
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Seleziona una materia per iniziare",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame per la selezione materia
        subject_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        subject_frame.pack(fill="x", padx=20, pady=20)
        
        subject_label = ctk.CTkLabel(
            subject_frame,
            text="📚 Seleziona Materia:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subject_label.pack(pady=(20, 10))
        
        self.subject_combo = ctk.CTkComboBox(
            subject_frame,
            values=[],
            font=ctk.CTkFont(size=14),
            width=300,
            height=35,
            state="readonly"
        )
        self.subject_combo.pack(pady=(0, 20))
        
        # Frame pulsanti
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=30)
        
        # Pulsante Avvia Cronometro
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="⏱️ Avvia Cronometro",
            command=self.start_stopwatch,
            height=50,
            width=180,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e")
        )
        self.start_btn.pack(side="left", padx=10)
        
        # Pulsante Annulla
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Annulla",
            command=self.window.destroy,
            height=50,
            width=120,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent",
            border_width=2
        )
        cancel_btn.pack(side="left", padx=10)

    def load_subjects(self):
        """Carica le materie dell'utente"""
        try:
            subjects_data = dataM.load_subjects(self.main_app.current_user)
            subjects_list = subjects_data.get(self.main_app.current_user, [])
            
            if not subjects_list:
                messagebox.showwarning(
                    "Nessuna Materia", 
                    "Non hai ancora aggiunto delle materie.\nVai in 'Gestione Materie' per aggiungerne."
                )
                self.window.destroy()
                return
            
            self.subject_combo.configure(values=subjects_list)
            if subjects_list:
                self.subject_combo.set(subjects_list[0])
                
        except Exception as e:
            print(f"Errore nel caricamento materie: {e}")
            messagebox.showerror("Errore", "Errore nel caricamento delle materie!")
            self.window.destroy()

    def start_stopwatch(self):
        """Avvia il cronometro con la materia selezionata"""
        selected_subject = self.subject_combo.get()
        
        if not selected_subject:
            messagebox.showerror("Errore", "Seleziona una materia!")
            return
        
        # Chiudi questa finestra
        self.window.destroy()
        
        # Apri cronometro con materia selezionata
        stopwatch_window = StopwatchWindow(self.main_app, selected_subject)

class StopwatchWindow:
    def __init__(self, main_app, subject=None):
        self.main_app = main_app
        self.subject = subject
        self.elapsed_seconds = 0
        self.is_running = False
        self.is_paused = False
        self.timer_thread = None
        
        self.window = ctk.CTkToplevel(main_app)
        title = f"⏱️ Cronometro - {self.subject}" if self.subject else "⏱️ Cronometro"
        self.window.title(title)
        self.window.geometry("600x550")
        self.window.resizable(True, True)
        self.window.minsize(550, 500)
        
        # Configura griglia per ridimensionamento dinamico
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        self.window.transient(main_app)
        self.window.grab_set()
        
        # Gestione chiusura sicura
        self.window.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        self.setup_ui()
        self.center_window()

    def center_window(self):
        """Centra la finestra"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        pos_x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

    def setup_ui(self):
        """Configura l'interfaccia del cronometro"""
        
        # Frame principale con layout ottimizzato
        main_frame = ctk.CTkFrame(self.window, corner_radius=15)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Frame superiore per contenuto principale
        content_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Titolo
        title_label = ctk.CTkLabel(
            content_frame,
            text="⏱️ Cronometro",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(10, 5))
        
        # Materia selezionata
        if self.subject:
            subject_label = ctk.CTkLabel(
                content_frame,
                text=f"📚 {self.subject}",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color=("#3b82f6", "#60a5fa")
            )
            subject_label.pack(pady=(0, 15))
        
        # Display cronometro - dimensione ridotta per lasciare spazio ai pulsanti
        self.timer_label = ctk.CTkLabel(
            content_frame,
            text="00:00:00",
            font=ctk.CTkFont(size=48, weight="bold")
        )
        self.timer_label.pack(pady=15)
        
        # Status label
        self.status_label = ctk.CTkLabel(
            content_frame,
            text="⏹️ FERMO",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="gray"
        )
        self.status_label.pack(pady=(5, 15))
        
        # Frame contenitore per pulsanti fisso in basso
        buttons_container = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_container.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Prima riga di pulsanti - centrata
        button_frame1 = ctk.CTkFrame(buttons_container, fg_color="transparent")
        button_frame1.pack(pady=(0, 10))
        
        # Pulsante Start/Pause
        self.start_pause_btn = ctk.CTkButton(
            button_frame1,
            text="▶️ Inizia",
            command=self.toggle_stopwatch,
            height=50,
            width=140,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e")
        )
        self.start_pause_btn.pack(side="left", padx=10)
        
        # Pulsante Sospendi (salva sessione)
        self.stop_btn = ctk.CTkButton(
            button_frame1,
            text="⏹️ Sospendi",
            command=self.stop_and_save,
            height=50,
            width=140,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#dc2626", "#ef4444"),
            hover_color=("#991b1b", "#dc2626")
        )
        self.stop_btn.pack(side="left", padx=10)
        
        # Pulsante Reset
        self.reset_btn = ctk.CTkButton(
            button_frame1,
            text="🔄 Reset",
            command=self.reset_stopwatch,
            height=50,
            width=140,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#ea580c", "#f97316"),
            hover_color=("#dc2626", "#ef4444")
        )
        self.reset_btn.pack(side="left", padx=10)
        
        # Seconda riga - Pulsante Chiudi centrato
        button_frame2 = ctk.CTkFrame(buttons_container, fg_color="transparent")
        button_frame2.pack(pady=(10, 0))
        
        close_btn = ctk.CTkButton(
            button_frame2,
            text="✅ Chiudi",
            command=self.safe_close,
            height=40,
            width=150,
            font=ctk.CTkFont(size=14)
        )
        close_btn.pack()

    def toggle_stopwatch(self):
        """Avvia/Pausa il cronometro"""
        if not self.is_running:
            self.start_stopwatch()
        else:
            self.pause_stopwatch()

    def start_stopwatch(self):
        """Avvia il cronometro"""
        if not self.is_running:
            self.is_running = True
            self.is_paused = False
            
            # Avvia il thread del cronometro
            if self.timer_thread is None or not self.timer_thread.is_alive():
                self.timer_thread = threading.Thread(target=self.stopwatch_worker, daemon=True)
                self.timer_thread.start()
            
            # Aggiorna i controlli UI
            self.start_pause_btn.configure(text="⏸️ Pausa")
            self.status_label.configure(text="▶️ IN CORSO", text_color="green")

    def pause_stopwatch(self):
        """Pausa il cronometro"""
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            self.start_pause_btn.configure(text="▶️ Riprendi")
            self.status_label.configure(text="⏸️ IN PAUSA", text_color="orange")
        else:
            self.start_pause_btn.configure(text="⏸️ Pausa")
            self.status_label.configure(text="▶️ IN CORSO", text_color="green")

    def reset_stopwatch(self):
        """Reset del cronometro"""
        # Ferma completamente il cronometro
        self.is_running = False
        self.is_paused = False
        self.elapsed_seconds = 0
        
        # Aspetta che il thread termini se esiste
        if self.timer_thread and self.timer_thread.is_alive():
            self.is_running = False
            
        # Aggiorna UI
        self.start_pause_btn.configure(text="▶️ Inizia")
        self.status_label.configure(text="⏹️ FERMO", text_color="gray")
        self.update_display()

    def stopwatch_worker(self):
        """Worker del cronometro (thread separato)"""
        while self.is_running:
            if not self.is_paused:
                time.sleep(1)
                self.elapsed_seconds += 1
                self.window.after(0, self.update_display)
            else:
                time.sleep(0.1)

    def update_display(self):
        """Aggiorna il display del tempo"""
        formatted_time = self.format_time(self.elapsed_seconds)
        self.timer_label.configure(text=formatted_time)

    def format_time(self, seconds):
        """Formatta i secondi in HH:MM:SS"""
        hours, remainder = divmod(seconds, 3600)
        minutes, secs = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    def stop_and_save(self):
        """Ferma il cronometro e salva la sessione"""
        if self.elapsed_seconds < 60:  # Meno di 1 minuto
            result = messagebox.askyesno(
                "Sessione Breve",
                "La sessione è durata meno di 1 minuto.\nVuoi comunque salvarla?"
            )
            if not result:
                return
        
        # Ferma il cronometro
        self.is_running = False
        self.is_paused = False
        
        # Calcola durata in minuti (minimo 1)
        duration_minutes = max(1, int(self.elapsed_seconds / 60))
        
        # Salva la sessione
        if self.subject:
            try:
                success = dataM.save_session(self.main_app.current_user, self.subject, duration_minutes)
                
                if success:
                    messagebox.showinfo(
                        "Sessione Salvata", 
                        f"✅ Sessione salvata con successo!\n\n📚 Materia: {self.subject}\n⏱️ Durata: {duration_minutes} minuti"
                    )
                    self.window.destroy()
                else:
                    messagebox.showerror("Errore", "❌ Errore nel salvataggio della sessione!")
                    
            except Exception as e:
                print(f"Errore nel salvataggio: {e}")
                messagebox.showerror("Errore", f"❌ Errore nel salvataggio!\n\nDettagli: {e}")
        else:
            messagebox.showwarning("Attenzione", "Nessuna materia selezionata per il salvataggio!")

    def safe_close(self):
        """Chiusura sicura del cronometro"""
        try:
            if self.is_running and self.elapsed_seconds > 30:  # Se sta girando e ha più di 30 secondi
                result = messagebox.askyesnocancel(
                    "Cronometro Attivo",
                    "⏱️ Il cronometro è ancora attivo!\n\nVuoi salvare la sessione?"
                )
                if result is True:  # Sì, salva
                    self.stop_and_save()
                    return
                elif result is False:  # No, non salvare
                    self.is_running = False
                    self.is_paused = False
                    self.window.destroy()
                # None = Annulla, non fare niente
            else:
                self.is_running = False
                self.is_paused = False
                self.window.destroy()
        except Exception as e:
            print(f"Errore chiusura StopwatchWindow: {e}")
            self.window.destroy()


class AnalyticsWindow:
    """Finestra per l'analisi dei dati e visualizzazione grafici"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.current_user = main_app.current_user
        
        # Inizializza analytics engine
        try:
            from analytics_engine import AnalyticsEngine
            from chart_generator import ChartGenerator
            
            self.analytics = AnalyticsEngine(self.current_user)
            self.chart_gen = ChartGenerator(self.analytics)
            
            self.setup_window()
            self.create_widgets()
            self.load_initial_data()
            
            # Assicurati che la finestra sia visibile
            self.window.lift()
            self.window.focus_force()
            
        except Exception as e:
            print(f"ERRORE ANALYTICS: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Errore", f"Errore analytics: {e}")
            # Crea finestra di errore invece di uscire
            self.create_error_window(e)
    
    def create_error_window(self, error):
        """Crea una finestra di errore quando l'analytics non può essere caricato"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("Errore Analytics")
        self.window.geometry("500x300")
        
        error_label = ctk.CTkLabel(
            self.window,
            text=f"Impossibile caricare l'Analytics:\\n{str(error)}",
            font=ctk.CTkFont(size=14),
            wraplength=450
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        close_btn = ctk.CTkButton(
            self.window,
            text="Chiudi",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
    
    def setup_window(self):
        """Configura la finestra principale"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("Analytics - TimeTrackerT2")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        self.window.minsize(1000, 700)
        
        # Configura il grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        
        # Frame del titolo
        title_frame = ctk.CTkFrame(self.window)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"Analytics per {self.current_user}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Frame controlli periodo
        controls_frame = ctk.CTkFrame(self.window)
        controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Selezione periodo
        period_label = ctk.CTkLabel(controls_frame, text="Periodo:")
        period_label.grid(row=1, column=0, padx=10, pady=10)
        
        self.period_var = ctk.StringVar(value="tutto")
        period_menu = ctk.CTkOptionMenu(
            controls_frame,
            variable=self.period_var,
            values=["tutto", "oggi", "settimana", "mese"],
            command=self.on_period_change
        )
        period_menu.grid(row=1, column=1, padx=10, pady=10)
        
        # Pulsanti per tipi di grafico
        chart_types_frame = ctk.CTkFrame(controls_frame)
        chart_types_frame.grid(row=1, column=2, columnspan=4, padx=20, pady=10)
        
        self.create_chart_buttons(chart_types_frame)
        
        # Frame principale contenuto
        main_frame = ctk.CTkFrame(self.window)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Sidebar per statistiche
        self.create_stats_sidebar(main_frame)
        
        # Area grafico
        self.create_chart_area(main_frame)
    
    def create_chart_buttons(self, parent):
        """Crea i pulsanti per i tipi di grafico"""
        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Materie (Torta)", lambda: self.show_subject_chart("pie")),
            ("Materie (Barre)", lambda: self.show_subject_chart("bar")),
            ("Pattern Orario", self.show_hourly_heatmap),
            ("Pattern Settimanale", self.show_weekday_pattern)
        ]
        
        for i, (text, command) in enumerate(buttons):
            btn = ctk.CTkButton(
                parent, 
                text=text,
                command=command,
                width=130,
                height=30
            )
            btn.grid(row=i//4, column=i%4, padx=5, pady=5)
    
    def create_stats_sidebar(self, parent):
        """Crea la sidebar con le statistiche"""
        stats_frame = ctk.CTkScrollableFrame(parent, width=250)
        stats_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=10)
        
        # Titolo statistiche
        stats_title = ctk.CTkLabel(
            stats_frame,
            text="Statistiche",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        stats_title.pack(pady=(0, 20))
        
        # Textbox per le statistiche
        self.stats_text = ctk.CTkTextbox(
            stats_frame,
            width=230,
            height=400,
            wrap="word"
        )
        self.stats_text.pack(fill="both", expand=True)
        
    def create_chart_area(self, parent):
        """Crea l'area per i grafici"""
        # Frame per il grafico
        self.chart_frame = ctk.CTkFrame(parent)
        self.chart_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(0, weight=1)
        
        # Label di benvenuto
        welcome_label = ctk.CTkLabel(
            self.chart_frame,
            text="Seleziona un tipo di grafico per iniziare!",
            font=ctk.CTkFont(size=16)
        )
        welcome_label.grid(row=0, column=0, pady=50)
    
    def load_initial_data(self):
        """Carica i dati iniziali"""
        self.update_stats()
    
    def update_stats(self):
        """Aggiorna le statistiche nella sidebar"""
        try:
            insights = self.analytics.get_productivity_insights()
            
            stats_text = f"""
STATISTICHE GENERALI

Sessioni Totali: {insights['total_sessions']}
Ore Totali: {insights['total_hours']:.1f}h
Media per Sessione: {insights['avg_session_length']:.1f}h

TOP PERFORMANCE

Materia più Studiata:
{insights['most_studied_subject']}

Ora più Produttiva:
{insights['most_productive_hour']}

Giorno più Produttivo:
{insights['most_productive_day']}

ANALISI PERIODO CORRENTE

Tempo Totale: {self.analytics.get_total_study_time(self.period_var.get()):.1f}h

            """
            
            # Aggiungi statistiche per materia del periodo corrente
            subject_stats = self.analytics.get_study_time_by_subject(self.period_var.get())
            if subject_stats:
                stats_text += "\nTEMPO PER MATERIA:\n"
                for subject, hours in sorted(subject_stats.items(), key=lambda x: x[1], reverse=True):
                    stats_text += f"- {subject}: {hours:.1f}h\n"
            
            self.stats_text.delete("1.0", "end")
            self.stats_text.insert("1.0", stats_text)
            
        except Exception as e:
            print(f"Errore aggiornamento statistiche: {e}")
    
    def clear_chart_area(self):
        """Pulisce l'area del grafico"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
    
    def display_chart(self, figure):
        """Mostra un grafico matplotlib"""
        try:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            
            self.clear_chart_area()
            
            canvas = FigureCanvasTkAgg(figure, self.chart_frame)
            canvas.draw()
            
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            
            # Toolbar rimossa per evitare conflitti geometry manager
            
        except Exception as e:
            print(f"Errore visualizzazione grafico: {e}")
            self.show_error_message(f"Errore nella visualizzazione: {e}")
    
    def show_error_message(self, message):
        """Mostra messaggio di errore"""
        self.clear_chart_area()
        error_label = ctk.CTkLabel(
            self.chart_frame,
            text=f"ERRORE: {message}",
            font=ctk.CTkFont(size=14),
            text_color="red"
        )
        error_label.grid(row=0, column=0, pady=50)
    
    # Metodi per i diversi tipi di grafici
    def show_dashboard(self):
        """Mostra dashboard generale"""
        try:
            fig = self.chart_gen.create_productivity_dashboard()
            self.display_chart(fig)
        except Exception as e:
            self.show_error_message(f"Errore dashboard: {e}")
    
    def show_subject_chart(self, chart_type="pie"):
        """Mostra grafico distribuzione materie"""
        try:
            fig = self.chart_gen.create_subject_distribution_chart(
                period=self.period_var.get(),
                chart_type=chart_type
            )
            self.display_chart(fig)
        except Exception as e:
            self.show_error_message(f"Errore grafico materie: {e}")
    
    # Funzioni trend giornaliero e confronto settimanale rimosse per semplificare l'interfaccia
    
    def show_hourly_heatmap(self):
        """Mostra heatmap oraria"""
        try:
            fig = self.chart_gen.create_hourly_heatmap()
            self.display_chart(fig)
        except Exception as e:
            self.show_error_message(f"Errore pattern orario: {e}")
    
    def show_weekday_pattern(self):
        """Mostra pattern settimanale"""
        try:
            fig = self.chart_gen.create_weekday_pattern_chart()
            self.display_chart(fig)
        except Exception as e:
            self.show_error_message(f"Errore pattern settimanale: {e}")
    
    def on_period_change(self, new_period):
        """Callback per cambio periodo"""
        self.update_stats()
        # Ricarica il grafico corrente se presente
        # (Implementazione opzionale per auto-refresh)


class GoalsWindow:
    """Finestra per la gestione degli obiettivi di studio"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.current_user = main_app.current_user
        
        # Inizializza il gestore obiettivi
        try:
            from goals_manager import GoalsManager
            self.goals_manager = GoalsManager()
            
            self.setup_window()
            self.create_widgets()
            self.load_goals()
            self.check_new_completions()  # Controlla obiettivi appena completati
            
            # Assicurati che la finestra sia visibile
            self.window.lift()
            self.window.focus_force()
            
        except Exception as e:
            print(f"ERRORE GOALS: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Errore", f"Errore inizializzazione obiettivi: {e}")
            # Crea finestra di errore invece di uscire
            self.create_error_window(e)
    
    def create_error_window(self, error):
        """Crea una finestra di errore quando gli obiettivi non possono essere caricati"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("Errore Obiettivi")
        self.window.geometry("500x300")
        
        error_label = ctk.CTkLabel(
            self.window,
            text=f"Impossibile caricare gli Obiettivi:\\n{str(error)}",
            font=ctk.CTkFont(size=14),
            wraplength=450
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        close_btn = ctk.CTkButton(
            self.window,
            text="Chiudi",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
    
    def setup_window(self):
        """Configura la finestra principale"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("Obiettivi - TimeTrackerT2")
        self.window.geometry("900x650")
        self.window.resizable(True, True)
        self.window.minsize(800, 600)
        
        # Configura il grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Rende la finestra modale
        self.window.transient(self.main_app)
        self.window.grab_set()
    
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        
        # Frame del titolo
        title_frame = ctk.CTkFrame(self.window)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"Obiettivi di Studio - {self.current_user}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=15)
        
        # Frame principale contenuto
        main_frame = ctk.CTkFrame(self.window)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Sidebar sinistra per nuovo obiettivo
        self.create_new_goal_sidebar(main_frame)
        
        # Area principale per lista obiettivi
        self.create_goals_list_area(main_frame)
    
    def create_new_goal_sidebar(self, parent):
        """Crea la sidebar per creare un nuovo obiettivo"""
        sidebar_frame = ctk.CTkScrollableFrame(parent, width=300, label_text="Nuovo Obiettivo")
        sidebar_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=10)
        
        # Form per nuovo obiettivo
        # Materia
        materia_label = ctk.CTkLabel(sidebar_frame, text="Materia:", font=ctk.CTkFont(size=14, weight="bold"))
        materia_label.pack(pady=(20, 5))
        
        # Carica materie disponibili
        self.load_subjects()
        self.materia_combo = ctk.CTkComboBox(
            sidebar_frame,
            values=self.subjects_list,
            width=260,
            height=35,
            state="readonly"
        )
        self.materia_combo.pack(pady=(0, 15))
        
        # Tempo obiettivo
        tempo_label = ctk.CTkLabel(sidebar_frame, text="Tempo Obiettivo:", font=ctk.CTkFont(size=14, weight="bold"))
        tempo_label.pack(pady=(0, 5))
        
        # Frame per ore e minuti
        time_frame = ctk.CTkFrame(sidebar_frame, fg_color="transparent")
        time_frame.pack(pady=(0, 15), fill="x")
        
        # Ore
        ore_label = ctk.CTkLabel(time_frame, text="Ore:")
        ore_label.pack(pady=2)
        self.ore_entry = ctk.CTkEntry(time_frame, width=120, placeholder_text="0")
        self.ore_entry.pack(pady=2)
        
        # Minuti
        minuti_label = ctk.CTkLabel(time_frame, text="Minuti:")
        minuti_label.pack(pady=2)
        self.minuti_entry = ctk.CTkEntry(time_frame, width=120, placeholder_text="0")
        self.minuti_entry.pack(pady=2)
        
        # Intervallo
        intervallo_label = ctk.CTkLabel(sidebar_frame, text="Intervallo:", font=ctk.CTkFont(size=14, weight="bold"))
        intervallo_label.pack(pady=(0, 5))
        
        self.intervallo_combo = ctk.CTkComboBox(
            sidebar_frame,
            values=["giorno", "settimana", "mese"],
            width=260,
            height=35,
            state="readonly"
        )
        self.intervallo_combo.set("settimana")  # Default
        self.intervallo_combo.pack(pady=(0, 20))
        
        # Pulsante crea obiettivo
        create_btn = ctk.CTkButton(
            sidebar_frame,
            text="Crea Obiettivo",
            command=self.create_new_goal,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=("#2d5aa0", "#3b82f6"),
            hover_color=("#1e40af", "#60a5fa")
        )
        create_btn.pack(pady=(0, 20))
    
    def create_goals_list_area(self, parent):
        """Crea l'area per visualizzare la lista degli obiettivi"""
        # Frame principale per lista
        list_frame = ctk.CTkScrollableFrame(parent, label_text="I Tuoi Obiettivi")
        list_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.goals_container = list_frame
        
        # Messaggio iniziale (verrà sostituito dalla lista)
        self.no_goals_label = ctk.CTkLabel(
            self.goals_container,
            text="Nessun obiettivo creato ancora.\\nCrea il tuo primo obiettivo!",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.no_goals_label.pack(pady=50)
    
    def load_subjects(self):
        """Carica la lista delle materie disponibili"""
        try:
            # Usa la stessa logica di NewSessionWindow
            subjects_data = dataM.load_subjects(self.current_user)
            if isinstance(subjects_data, dict):
                # Se è un dizionario, prendi le materie per questo utente
                if self.current_user in subjects_data:
                    self.subjects_list = subjects_data[self.current_user]
                else:
                    self.subjects_list = list(subjects_data.keys()) if subjects_data else []
            elif isinstance(subjects_data, list):
                self.subjects_list = subjects_data
            else:
                self.subjects_list = []
                
            if not self.subjects_list:
                messagebox.showwarning(
                    "Attenzione", 
                    "Nessuna materia trovata.\\nCrea prima delle materie nella sezione Gestione Materie."
                )
                self.subjects_list = ["Nessuna materia disponibile"]
        except Exception as e:
            print(f"Errore caricamento materie: {e}")
            self.subjects_list = ["Errore nel caricamento"]
    
    def create_new_goal(self):
        """Crea un nuovo obiettivo"""
        try:
            # Validazioni
            materia = self.materia_combo.get()
            if not materia or materia in ["Nessuna materia disponibile", "Errore nel caricamento"]:
                messagebox.showerror("Errore", "Seleziona una materia valida!")
                return
            
            # Ore
            ore_text = self.ore_entry.get().strip()
            if not ore_text:
                ore = 0
            else:
                try:
                    ore = int(ore_text)
                    if ore < 0:
                        raise ValueError("Le ore non possono essere negative")
                except ValueError:
                    messagebox.showerror("Errore", "Inserisci un numero valido per le ore!")
                    return
            
            # Minuti
            minuti_text = self.minuti_entry.get().strip()
            if not minuti_text:
                minuti = 0
            else:
                try:
                    minuti = int(minuti_text)
                    if minuti < 0 or minuti >= 60:
                        raise ValueError("I minuti devono essere tra 0 e 59")
                except ValueError:
                    messagebox.showerror("Errore", "Inserisci un numero valido per i minuti (0-59)!")
                    return
            
            # Controllo tempo totale
            if ore == 0 and minuti == 0:
                messagebox.showerror("Errore", "L'obiettivo deve avere almeno 1 minuto!")
                return
            
            # Intervallo
            intervallo = self.intervallo_combo.get()
            if not intervallo:
                messagebox.showerror("Errore", "Seleziona un intervallo valido!")
                return
            
            # Crea l'obiettivo
            success = self.goals_manager.create_goal(
                user=self.current_user,
                materia=materia,
                ore_target=ore,
                minuti_target=minuti,
                intervallo=intervallo
            )
            
            if success:
                messagebox.showinfo("Successo", f"Obiettivo creato!\\n\\nMateria: {materia}\\nTempo: {self.goals_manager.format_time(ore*60 + minuti)}\\nIntervallo: {intervallo}")
                
                # Reset form
                self.ore_entry.delete(0, 'end')
                self.minuti_entry.delete(0, 'end')
                self.intervallo_combo.set("settimana")
                
                # Ricarica la lista
                self.load_goals()
            else:
                messagebox.showerror("Errore", "Errore nella creazione dell'obiettivo!")
                
        except Exception as e:
            messagebox.showerror("Errore", f"Errore creazione obiettivo!\\n\\nDettagli: {e}")
    
    def load_goals(self):
        """Carica e visualizza tutti gli obiettivi dell'utente"""
        try:
            # Pulisce il contenitore
            for widget in self.goals_container.winfo_children():
                widget.destroy()
            
            # Carica gli obiettivi
            goals = self.goals_manager.get_user_goals(self.current_user)
            
            if not goals:
                self.no_goals_label = ctk.CTkLabel(
                    self.goals_container,
                    text="Nessun obiettivo creato ancora.\\nCrea il tuo primo obiettivo!",
                    font=ctk.CTkFont(size=16),
                    text_color="gray"
                )
                self.no_goals_label.pack(pady=50)
                return
            
            # Ordina per data di creazione (più recenti prima)
            goals.sort(key=lambda x: x.get('data_creazione', ''), reverse=True)
            
            # Crea widget per ogni obiettivo
            for goal in goals:
                self.create_goal_widget(goal)
                
        except Exception as e:
            print(f"Errore caricamento obiettivi: {e}")
            error_label = ctk.CTkLabel(
                self.goals_container,
                text=f"Errore nel caricamento:\\n{str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def create_goal_widget(self, goal):
        """Crea un widget per visualizzare un singolo obiettivo"""
        try:
            # Calcola il progresso
            minuti_studiati, minuti_target, percentuale = self.goals_manager.calculate_progress(
                self.current_user, goal
            )
            
            # Colore basato sullo stato
            color = self.goals_manager.get_goal_status_color(percentuale)
            
            # Frame principale per l'obiettivo
            goal_frame = ctk.CTkFrame(
                self.goals_container,
                corner_radius=10,
                border_width=2,
                border_color=color
            )
            goal_frame.pack(fill="x", padx=10, pady=8)
            
            # Header con materia e stato
            header_frame = ctk.CTkFrame(goal_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(15, 5))
            
            # Materia
            materia_label = ctk.CTkLabel(
                header_frame,
                text=goal['materia'],
                font=ctk.CTkFont(size=18, weight="bold")
            )
            materia_label.pack(side="left")
            
            # Status badge
            if goal.get('completato'):
                status_text = "COMPLETATO"
                status_color = "#28a745"
            else:
                status_text = f"{percentuale:.1f}%"
                status_color = color
            
            status_label = ctk.CTkLabel(
                header_frame,
                text=status_text,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=status_color
            )
            status_label.pack(side="right")
            
            # Info obiettivo
            info_frame = ctk.CTkFrame(goal_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=5)
            
            # Target e progresso
            target_time = self.goals_manager.format_time(minuti_target)
            studied_time = self.goals_manager.format_time(minuti_studiati)
            
            target_label = ctk.CTkLabel(
                info_frame,
                text=f"Obiettivo: {target_time} / {goal['intervallo']}",
                font=ctk.CTkFont(size=14)
            )
            target_label.pack(side="left")
            
            progress_label = ctk.CTkLabel(
                info_frame,
                text=f"Progresso: {studied_time}",
                font=ctk.CTkFont(size=14)
            )
            progress_label.pack(side="right")
            
            # Barra di progresso
            progress_frame = ctk.CTkFrame(goal_frame, fg_color="transparent")
            progress_frame.pack(fill="x", padx=15, pady=5)
            
            progress_bar = ctk.CTkProgressBar(progress_frame, width=400, height=20)
            progress_bar.pack(fill="x")
            progress_bar.set(min(1.0, percentuale / 100))
            
            # Frame pulsanti
            buttons_frame = ctk.CTkFrame(goal_frame, fg_color="transparent")
            buttons_frame.pack(fill="x", padx=15, pady=(5, 15))
            
            # Pulsante elimina
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="Elimina",
                command=lambda: self.delete_goal(goal['id']),
                height=25,
                width=80,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=12)
            )
            delete_btn.pack(side="right")
            
        except Exception as e:
            print(f"Errore creazione widget obiettivo: {e}")
    
    def delete_goal(self, goal_id):
        """Elimina un obiettivo"""
        try:
            # Conferma eliminazione
            if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questo obiettivo?"):
                success = self.goals_manager.delete_goal(goal_id)
                if success:
                    messagebox.showinfo("Successo", "Obiettivo eliminato!")
                    self.load_goals()  # Ricarica la lista
                else:
                    messagebox.showerror("Errore", "Errore nell'eliminazione dell'obiettivo!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore eliminazione!\\n\\nDettagli: {e}")
    
    def check_new_completions(self):
        """Controlla se ci sono obiettivi appena completati"""
        try:
            completed_goals = self.goals_manager.check_completed_goals(self.current_user)
            
            for goal in completed_goals:
                materia = goal['materia']
                target_time = self.goals_manager.format_time(goal['tempo_target_minuti'])
                intervallo = goal['intervallo']
                
                messagebox.showinfo(
                    "Obiettivo Raggiunto!",
                    f"Congratulazioni!\\n\\nHai completato l'obiettivo:\\n\\n"
                    f"Materia: {materia}\\n"
                    f"Tempo: {target_time}\\n"
                    f"Intervallo: {intervallo}\\n\\n"
                    f"Continua cosi!"
                )
            
        except Exception as e:
            print(f"Errore controllo completamenti: {e}")


class NoteDialog(AeroStyleMixin):
    """Finestra di dialogo moderna per inserire note argomento a fine sessione"""
    
    def __init__(self, parent, materia, durata_minuti):
        self.materia = materia
        self.durata_minuti = durata_minuti
        self.note_text = ""
        
        # Setup stile Aero
        self.setup_aero_styling()
        
        # Crea finestra dialogo moderna
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("📝 Aggiungi Nota Argomento")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        self.dialog.minsize(550, 450)
        
        # Styling Aero per la finestra
        self.dialog.configure(fg_color=self.colors['glass_bg'])
        
        # Centra e configura finestra
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.center_window()
        
        # Setup UI e focus
        self.setup_ui()
        self.note_entry.focus_set()
    
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
    
    def setup_ui(self):
        """Crea l'interfaccia moderna con design Aero"""
        
        # Frame principale con gradient Aero
        main_frame = ctk.CTkFrame(
            self.dialog,
            corner_radius=20,
            fg_color=self.colors['glass_bg'],
            border_width=2,
            border_color=self.colors['border_light']
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # === HEADER CON GLASS EFFECT ===
        header_frame = self.create_aero_header(
            main_frame,
            "Sessione Completata! 🎉",
            "✅",
            "success_green"
        )
        
        # === AREA SCROLLABILE ===
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            corner_radius=16,
            fg_color="transparent",
            scrollbar_button_color=self.colors['primary_blue'],
            scrollbar_button_hover_color=self.colors['border_light']
        )
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # === CARD INFO SESSIONE ===
        info_card, info_content = self.create_aero_card(
            scroll_frame,
            "Informazioni Sessione",
            "📊",
            "primary_blue"
        )
        info_card.pack(fill="x", pady=15, padx=10)
        
        # Calcola ore e minuti per display migliore
        hours = self.durata_minuti // 60
        minutes = self.durata_minuti % 60
        
        if hours > 0:
            durata_text = f"{hours}h {minutes}m" if minutes > 0 else f"{hours}h"
        else:
            durata_text = f"{minutes}m"
        
        # Info sessione con icone
        session_info = ctk.CTkFrame(
            info_content,
            fg_color="transparent",
            corner_radius=12
        )
        session_info.pack(fill="x", pady=10)
        
        materia_label = ctk.CTkLabel(
            session_info,
            text=f"📚 Materia: {self.materia}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        materia_label.pack(fill="x", pady=(5, 2))
        
        durata_label = ctk.CTkLabel(
            session_info,
            text=f"⏱️ Durata: {durata_text}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        durata_label.pack(fill="x", pady=2)
        
        # === CARD NOTA ARGOMENTO ===
        note_card, note_content = self.create_aero_card(
            scroll_frame,
            "Nota Argomento",
            "📝",
            "purple_creative"
        )
        note_card.pack(fill="x", pady=15, padx=10)
        
        # Testo helper
        helper_text = ctk.CTkLabel(
            note_content,
            text="💭 Aggiungi una nota per tracciare gli argomenti studiati:\n"
                 "• Aiuta a ricordare cosa hai fatto\n"
                 "• Migliora l'analisi dei progressi\n"
                 "• Facilita la revisione futura",
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary'],
            justify="left"
        )
        helper_text.pack(fill="x", pady=(5, 15))
        
        # Campo testo per nota con design moderno
        self.note_entry = ctk.CTkEntry(
            note_content,
            placeholder_text="es. Capitolo 5 - Normalizzazione database, Esercizi algebra lineare...",
            font=ctk.CTkFont(size=14),
            width=500,
            height=50,
            corner_radius=12,
            border_width=2,
            border_color=self.colors['border_light']
        )
        self.note_entry.pack(fill="x", pady=(0, 15))
        
        # Bind Enter per salvare
        self.note_entry.bind('<Return>', lambda e: self.save_note())
        
        # === FOOTER FISSO CON PULSANTI ===
        footer_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=16,
            fg_color=self.colors['card_bg'],
            height=80
        )
        footer_frame.pack(fill="x", padx=20, pady=(0, 20))
        footer_frame.pack_propagate(False)
        
        # Container pulsanti centrato
        buttons_container = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_container.pack(expand=True, fill="both")
        
        # Pulsante Salva con nota - Design Aero
        save_btn = ctk.CTkButton(
            buttons_container,
            text="📝 Salva con Nota",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=180,
            height=50,
            corner_radius=25,
            fg_color=self.colors['success_green'],
            hover_color=("#047857", "#059669"),
            border_width=2,
            border_color=("#10b981", "#34d399"),
            command=self.save_note
        )
        save_btn.pack(side="left", padx=(20, 10), pady=15)
        
        # Pulsante Salta nota
        skip_btn = ctk.CTkButton(
            buttons_container,
            text="⏭️ Salta Nota",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=150,
            height=50,
            corner_radius=25,
            fg_color=self.colors['gray_neutral'],
            hover_color=("#4b5563", "#6b7280"),
            command=self.skip_note
        )
        skip_btn.pack(side="left", padx=10, pady=15)
    
    def save_note(self):
        """Salva la nota e chiude il dialogo"""
        self.note_text = self.note_entry.get().strip()
        self.dialog.destroy()
    
    def skip_note(self):
        """Salta la nota (salva vuota) e chiude il dialogo"""
        self.note_text = ""
        self.dialog.destroy()


class NotesWindow:
    """Finestra per visualizzare timeline argomenti e gestione note di progresso"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.current_user = main_app.current_user
        
        # Inizializza il gestore note
        try:
            from progress_manager import ProgressManager
            self.progress_manager = ProgressManager()
            
            self.setup_window()
            self.create_widgets()
            self.load_notes()
            
            # Assicurati che la finestra sia visibile
            self.window.lift()
            self.window.focus_force()
            
        except Exception as e:
            print(f"ERRORE NOTES: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Errore", f"Errore inizializzazione note: {e}")
            self.create_error_window(e)
    
    def create_error_window(self, error):
        """Crea una finestra di errore quando le note non possono essere caricate"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("Errore Note")
        self.window.geometry("500x300")
        
        error_label = ctk.CTkLabel(
            self.window,
            text=f"Impossibile caricare le Note:\\n{str(error)}",
            font=ctk.CTkFont(size=14),
            wraplength=450
        )
        error_label.pack(expand=True, padx=20, pady=20)
        
        close_btn = ctk.CTkButton(
            self.window,
            text="Chiudi",
            command=self.window.destroy
        )
        close_btn.pack(pady=10)
    
    def setup_window(self):
        """Configura la finestra principale con design Aero"""
        self.window = ctk.CTkToplevel(self.main_app)
        self.window.title("📝 Registro Argomenti - TimeTrackerT2 Pro")
        self.window.geometry("1200x800")
        self.window.resizable(True, True)
        self.window.minsize(1000, 700)
        
        # Stile Aero
        self.colors = {
            'primary': ("#7c3aed", "#6d28d9"),
            'secondary': ("#f8fafc", "#334155"),
            'accent': ("#a78bfa", "#c4b5fd"),
            'card_bg': ("#ffffff", "#1e293b"),
            'glass_bg': ("#faf5ff", "#1e1b2e")
        }
        
        # Configura il grid
        self.window.grid_rowconfigure(1, weight=1)
        self.window.grid_columnconfigure(0, weight=1)
        
        # Rende la finestra modale
        self.window.transient(self.main_app)
        self.window.grab_set()
    
    def create_widgets(self):
        """Crea i widget dell'interfaccia"""
        
        # Frame del titolo e controlli
        title_frame = ctk.CTkFrame(self.window)
        title_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text=f"Registro Argomenti - {self.current_user}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", pady=15, padx=20)
        
        # Frame controlli filtri
        controls_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        controls_frame.pack(side="right", padx=20)
        
        # Filtro per materia
        filter_label = ctk.CTkLabel(controls_frame, text="Filtra per materia:")
        filter_label.pack(side="left", padx=(0, 10))
        
        # Carica materie per filtro
        self.load_subjects()
        filter_options = ["Tutte le materie"] + self.subjects_list
        
        self.filter_var = ctk.StringVar(value="Tutte le materie")
        self.filter_combo = ctk.CTkComboBox(
            controls_frame,
            variable=self.filter_var,
            values=filter_options,
            command=self.on_filter_change,
            width=200
        )
        self.filter_combo.pack(side="left", padx=(0, 10))
        
        # Pulsante aggiungi milestone
        add_btn = ctk.CTkButton(
            controls_frame,
            text="+ Milestone",
            command=self.show_add_milestone,
            height=30,
            width=100,
            fg_color=("#2d5aa0", "#3b82f6"),
            hover_color=("#1e40af", "#60a5fa")
        )
        add_btn.pack(side="left")
        
        # Frame principale contenuto
        main_frame = ctk.CTkFrame(self.window)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Sidebar statistiche
        self.create_stats_sidebar(main_frame)
        
        # Area timeline note
        self.create_timeline_area(main_frame)
    
    def load_subjects(self):
        """Carica la lista delle materie disponibili"""
        try:
            subjects_data = dataM.load_subjects(self.current_user)
            if isinstance(subjects_data, dict):
                if self.current_user in subjects_data:
                    self.subjects_list = subjects_data[self.current_user]
                else:
                    self.subjects_list = list(subjects_data.keys()) if subjects_data else []
            elif isinstance(subjects_data, list):
                self.subjects_list = subjects_data
            else:
                self.subjects_list = []
        except Exception as e:
            print(f"Errore caricamento materie: {e}")
            self.subjects_list = []
    
    def create_stats_sidebar(self, parent):
        """Crea la sidebar con le statistiche"""
        stats_frame = ctk.CTkScrollableFrame(parent, width=280, label_text="Statistiche Argomenti")
        stats_frame.grid(row=0, column=0, sticky="ns", padx=(0, 10), pady=10)
        
        self.stats_container = stats_frame
        
        # Le statistiche verranno caricate dinamicamente
        
    def create_timeline_area(self, parent):
        """Crea l'area timeline per visualizzare le note"""
        timeline_frame = ctk.CTkScrollableFrame(parent, label_text="Timeline Argomenti")
        timeline_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        self.timeline_container = timeline_frame
        
        # Messaggio iniziale (verrà sostituito dalla timeline)
        self.no_notes_label = ctk.CTkLabel(
            self.timeline_container,
            text="Nessuna nota argomento ancora.\\nCompleta delle sessioni con note per vederle qui!",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        self.no_notes_label.pack(pady=50)
    
    def load_notes(self):
        """Carica e visualizza tutte le note dell'utente"""
        try:
            # Determina materia filtro
            selected_filter = self.filter_var.get()
            materia_filter = None if selected_filter == "Tutte le materie" else selected_filter
            
            # Carica le note
            notes = self.progress_manager.get_user_notes(self.current_user, materia_filter)
            
            # Aggiorna timeline
            self.update_timeline(notes)
            
            # Aggiorna statistiche
            self.update_stats(materia_filter)
            
        except Exception as e:
            print(f"Errore caricamento note: {e}")
            error_label = ctk.CTkLabel(
                self.timeline_container,
                text=f"Errore nel caricamento:\\n{str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(pady=20)
    
    def update_timeline(self, notes):
        """Aggiorna la visualizzazione della timeline"""
        # Pulisce il contenitore
        for widget in self.timeline_container.winfo_children():
            widget.destroy()
        
        if not notes:
            self.no_notes_label = ctk.CTkLabel(
                self.timeline_container,
                text="Nessuna nota per il filtro selezionato.\\nProva a cambiare il filtro o aggiungi nuove note!",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )
            self.no_notes_label.pack(pady=50)
            return
        
        # Crea widget per ogni nota
        for note in notes:
            self.create_note_widget(note)
    
    def create_note_widget(self, note):
        """Crea un widget per visualizzare una singola nota"""
        try:
            # Frame principale per la nota
            note_frame = ctk.CTkFrame(
                self.timeline_container,
                corner_radius=10,
                border_width=1,
                border_color=("#3b82f6" if note.get('tipo') == 'milestone' else "#6b7280")
            )
            note_frame.pack(fill="x", padx=10, pady=8)
            
            # Header con materia e timestamp
            header_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(15, 5))
            
            # Materia e tipo
            tipo_icon = "🏆" if note.get('tipo') == 'milestone' else "📝"
            materia_text = f"{tipo_icon} {note['materia']}"
            
            materia_label = ctk.CTkLabel(
                header_frame,
                text=materia_text,
                font=ctk.CTkFont(size=16, weight="bold")
            )
            materia_label.pack(side="left")
            
            # Timestamp
            try:
                from datetime import datetime
                timestamp = datetime.fromisoformat(note.get('timestamp', ''))
                time_str = timestamp.strftime("%d/%m/%Y %H:%M")
            except:
                time_str = note.get('timestamp', 'N/A')
            
            time_label = ctk.CTkLabel(
                header_frame,
                text=time_str,
                font=ctk.CTkFont(size=12),
                text_color="gray"
            )
            time_label.pack(side="right")
            
            # Argomento
            argomento_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
            argomento_frame.pack(fill="x", padx=15, pady=5)
            
            argomento_label = ctk.CTkLabel(
                argomento_frame,
                text=f"Argomento: {note.get('argomento', 'N/A')}",
                font=ctk.CTkFont(size=14, weight="bold"),
                anchor="w"
            )
            argomento_label.pack(fill="x")
            
            # Descrizione (se milestone)
            if note.get('tipo') == 'milestone' and note.get('descrizione'):
                desc_label = ctk.CTkLabel(
                    argomento_frame,
                    text=f"Dettagli: {note['descrizione']}",
                    font=ctk.CTkFont(size=12),
                    text_color="gray",
                    anchor="w",
                    wraplength=500
                )
                desc_label.pack(fill="x", pady=(5, 0))
            
            # Info durata e ore totali
            info_frame = ctk.CTkFrame(note_frame, fg_color="transparent")
            info_frame.pack(fill="x", padx=15, pady=5)
            
            if note.get('tipo') == 'sessione':
                durata_text = f"Durata sessione: {note.get('durata_sessione', 0)} min"
            else:
                durata_text = "Milestone completata"
            
            durata_label = ctk.CTkLabel(
                info_frame,
                text=durata_text,
                font=ctk.CTkFont(size=12)
            )
            durata_label.pack(side="left")
            
            ore_totali = note.get('ore_totali_materia', 0)
            ore_text = f"Ore totali materia: {ore_totali:.1f}h"
            
            ore_label = ctk.CTkLabel(
                info_frame,
                text=ore_text,
                font=ctk.CTkFont(size=12),
                text_color="#3b82f6"
            )
            ore_label.pack(side="right")
            
            # Pulsante elimina (solo per l'utente)
            delete_btn = ctk.CTkButton(
                note_frame,
                text="Elimina",
                command=lambda: self.delete_note(note['id']),
                height=25,
                width=80,
                fg_color="#dc3545",
                hover_color="#c82333",
                font=ctk.CTkFont(size=12)
            )
            delete_btn.pack(side="right", padx=15, pady=(0, 15))
            
        except Exception as e:
            print(f"Errore creazione widget nota: {e}")
    
    def update_stats(self, materia_filter=None):
        """Aggiorna le statistiche nella sidebar"""
        try:
            # Pulisce il contenitore statistiche
            for widget in self.stats_container.winfo_children():
                widget.destroy()
            
            if materia_filter and materia_filter in self.subjects_list:
                # Statistiche per materia specifica
                stats = self.progress_manager.get_subject_statistics(self.current_user, materia_filter)
                self._create_subject_stats_widget(stats)
            else:
                # Statistiche generali per tutte le materie
                self._create_general_stats_widget()
                
        except Exception as e:
            print(f"Errore aggiornamento statistiche: {e}")
    
    def _create_subject_stats_widget(self, stats):
        """Crea widget statistiche per materia specifica"""
        title = ctk.CTkLabel(
            self.stats_container,
            text=f"Statistiche {stats['materia']}",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Statistiche principali
        stats_text = f"""
Ore Totali: {stats.get('ore_totali', 0)}h

Sessioni Totali: {stats.get('sessioni_totali', 0)}

Argomenti Studiati: {stats.get('argomenti_studiati', 0)}

Milestone: {stats.get('milestone_completate', 0)}

Copertura Note: {stats.get('copertura_note', 0)}%

Tempo Medio/Argomento: {stats.get('tempo_medio_per_argomento', 0):.1f}h
        """
        
        stats_label = ctk.CTkLabel(
            self.stats_container,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            justify="left"
        )
        stats_label.pack(fill="x", padx=10)
    
    def _create_general_stats_widget(self):
        """Crea widget statistiche generali"""
        title = ctk.CTkLabel(
            self.stats_container,
            text="Statistiche Generali",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title.pack(pady=(10, 20))
        
        # Calcola statistiche per tutte le materie
        all_notes = self.progress_manager.get_user_notes(self.current_user)
        
        total_notes = len(all_notes)
        session_notes = len([n for n in all_notes if n.get('tipo') == 'sessione'])
        milestone_notes = len([n for n in all_notes if n.get('tipo') == 'milestone'])
        
        # Materie con note
        materie_con_note = len(set(n.get('materia', '') for n in all_notes if n.get('materia')))
        
        # Attività recente (ultimi 7 giorni)
        recent_activity = self.progress_manager.get_recent_activity(self.current_user, 7)
        
        stats_text = f"""
Note Totali: {total_notes}

Note Sessioni: {session_notes}

Milestone: {milestone_notes}

Materie Attive: {materie_con_note}

Attività (7 giorni): {len(recent_activity)}
        """
        
        stats_label = ctk.CTkLabel(
            self.stats_container,
            text=stats_text,
            font=ctk.CTkFont(size=12),
            anchor="w",
            justify="left"
        )
        stats_label.pack(fill="x", padx=10)
    
    def on_filter_change(self, selected_materia):
        """Callback per cambio filtro materia"""
        self.load_notes()
    
    def show_add_milestone(self):
        """Mostra finestra per aggiungere milestone"""
        milestone_dialog = MilestoneDialog(self.window, self.current_user, self.subjects_list)
        self.window.wait_window(milestone_dialog.dialog)
        
        # Ricarica le note se è stata aggiunta una milestone
        if hasattr(milestone_dialog, 'milestone_added') and milestone_dialog.milestone_added:
            self.load_notes()
    
    def delete_note(self, note_id):
        """Elimina una nota"""
        try:
            if messagebox.askyesno("Conferma", "Sei sicuro di voler eliminare questa nota?"):
                success = self.progress_manager.delete_note(note_id)
                if success:
                    messagebox.showinfo("Successo", "Nota eliminata!")
                    self.load_notes()  # Ricarica la lista
                else:
                    messagebox.showerror("Errore", "Errore nell'eliminazione della nota!")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore eliminazione!\\n\\nDettagli: {e}")


class MilestoneDialog(AeroStyleMixin):
    """Finestra di dialogo per aggiungere milestone manuali - Design Aero"""
    
    def __init__(self, parent, user, subjects_list):
        self.user = user
        self.subjects_list = subjects_list if subjects_list else ["Nessuna materia disponibile"]
        self.milestone_added = False
        self.colors = self.get_aero_colors()
        
        # Crea finestra dialogo con design Aero
        self.dialog = ctk.CTkToplevel(parent)
        self.dialog.title("🏆 Aggiungi Milestone")
        self.dialog.geometry("650x700")
        self.dialog.resizable(True, True)
        self.dialog.minsize(600, 650)
        
        # Configura griglia
        self.dialog.grid_rowconfigure(0, weight=1)
        self.dialog.grid_columnconfigure(0, weight=1)
        
        # Centra e rende modale
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.setup_ui()
        self.center_window()
    
    def center_window(self):
        """Centra la finestra"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        pos_x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        pos_y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f"{width}x{height}+{pos_x}+{pos_y}")
        
    def setup_ui(self):
        """Crea l'interfaccia del dialogo milestone con design Aero"""
        
        # Frame principale con gradient Aero
        main_frame = ctk.CTkFrame(
            self.dialog,
            corner_radius=20,
            fg_color=self.colors['glass_bg'],
            border_width=2,
            border_color=self.colors['border_light']
        )
        main_frame.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_frame.grid_rowconfigure(1, weight=1)  # Solo il contenuto scrollabile si espande
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header con effetto glass
        header_frame = self.create_aero_header(
            main_frame, 
            "Aggiungi Milestone", 
            "🏆", 
            "warning_orange"
        )
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Scrollable frame per contenuto (senza i pulsanti)
        scroll_frame = ctk.CTkScrollableFrame(
            main_frame,
            corner_radius=16,
            fg_color=self.colors['card_bg'],
            scrollbar_fg_color=self.colors['border_light']
        )
        scroll_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(10, 0))
        scroll_frame.grid_columnconfigure(0, weight=1)
        
        # Footer fisso per i pulsanti
        footer_frame = ctk.CTkFrame(
            main_frame,
            corner_radius=16,
            height=90,
            fg_color=self.colors['glass_bg'],
            border_width=1,
            border_color=self.colors['border_light']
        )
        footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        footer_frame.grid_propagate(False)
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # === INFO CARD ===
        info_card, info_content = self.create_aero_card(
            scroll_frame, 
            "Informazioni Milestone", 
            "💡", 
            "cyan_academic"
        )
        info_card.pack(fill="x", pady=15, padx=10)
        
        help_text = ctk.CTkLabel(
            info_content,
            text="🎯 Le milestone segnano traguardi importanti nel tuo percorso di apprendimento.\n\n"
                 "📊 Vengono visualizzate nella timeline del Registro Argomenti.\n"
                 "🏆 Aiutano a tracciare i progressi e celebrare i successi.",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['text_secondary'],
            justify="left"
        )
        help_text.pack(fill="x", pady=10)
        
        # === MATERIA CARD ===
        materia_card, materia_content = self.create_aero_card(
            scroll_frame, 
            "Materia di Studio", 
            "📚", 
            "primary_blue"
        )
        materia_card.pack(fill="x", pady=15, padx=10)
        
        self.materia_combo = ctk.CTkComboBox(
            materia_content,
            values=self.subjects_list,
            font=ctk.CTkFont(size=16),
            width=450,
            height=45,
            corner_radius=12,
            border_width=2,
            border_color=self.colors['border_light']
        )
        self.materia_combo.pack(pady=10)
        
        if self.subjects_list and self.subjects_list[0] != "Nessuna materia disponibile":
            self.materia_combo.set(self.subjects_list[0])
        
        # === ARGOMENTO CARD ===
        argomento_card, argomento_content = self.create_aero_card(
            scroll_frame, 
            "Traguardo Raggiunto", 
            "🎯", 
            "success_green"
        )
        argomento_card.pack(fill="x", pady=15, padx=10)
        
        # Helper text
        helper_argomento = ctk.CTkLabel(
            argomento_content,
            text="💭 Descrivi il traguardo che hai raggiunto:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['text_secondary']
        )
        helper_argomento.pack(pady=(5, 10))
        
        self.argomento_entry = ctk.CTkEntry(
            argomento_content,
            placeholder_text="es. Completato Capitolo 5 - Reti Neurali, Superato Esame Intermedio, etc.",
            font=ctk.CTkFont(size=16),
            width=500,
            height=45,
            corner_radius=12,
            border_width=2
        )
        self.argomento_entry.pack(pady=(0, 10))
        
        # === DESCRIZIONE CARD ===
        desc_card, desc_content = self.create_aero_card(
            scroll_frame, 
            "Dettagli (Opzionale)", 
            "📝", 
            "purple_creative"
        )
        desc_card.pack(fill="x", pady=15, padx=10)
        
        # Helper text
        helper_desc = ctk.CTkLabel(
            desc_content,
            text="✍️ Aggiungi dettagli, riflessioni o note sul traguardo:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors['text_secondary']
        )
        helper_desc.pack(pady=(5, 10))
        
        self.desc_textbox = ctk.CTkTextbox(
            desc_content,
            width=500,
            height=100,
            font=ctk.CTkFont(size=14),
            corner_radius=12,
            border_width=2
        )
        self.desc_textbox.pack(pady=(0, 10))
        
        # === PULSANTI NEL FOOTER FISSO ===
        # Pulsanti sempre visibili nel footer
        buttons_container = ctk.CTkFrame(footer_frame, fg_color="transparent")
        buttons_container.pack(expand=True)
        
        # Pulsante Salva - Principale
        save_btn = ctk.CTkButton(
            buttons_container,
            text="🏆 Salva Milestone",
            font=ctk.CTkFont(size=18, weight="bold"),
            width=200,
            height=50,
            corner_radius=25,
            fg_color=self.colors['success_green'],
            hover_color=("#047857", "#059669"),
            border_width=3,
            border_color=("#10b981", "#34d399"),
            command=self.save_milestone
        )
        save_btn.pack(side="left", padx=(0, 15))
        
        # Pulsante Annulla
        cancel_btn = ctk.CTkButton(
            buttons_container,
            text="❌ Annulla",
            font=ctk.CTkFont(size=16, weight="bold"),
            width=120,
            height=50,
            corner_radius=25,
            fg_color=self.colors['gray_neutral'],
            hover_color=("#4b5563", "#6b7280"),
            command=self.dialog.destroy
        )
        cancel_btn.pack(side="left")
    
    def save_milestone(self):
        """Salva la milestone"""
        try:
            # Validazioni
            materia = self.materia_combo.get()
            if not materia or materia == "Nessuna materia disponibile":
                messagebox.showerror("Errore", "Seleziona una materia valida!")
                return
            
            argomento = self.argomento_entry.get().strip()
            if not argomento:
                messagebox.showerror("Errore", "Inserisci l'argomento/traguardo!")
                return
            
            descrizione = self.desc_textbox.get("1.0", "end-1c").strip()
            
            # Salva milestone
            from progress_manager import ProgressManager
            progress_manager = ProgressManager()
            
            success = progress_manager.add_milestone_note(
                user=self.user,
                materia=materia,
                argomento=argomento,
                descrizione=descrizione if descrizione else None
            )
            
            if success:
                self.milestone_added = True
                messagebox.showinfo("Successo", f"Milestone salvata!\\n\\nMateria: {materia}\\nArgomento: {argomento}")
                self.dialog.destroy()
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio della milestone!")
                
        except Exception as e:
            messagebox.showerror("Errore", f"Errore salvataggio milestone!\\n\\nDettagli: {e}")