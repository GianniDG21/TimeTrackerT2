"""
Finestra di gestione utenti per TimeTrackerT2
Gestisce selezione utente all'avvio e creazione nuovo utente
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path

class UserSelectionWindow(ctk.CTkToplevel):
    def __init__(self, parent, callback):
        super().__init__(parent)
        
        self.callback = callback
        self.selected_user = None
        self.users_file = Path("users.txt")
        self.config_file = Path("user_config.json")
        
        self.setup_window()
        self.load_users()
        self.create_widgets()
        
        # Centra la finestra
        self.center_window()
        
        # Impedisce di chiudere senza selezione
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Focus e sempre in primo piano
        self.focus_set()
        self.grab_set()  # Finestra modale
        
    def setup_window(self):
        """Configura la finestra"""
        self.title("TimeTrackerT2 - Selezione Utente")
        self.geometry("450x500")
        self.resizable(False, False)
        
        # Tema scuro
        ctk.set_appearance_mode("dark")
        
    def center_window(self):
        """Centra la finestra sullo schermo"""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - self.winfo_width()) // 2
        y = (self.winfo_screenheight() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")
        
    def load_users(self):
        """Carica lista utenti e configurazione"""
        # Carica utenti
        self.users = []
        if self.users_file.exists():
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = [line.strip() for line in f if line.strip()]
                
        # Carica configurazione
        self.config = {"default_user": None, "auto_login": False}
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config.update(json.load(f))
            except:
                pass
                
    def save_config(self):
        """Salva configurazione utente"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Errore salvataggio config: {e}")
            
    def save_users(self):
        """Salva lista utenti"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                for user in self.users:
                    f.write(f"{user}\n")
        except Exception as e:
            print(f"Errore salvataggio utenti: {e}")
            
    def create_widgets(self):
        """Crea interfaccia"""
        # Header
        header_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_label = ctk.CTkLabel(
            header_frame,
            text="👤 Seleziona Utente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=("#ffffff", "#ffffff")
        )
        title_label.pack(expand=True)
        
        # Main content frame
        content_frame = ctk.CTkFrame(self, corner_radius=15)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Se non ci sono utenti, mostra creazione
        if not self.users:
            self.create_new_user_interface(content_frame)
        else:
            self.create_user_selection_interface(content_frame)
            
    def create_user_selection_interface(self, parent):
        """Interfaccia per selezione utente esistente"""
        # Lista utenti
        users_label = ctk.CTkLabel(
            parent,
            text="Seleziona il tuo utente:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        users_label.pack(pady=(20, 10))
        
        # Scrollable frame per utenti
        self.users_frame = ctk.CTkScrollableFrame(parent, height=200)
        self.users_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        # Radio buttons per utenti
        self.selected_user_var = tk.StringVar(value=self.config.get("default_user", ""))
        
        for user in self.users:
            user_frame = ctk.CTkFrame(self.users_frame)
            user_frame.pack(fill="x", pady=5)
            
            radio = ctk.CTkRadioButton(
                user_frame,
                text=f"👤 {user}",
                variable=self.selected_user_var,
                value=user,
                font=ctk.CTkFont(size=14)
            )
            radio.pack(side="left", padx=15, pady=10)
            
        # Checkbox utente predefinito
        self.default_user_var = tk.BooleanVar(value=self.config.get("auto_login", False))
        self.default_checkbox = ctk.CTkCheckBox(
            parent,
            text="🔄 Ricorda come utente predefinito",
            variable=self.default_user_var,
            font=ctk.CTkFont(size=12)
        )
        self.default_checkbox.pack(pady=10)
        
        # Pulsanti
        buttons_frame = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_frame.pack(fill="x", padx=20, pady=15)
        
        # Pulsante nuovo utente
        new_user_btn = ctk.CTkButton(
            buttons_frame,
            text="➕ Nuovo Utente",
            command=self.show_new_user_dialog,
            height=40,
            fg_color=("#1f4e79", "#2563eb"),
            hover_color=("#1e40af", "#3b82f6")
        )
        new_user_btn.pack(side="left", padx=(0, 10))
        
        # Pulsante conferma
        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="✅ Conferma",
            command=self.confirm_selection,
            height=40,
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e")
        )
        confirm_btn.pack(side="right")
        
    def create_new_user_interface(self, parent):
        """Interfaccia per creazione primo utente"""
        welcome_label = ctk.CTkLabel(
            parent,
            text="🎉 Benvenuto in TimeTrackerT2!",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        welcome_label.pack(pady=(30, 10))
        
        info_label = ctk.CTkLabel(
            parent,
            text="Per iniziare, crea il tuo primo utente:",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=(0, 20))
        
        # Input nome utente
        name_label = ctk.CTkLabel(
            parent,
            text="Nome Utente:",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        name_label.pack(pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Inserisci il tuo nome...",
            height=40,
            font=ctk.CTkFont(size=14),
            corner_radius=10
        )
        self.name_entry.pack(fill="x", padx=40, pady=(0, 20))
        self.name_entry.focus_set()
        
        # Pulsante crea
        create_btn = ctk.CTkButton(
            parent,
            text="🚀 Crea Utente",
            command=self.create_first_user,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color=("#166534", "#16a34a"),
            hover_color=("#15803d", "#22c55e")
        )
        create_btn.pack(pady=20)
        
        # Bind Enter per creazione rapida
        self.name_entry.bind("<Return>", lambda e: self.create_first_user())
        
    def show_new_user_dialog(self):
        """Mostra dialog per nuovo utente"""
        dialog = ctk.CTkInputDialog(
            text="Inserisci nome del nuovo utente:",
            title="Nuovo Utente"
        )
        
        new_name = dialog.get_input()
        if new_name and new_name.strip():
            new_name = new_name.strip()
            if new_name not in self.users:
                self.users.append(new_name)
                self.save_users()
                
                # Ricarica interfaccia
                for widget in self.winfo_children():
                    if isinstance(widget, ctk.CTkFrame):
                        widget.destroy()
                        
                self.create_widgets()
                messagebox.showinfo("Successo", f"Utente '{new_name}' creato!")
            else:
                messagebox.showwarning("Attenzione", "Utente già esistente!")
                
    def create_first_user(self):
        """Crea il primo utente"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showwarning("Attenzione", "Inserisci un nome utente!")
            self.name_entry.focus_set()
            return
            
        # Crea utente
        self.users = [name]
        self.save_users()
        
        # Imposta come predefinito
        self.config["default_user"] = name
        self.config["auto_login"] = True
        self.save_config()
        
        # Conferma selezione
        self.selected_user = name
        self.close_window()
        
    def confirm_selection(self):
        """Conferma selezione utente"""
        selected = self.selected_user_var.get()
        if not selected:
            messagebox.showwarning("Attenzione", "Seleziona un utente!")
            return
            
        # Salva configurazione
        if self.default_user_var.get():
            self.config["default_user"] = selected
            self.config["auto_login"] = True
        else:
            self.config["default_user"] = None
            self.config["auto_login"] = False
            
        self.save_config()
        
        self.selected_user = selected
        self.close_window()
        
    def close_window(self):
        """Chiude la finestra e ritorna il risultato"""
        if self.selected_user:
            self.callback(self.selected_user)
            self.destroy()
        
    def on_closing(self):
        """Gestisce chiusura finestra"""
        if self.selected_user:
            self.close_window()
        else:
            # Non permette di chiudere senza selezione
            messagebox.showwarning(
                "Attenzione", 
                "Devi selezionare un utente per continuare!"
            )

