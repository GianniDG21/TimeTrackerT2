"""
Utilità e funzioni aggiuntive per TimeTrackerT GUI
Include: generazione statistiche, validazione dati, helper functions
"""

import json
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import dataM
# import user # Rimosso - ora gestito da user_manager

class StatsCalculator:
    """Classe per calcolare statistiche avanzate delle sessioni"""
    
    @staticmethod
    def calculate_session_stats(sessions):
        """Calcola statistiche complete dalle sessioni"""
        if not sessions:
            return {
                'total_sessions': 0,
                'total_minutes': 0,
                'total_hours': 0.0,
                'average_session': 0.0,
                'favorite_subject': 'N/A',
                'subjects_stats': {},
                'daily_stats': {},
                'weekly_total': 0,
                'this_month': 0
            }
        
        # Statistiche di base
        total_sessions = len(sessions)
        total_minutes = sum(s.get('durata', 0) for s in sessions)
        total_hours = total_minutes / 60
        average_session = total_minutes / total_sessions if total_sessions > 0 else 0
        
        # Statistiche per materia
        subjects_stats = defaultdict(lambda: {'minutes': 0, 'sessions': 0})
        for session in sessions:
            subject = session.get('materia', 'Sconosciuto')
            duration = session.get('durata', 0)
            subjects_stats[subject]['minutes'] += duration
            subjects_stats[subject]['sessions'] += 1
        
        # Materia preferita (più minuti studiati)
        favorite_subject = 'N/A'
        if subjects_stats:
            favorite_subject = max(subjects_stats.keys(), 
                                 key=lambda s: subjects_stats[s]['minutes'])
        
        # Statistiche temporali
        now = datetime.now()
        week_start = now - timedelta(days=7)
        month_start = now - timedelta(days=30)
        
        weekly_total = 0
        monthly_total = 0
        daily_stats = defaultdict(int)
        
        for session in sessions:
            try:
                timestamp_str = session.get('timestamp', '')
                session_date = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
                duration = session.get('durata', 0)
                
                # Statistiche settimanali
                if session_date >= week_start:
                    weekly_total += duration
                
                # Statistiche mensili
                if session_date >= month_start:
                    monthly_total += duration
                
                # Statistiche giornaliere (ultimi 7 giorni)
                if session_date >= week_start:
                    day_key = session_date.strftime("%Y-%m-%d")
                    daily_stats[day_key] += duration
                    
            except ValueError:
                continue  # Ignora timestamp malformati
        
        return {
            'total_sessions': total_sessions,
            'total_minutes': total_minutes,
            'total_hours': total_hours,
            'average_session': average_session,
            'favorite_subject': favorite_subject,
            'subjects_stats': dict(subjects_stats),
            'daily_stats': dict(daily_stats),
            'weekly_total': weekly_total,
            'monthly_total': monthly_total
        }

    @staticmethod
    def get_productivity_insights(sessions):
        """Genera insights di produttività"""
        if not sessions or len(sessions) < 5:
            return ["Accumula più sessioni per vedere insights personalizzati! 📊"]
        
        stats = StatsCalculator.calculate_session_stats(sessions)
        insights = []
        
        # Insight sulla consistenza
        if stats['weekly_total'] > 0:
            daily_avg = stats['weekly_total'] / 7
            if daily_avg >= 60:
                insights.append(f"🔥 Ottima consistenza! Studi in media {daily_avg:.0f} minuti al giorno")
            elif daily_avg >= 30:
                insights.append(f"👍 Buona costanza con {daily_avg:.0f} minuti giornalieri")
            else:
                insights.append(f"💡 Prova ad aumentare la costanza: {daily_avg:.0f} min/giorno")
        
        # Insight sulla durata sessioni
        avg_session = stats['average_session']
        if avg_session >= 45:
            insights.append("🎯 Eccellente focus! Sessioni lunghe e produttive")
        elif avg_session >= 25:
            insights.append("⚡ Buon ritmo di studio con sessioni equilibrate")
        else:
            insights.append("🚀 Prova sessioni più lunghe per maggiore concentrazione")
        
        # Insight sulla varietà
        subjects_count = len(stats['subjects_stats'])
        if subjects_count >= 4:
            insights.append("🌟 Ottima varietà di studio! Mantieni l'equilibrio")
        elif subjects_count >= 2:
            insights.append("📚 Buona diversificazione delle materie")
        else:
            insights.append("🎨 Considera di aggiungere più materie per varietà")
        
        # Insight temporale
        recent_sessions = [s for s in sessions[-7:]]  # Ultime 7 sessioni
        if len(recent_sessions) >= 5:
            insights.append("🚀 Sei in un ottimo periodo produttivo!")
        elif len(recent_sessions) >= 3:
            insights.append("📈 Stai mantenendo un buon ritmo di studio")
        
        return insights[:3]  # Massimo 3 insights

