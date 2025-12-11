"""
Gestore obiettivi di studio per TimeTrackerT2
Gestisce creazione, salvataggio, caricamento e controllo progresso obiettivi
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import dataM  # Per accedere alle sessioni di studio


class GoalsManager:
    """Gestisce gli obiettivi di studio degli utenti"""
    
    def __init__(self):
        self.goals_file = "goals.json"
        self.goals = self._load_goals()
    
    def _load_goals(self) -> List[Dict]:
        """Carica gli obiettivi dal file JSON"""
        try:
            if os.path.exists(self.goals_file):
                with open(self.goals_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Errore caricamento obiettivi: {e}")
            return []
    
    def _save_goals(self) -> bool:
        """Salva gli obiettivi nel file JSON"""
        try:
            with open(self.goals_file, 'w', encoding='utf-8') as f:
                json.dump(self.goals, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Errore salvataggio obiettivi: {e}")
            return False
    
    def create_goal(self, user: str, materia: str, ore_target: int, 
                   minuti_target: int, intervallo: str) -> bool:
        """Crea un nuovo obiettivo"""
        try:
            # Calcola tempo target totale in minuti
            tempo_target_minuti = ore_target * 60 + minuti_target
            
            if tempo_target_minuti <= 0:
                return False
            
            # Genera ID unico
            goal_id = max([g.get('id', 0) for g in self.goals], default=0) + 1
            
            nuovo_obiettivo = {
                'id': goal_id,
                'user': user,
                'materia': materia,
                'ore_target': ore_target,
                'minuti_target': minuti_target,
                'tempo_target_minuti': tempo_target_minuti,
                'intervallo': intervallo,  # 'giorno', 'settimana', 'mese'
                'data_creazione': datetime.now().isoformat(),
                'completato': False,
                'data_completamento': None
            }
            
            self.goals.append(nuovo_obiettivo)
            return self._save_goals()
            
        except Exception as e:
            print(f"Errore creazione obiettivo: {e}")
            return False
    
    def get_user_goals(self, user: str) -> List[Dict]:
        """Ottieni tutti gli obiettivi di un utente"""
        return [goal for goal in self.goals if goal.get('user') == user]
    
    def delete_goal(self, goal_id: int) -> bool:
        """Elimina un obiettivo"""
        try:
            self.goals = [goal for goal in self.goals if goal.get('id') != goal_id]
            return self._save_goals()
        except Exception as e:
            print(f"Errore eliminazione obiettivo: {e}")
            return False
    
    def _get_period_start_date(self, intervallo: str) -> datetime:
        """Calcola la data di inizio del periodo in base all'intervallo"""
        now = datetime.now()
        
        if intervallo == 'giorno':
            return now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif intervallo == 'settimana':
            # Inizio settimana (Lunedì)
            days_since_monday = now.weekday()
            start_week = now - timedelta(days=days_since_monday)
            return start_week.replace(hour=0, minute=0, second=0, microsecond=0)
        elif intervallo == 'mese':
            # Inizio mese
            return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        else:
            return now
    
    def calculate_progress(self, user: str, goal: Dict) -> Tuple[int, int, float]:
        """
        Calcola il progresso di un obiettivo
        Ritorna: (minuti_studiati, minuti_target, percentuale_completamento)
        """
        try:
            # Carica le sessioni dell'utente
            sessions = dataM.load_sessions(user)
            if not sessions:
                return 0, goal['tempo_target_minuti'], 0.0
            
            # Calcola periodo di riferimento
            period_start = self._get_period_start_date(goal['intervallo'])
            
            # Filtra sessioni per materia e periodo
            materia_target = goal['materia']
            minuti_studiati = 0
            
            for session in sessions:
                # Controlla se è la materia giusta
                if session.get('materia') != materia_target:
                    continue
                
                # Controlla se è nel periodo giusto
                session_date = self._parse_session_date(session)
                if session_date and session_date >= period_start:
                    minuti_studiati += session.get('durata', 0)
            
            tempo_target = goal['tempo_target_minuti']
            percentuale = min(100.0, (minuti_studiati / tempo_target * 100)) if tempo_target > 0 else 0.0
            
            return minuti_studiati, tempo_target, percentuale
            
        except Exception as e:
            print(f"Errore calcolo progresso: {e}")
            return 0, goal.get('tempo_target_minuti', 0), 0.0
    
    def _parse_session_date(self, session: Dict) -> Optional[datetime]:
        """Estrae la data da una sessione"""
        try:
            timestamp = session.get('timestamp')
            if not timestamp:
                return None
            
            # Prova diversi formati di timestamp
            formats = [
                '%Y-%m-%d %H:%M:%S',
                '%Y-%m-%d %H:%M:%S.%f',
                '%d/%m/%Y %H:%M:%S',
                '%d/%m/%Y %H:%M'
            ]
            
            for fmt in formats:
                try:
                    return datetime.strptime(timestamp, fmt)
                except ValueError:
                    continue
            
            return None
            
        except Exception:
            return None
    
    def check_completed_goals(self, user: str) -> List[Dict]:
        """
        Controlla se ci sono obiettivi appena completati
        Ritorna la lista di obiettivi appena raggiunti
        """
        newly_completed = []
        user_goals = self.get_user_goals(user)
        
        for goal in user_goals:
            if goal.get('completato'):
                continue  # Già completato prima
            
            # Calcola progresso attuale
            minuti_studiati, minuti_target, percentuale = self.calculate_progress(user, goal)
            
            # Se raggiunto il target, marca come completato
            if minuti_studiati >= minuti_target:
                goal['completato'] = True
                goal['data_completamento'] = datetime.now().isoformat()
                newly_completed.append(goal)
        
        # Salva i cambiamenti se ci sono obiettivi completati
        if newly_completed:
            self._save_goals()
        
        return newly_completed
    
    def format_time(self, minuti: int) -> str:
        """Formatta i minuti in ore e minuti leggibili"""
        if minuti < 60:
            return f"{minuti}min"
        else:
            ore = minuti // 60
            min_restanti = minuti % 60
            if min_restanti == 0:
                return f"{ore}h"
            else:
                return f"{ore}h {min_restanti}min"
    
    def get_goal_status_color(self, percentuale: float) -> str:
        """Ritorna il colore appropriato per lo stato dell'obiettivo"""
        if percentuale >= 100:
            return "#28a745"  # Verde - Completato
        elif percentuale >= 75:
            return "#ffc107"  # Giallo - Quasi completato
        elif percentuale >= 50:
            return "#fd7e14"  # Arancione - A metà
        else:
            return "#6c757d"  # Grigio - Appena iniziato