class UserManager:
    """Gestore utenti per l'applicazione principale"""
    
    @staticmethod
    def get_current_user(parent_window=None):
        """
        Ottiene l'utente corrente.
        Se configurato auto-login, usa quello.
        Altrimenti mostra finestra selezione.
        """
        config_file = Path("user_config.json")
        users_file = Path("users.txt")
        
        # Carica configurazione
        config = {"default_user": None, "auto_login": False}
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config.update(json.load(f))
            except:
                pass
                
        # Carica utenti
        users = []
        if users_file.exists():
            with open(users_file, 'r', encoding='utf-8') as f:
                users = [line.strip() for line in f if line.strip()]
                
        # Se auto-login e utente predefinito esiste
        if (config.get("auto_login") and 
            config.get("default_user") and 
            config["default_user"] in users):
            return config["default_user"]
            
        # Altrimenti mostra selezione
        result = {"user": None}
        
        def user_selected(user):
            result["user"] = user
            
        # Crea finestra selezione (modale)
        if parent_window:
            selection_window = UserSelectionWindow(parent_window, user_selected)
            parent_window.wait_window(selection_window)
        else:
            # Crea finestra temporanea se non c'è parent
            temp_root = ctk.CTk()
            temp_root.withdraw()  # Nasconde finestra principale temporanea
            selection_window = UserSelectionWindow(temp_root, user_selected)
            temp_root.wait_window(selection_window)
            temp_root.destroy()
            
        return result["user"]