class DataValidator:
    """Classe per validare e sanificare i dati"""
    
    @staticmethod
    def validate_session_data(sessions):
        """Valida e corregge i dati delle sessioni"""
        if not sessions:
            return []
        
        validated = []
        for session in sessions:
            # Controlla che abbia i campi essenziali
            if not all(key in session for key in ['id', 'user', 'materia', 'durata']):
                continue
            
            # Valida durata
            try:
                duration = int(session['durata'])
                if duration < 0:
                    continue
                session['durata'] = duration
            except (ValueError, TypeError):
                continue
            
            # Valida timestamp
            try:
                if 'timestamp' in session:
                    datetime.strptime(session['timestamp'], "%Y-%m-%d %H:%M:%S")
                else:
                    session['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                session['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            validated.append(session)
        
        return validated

    @staticmethod
    def validate_subject_name(name):
        """Valida il nome di una materia"""
        if not name or not isinstance(name, str):
            return False, "Il nome della materia non può essere vuoto"
        
        name = name.strip()
        if len(name) < 2:
            return False, "Il nome deve essere lungo almeno 2 caratteri"
        
        if len(name) > 50:
            return False, "Il nome non può superare 50 caratteri"
        
        # Caratteri non consentiti
        forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
        if any(char in name for char in forbidden_chars):
            return False, "Il nome contiene caratteri non consentiti"
        
        return True, name.strip()

class UIHelpers:
    """Funzioni helper per l'interfaccia utente"""
    
    @staticmethod
    def format_duration(minutes):
        """Formatta la durata in formato user-friendly"""
        if minutes < 60:
            return f"{minutes} min"
        elif minutes < 1440:  # Meno di 24 ore
            hours = minutes // 60
            mins = minutes % 60
            if mins == 0:
                return f"{hours}h"
            return f"{hours}h {mins}min"
        else:  # Più di 24 ore
            days = minutes // 1440
            remaining_hours = (minutes % 1440) // 60
            return f"{days}g {remaining_hours}h"
    
    @staticmethod
    def get_subject_emoji(subject_name):
        """Restituisce un emoji appropriato per la materia"""
        subject_lower = subject_name.lower()
        
        emoji_map = {
            'matematica': '🔢', 'math': '🔢', 'algebra': '🔢', 'geometria': '📐',
            'fisica': '⚛️', 'chimica': '🧪', 'biologia': '🧬', 'scienze': '🔬',
            'italiano': '🇮🇹', 'inglese': '🇬🇧', 'francese': '🇫🇷', 'spagnolo': '🇪🇸',
            'storia': '📜', 'geografia': '🗺️', 'filosofia': '🤔', 'letteratura': '📚',
            'programmazione': '💻', 'coding': '💻', 'python': '🐍', 'java': '☕',
            'web': '🌐', 'html': '📝', 'css': '🎨', 'javascript': '📜',
            'database': '🗄️', 'sql': '🗄️', 'bdd': '🗄️',
            'economia': '💰', 'diritto': '⚖️', 'psicologia': '🧠',
            'arte': '🎨', 'musica': '🎵', 'sport': '⚽', 'fitness': '💪',
            'studio': '📖', 'lettura': '📚', 'ricerca': '🔍',
            'golang': '🐹', 'go': '🐹', 'rust': '🦀', 'c++': '⚙️',
            'analisi': '📊', 'dati': '📊', 'analisidati': '📊',
            'sistemi': '🖥️', 'reti': '🌐', 'sicurezza': '🔒',
            'gioco': '🎮', 'game': '🎮', 'hobby': '🎯'
        }
        
        for keyword, emoji in emoji_map.items():
            if keyword in subject_lower:
                return emoji
        
        return '📚'  # Emoji default
    
    @staticmethod
    def get_motivation_message():
        """Restituisce un messaggio motivazionale casuale"""
        messages = [
            "🌟 Ogni sessione di studio è un passo verso il successo!",
            "💪 La costanza è la chiave del progresso!",
            "🎯 Concentrati sul tuo obiettivo, sei sulla strada giusta!",
            "🚀 Ogni minuto investito nello studio è un investimento nel tuo futuro!",
            "⭐ Il sapere è l'unico tesoro che nessuno può rubarti!",
            "🔥 La disciplina è libertà attraverso l'autodeterminazione!",
            "💎 La conoscenza è il più prezioso dei tesori!",
            "🌈 Il successo è la somma di piccoli sforzi ripetuti giorno dopo giorno!",
            "🎪 Impara qualcosa di nuovo ogni giorno!",
            "🏆 L'eccellenza è un'abitudine, non un atto!"
        ]
        
        import random
        return random.choice(messages)
    
    @staticmethod
    def format_timestamp(timestamp_str):
        """Formatta un timestamp per la visualizzazione"""
        try:
            dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")
            now = datetime.now()
            
            # Se è oggi
            if dt.date() == now.date():
                return f"Oggi alle {dt.strftime('%H:%M')}"
            
            # Se è ieri
            yesterday = now.date() - timedelta(days=1)
            if dt.date() == yesterday:
                return f"Ieri alle {dt.strftime('%H:%M')}"
            
            # Se è questa settimana
            days_ago = (now.date() - dt.date()).days
            if days_ago <= 7:
                weekdays = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 
                           'Venerdì', 'Sabato', 'Domenica']
                weekday = weekdays[dt.weekday()]
                return f"{weekday} alle {dt.strftime('%H:%M')}"
            
            # Formato standard per date più vecchie
            return dt.strftime("%d/%m/%Y alle %H:%M")
            
        except ValueError:
            return timestamp_str  # Fallback al timestamp originale

