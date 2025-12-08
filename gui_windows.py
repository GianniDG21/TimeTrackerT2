"""
Finestre secondarie per TimeTrackerT GUI
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
import subj
import user
from gui_utils import StatsCalculator, UIHelpers, DataValidator

class NewSessionWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app.window)
        self.window.title("Nuova Sessione")
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # Rende la finestra modale
        self.window.transient(main_app.window)
        self.window.grab_set()
        
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
        """Configura l'interfaccia della finestra"""
        
        # Frame principale - Design moderno
        main_frame = ctk.CTkFrame(
            self.window, 
            corner_radius=15,
            fg_color=("#0e1621", "#0e1621"),
            border_width=1,
            border_color=("#1a1a2e", "#1a1a2e")
        )
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="🚀 Nuova Sessione di Studio",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 30))
        
        # Frame per la selezione materia
        subject_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        subject_frame.pack(fill="x", padx=20, pady=10)
        
        subject_label = ctk.CTkLabel(
            subject_frame,
            text="📚 Seleziona Materia:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        subject_label.pack(pady=(15, 5))
        
        # Carica le materie dell'utente
        self.load_subjects()
        
        self.subject_combo = ctk.CTkComboBox(
            subject_frame,
            values=self.subjects_list,
            font=ctk.CTkFont(size=14),
            width=300,
            height=35
        )
        self.subject_combo.pack(pady=(5, 15))
        
        if self.subjects_list:
            self.subject_combo.set(self.subjects_list[0])
        
        # Frame per la durata
        duration_frame = ctk.CTkFrame(main_frame, corner_radius=10)
        duration_frame.pack(fill="x", padx=20, pady=10)
        
        duration_label = ctk.CTkLabel(
            duration_frame,
            text="⏱️ Durata (minuti):",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        duration_label.pack(pady=(15, 5))
        
        # Entry per la durata
        self.duration_entry = ctk.CTkEntry(
            duration_frame,
            placeholder_text="es. 25, 45, 60...",
            font=ctk.CTkFont(size=14),
            width=300,
            height=35,
            justify="center"
        )
        self.duration_entry.pack(pady=(5, 10))
        
        # Pulsanti preset durata
        preset_frame = ctk.CTkFrame(duration_frame, fg_color="transparent")
        preset_frame.pack(pady=(0, 15))
        
        durations = [15, 25, 45, 60, 90]
        for duration in durations:
            btn = ctk.CTkButton(
                preset_frame,
                text=f"{duration}m",
                width=50,
                height=25,
                command=lambda d=duration: self.set_duration(d),
                font=ctk.CTkFont(size=12)
            )
            btn.pack(side="left", padx=5)
        
        # Frame per i pulsanti
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # Pulsante Avvia - Design elegante
        self.start_btn = ctk.CTkButton(
            button_frame,
            text="▶️ Avvia Sessione",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.start_session,
            height=40,
            width=150,
            fg_color=("#1f4e79", "#2563eb"),
            hover_color=("#1e40af", "#3b82f6"),
            border_width=1,
            border_color=("#3b82f6", "#60a5fa")
        )
        self.start_btn.pack(side="left", padx=(0, 10))
        
        # Pulsante Annulla
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="❌ Annulla",
            font=ctk.CTkFont(size=16, weight="bold"),
            command=self.window.destroy,
            height=40,
            width=150,
            fg_color="transparent",
            border_width=2
        )
        cancel_btn.pack(side="right")

    def load_subjects(self):
        """Carica le materie dell'utente"""
        try:
            subjects_data = dataM.load_subjects(user.act_user)
            self.subjects_list = subjects_data.get(user.act_user, [])
            
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

    def start_session(self):
        """Avvia una nuova sessione"""
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
        
        # Chiudi questa finestra e apri il timer
        self.window.destroy()
        
        # Avvia il timer nella finestra principale
        timer_window = TimerWindow(self.main_app, subject, duration)

class SessionHistoryWindow:
    def __init__(self, main_app):
        self.main_app = main_app
        self.window = ctk.CTkToplevel(main_app.window)
        self.window.title("Storico Sessioni")
        self.window.geometry("700x500")
        self.window.resizable(True, True)
        
        self.window.transient(main_app.window)
        self.window.grab_set()
        
        self.setup_ui()
        self.center_window()
        self.load_sessions()

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
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="📊 Storico Sessioni",
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
            sessions = dataM.load_sessions(user.act_user)
            
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
        self.window = ctk.CTkToplevel(main_app.window)
        self.window.title("Gestione Materie")
        self.window.geometry("600x500")
        self.window.resizable(True, True)
        
        self.window.transient(main_app.window)
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
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Titolo
        title_label = ctk.CTkLabel(
            main_frame,
            text="📚 Gestione Materie",
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
            subjects_data = dataM.load_subjects(user.act_user)
            subjects_list = subjects_data.get(user.act_user, [])
            
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
            subjects_data = dataM.load_subjects(user.act_user)
            subjects_list = subjects_data.get(user.act_user, [])
            
            if subject_name in subjects_list:
                messagebox.showwarning("Attenzione", "Questa materia esiste già!")
                return
            
            # Aggiungi la nuova materia
            subjects_list.append(subject_name)
            subjects_data[user.act_user] = subjects_list
            
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
            subjects_data = dataM.load_subjects(user.act_user)
            subjects_list = subjects_data.get(user.act_user, [])
            
            if subject in subjects_list:
                subjects_list.remove(subject)
                subjects_data[user.act_user] = subjects_list
                
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
        
        self.window = ctk.CTkToplevel(main_app.window)
        self.window.title(f"Timer - {subject}")
        self.window.geometry("600x400")
        self.window.resizable(False, False)
        
        self.window.transient(main_app.window)
        self.window.grab_set()
        
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
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
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
            
            success = dataM.save_session(user.act_user, self.subject, effective_duration)
            
            if success:
                self.main_app.update_status(
                    f"Sessione salvata: {self.subject} - {effective_duration} minuti"
                )
            else:
                messagebox.showerror("Errore", "Errore nel salvataggio della sessione!")
                
        except Exception as e:
            print(f"Errore nel salvataggio: {e}")
            messagebox.showerror("Errore", "Errore nel salvataggio della sessione!")