class ConfigManager:
    """Gestione configurazioni dell'applicazione"""
    
    CONFIG_FILE = "config.json"
    
    DEFAULT_CONFIG = {
        "appearance": {
            "theme": "dark",
            "color_scheme": "blue"
        },
        "timer": {
            "default_duration": 25,
            "auto_start": True,
            "sound_enabled": True,
            "break_reminder": True
        },
        "ui": {
            "window_size": "800x600",
            "remember_position": True,
            "show_motivational_quotes": True
        },
        "presets": {
            "durations": [15, 25, 45, 60, 90]
        }
    }
    
    @classmethod
    def load_config(cls):
        """Carica la configurazione"""
        try:
            with open(cls.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            # Merge con configurazione default per nuove opzioni
            return cls._merge_configs(cls.DEFAULT_CONFIG, config)
        except (FileNotFoundError, json.JSONDecodeError):
            return cls.DEFAULT_CONFIG.copy()
    
    @classmethod
    def save_config(cls, config):
        """Salva la configurazione"""
        try:
            with open(cls.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Errore nel salvataggio configurazione: {e}")
            return False
    
    @classmethod
    def _merge_configs(cls, default, user):
        """Merge configurazione utente con quella default"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = cls._merge_configs(result[key], value)
            else:
                result[key] = value
        return result