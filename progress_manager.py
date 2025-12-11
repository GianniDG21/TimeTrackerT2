"""
Gestore note di progresso per TimeTrackerT2
Gestisce le note sugli argomenti studiati e il tempo speso per ciascun argomento
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import dataM  # Per accedere alle sessioni


class ProgressManager:
    """Gestisce le note di progresso e argomenti studiati"""
    
    def __init__(self):
        self.notes_file = "progress_notes.json"
        self.notes = self._load_notes()
    
    def _load_notes(self) -> List[Dict]:
        """Carica le note dal file JSON"""
        try:
            if os.path.exists(self.notes_file):
                with open(self.notes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Errore caricamento note: {e}")
            return []
    
    def _save_notes(self) -> bool:
        """Salva le note nel file JSON"""
        try:
            with open(self.notes_file, 'w', encoding='utf-8') as f:
                json.dump(self.notes, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Errore salvataggio note: {e}")
            return False
    
    def add_session_note(self, user: str, materia: str, argomento: str, 
                        durata_sessione: int, session_id: Optional[int] = None) -> bool:
        """
        Aggiunge una nota collegata a una sessione specifica
        
        Args:
            user: Nome utente
            materia: Materia studiata
            argomento: Descrizione argomento completato/studiato
            durata_sessione: Durata della sessione in minuti
            session_id: ID della sessione (opzionale)
        """
        try:
            # Calcola ore totali per questa materia fino ad ora
            ore_totali_materia = self._calculate_total_subject_hours(user, materia)
            
            # Genera ID unico per la nota
            note_id = max([note.get('id', 0) for note in self.notes], default=0) + 1
            
            new_note = {
                'id': note_id,
                'user': user,
                'materia': materia,
                'argomento': argomento,
                'durata_sessione': durata_sessione,
                'ore_totali_materia': round(ore_totali_materia, 2),
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'tipo': 'sessione'  # Tipo di nota
            }
            
            self.notes.append(new_note)
            return self._save_notes()
            
        except Exception as e:
            print(f"Errore aggiunta nota sessione: {e}")
            return False
    
    def add_milestone_note(self, user: str, materia: str, argomento: str, 
                          descrizione: Optional[str] = None) -> bool:
        """
        Aggiunge una nota milestone (traguardo completato)
        
        Args:
            user: Nome utente  
            materia: Materia
            argomento: Titolo del traguardo/argomento completato
            descrizione: Descrizione opzionale dettagliata
        """
        try:
            ore_totali_materia = self._calculate_total_subject_hours(user, materia)
            note_id = max([note.get('id', 0) for note in self.notes], default=0) + 1
            
            new_note = {
                'id': note_id,
                'user': user,
                'materia': materia,
                'argomento': argomento,
                'descrizione': descrizione or "",
                'ore_totali_materia': round(ore_totali_materia, 2),
                'timestamp': datetime.now().isoformat(),
                'tipo': 'milestone'
            }
            
            self.notes.append(new_note)
            return self._save_notes()
            
        except Exception as e:
            print(f"Errore aggiunta milestone: {e}")
            return False
    
    def get_user_notes(self, user: str, materia: Optional[str] = None) -> List[Dict]:
        """Ottieni tutte le note di un utente, opzionalmente filtrate per materia"""
        user_notes = [note for note in self.notes if note.get('user') == user]
        
        if materia:
            user_notes = [note for note in user_notes if note.get('materia') == materia]
        
        # Ordina per timestamp (più recenti prima)
        user_notes.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return user_notes
    
    def get_subject_timeline(self, user: str, materia: str) -> List[Dict]:
        """Ottieni timeline completa di una materia con note e statistiche"""
        notes = self.get_user_notes(user, materia)
        
        # Aggiungi statistiche per ogni nota
        for note in notes:
            if note.get('tipo') == 'sessione':
                note['tempo_formattato'] = self._format_time(note.get('durata_sessione', 0))
            note['ore_totali_formattate'] = self._format_time(int(note.get('ore_totali_materia', 0) * 60))
        
        return notes
    
    def get_subject_statistics(self, user: str, materia: str) -> Dict:
        """Ottieni statistiche complete per una materia"""
        try:
            # Carica tutte le sessioni per calcoli
            sessions = dataM.load_sessions(user)
            subject_sessions = [s for s in sessions if s.get('materia') == materia]
            
            # Carica le note
            notes = self.get_user_notes(user, materia)
            session_notes = [n for n in notes if n.get('tipo') == 'sessione']
            milestone_notes = [n for n in notes if n.get('tipo') == 'milestone']
            
            # Calcoli base
            total_sessions = len(subject_sessions)
            total_hours = sum(s.get('durata', 0) for s in subject_sessions) / 60
            sessions_with_notes = len(session_notes)
            
            # Argomenti unici studiati
            argomenti_unici = len(set(n.get('argomento', '') for n in notes if n.get('argomento')))
            
            # Tempo medio per argomento (approssimativo)
            tempo_medio_argomento = total_hours / max(argomenti_unici, 1)
            
            # Milestone completate
            milestone_count = len(milestone_notes)
            
            return {
                'materia': materia,
                'sessioni_totali': total_sessions,
                'ore_totali': round(total_hours, 2),
                'sessioni_con_note': sessions_with_notes,
                'copertura_note': round((sessions_with_notes / max(total_sessions, 1)) * 100, 1),
                'argomenti_studiati': argomenti_unici,
                'milestone_completate': milestone_count,
                'tempo_medio_per_argomento': round(tempo_medio_argomento, 2),
                'ultima_attivita': max([n.get('timestamp', '') for n in notes], default=None)
            }
            
        except Exception as e:
            print(f"Errore calcolo statistiche: {e}")
            return {'materia': materia, 'errore': str(e)}
    
    def _calculate_total_subject_hours(self, user: str, materia: str) -> float:
        """Calcola il totale delle ore studiate per una materia"""
        try:
            sessions = dataM.load_sessions(user)
            subject_sessions = [s for s in sessions if s.get('materia') == materia]
            total_minutes = sum(s.get('durata', 0) for s in subject_sessions)
            return total_minutes / 60
        except Exception:
            return 0.0
    
    def _format_time(self, minuti: int) -> str:
        """Formatta i minuti in formato leggibile"""
        if minuti < 60:
            return f"{minuti}min"
        else:
            ore = minuti // 60
            min_restanti = minuti % 60
            if min_restanti == 0:
                return f"{ore}h"
            else:
                return f"{ore}h {min_restanti}min"
    
    def delete_note(self, note_id: int) -> bool:
        """Elimina una nota per ID"""
        try:
            self.notes = [note for note in self.notes if note.get('id') != note_id]
            return self._save_notes()
        except Exception as e:
            print(f"Errore eliminazione nota: {e}")
            return False
    
    def get_recent_activity(self, user: str, days: int = 7) -> List[Dict]:
        """Ottieni attività recente degli ultimi N giorni"""
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_notes = []
            
            for note in self.notes:
                if note.get('user') != user:
                    continue
                
                try:
                    note_date = datetime.fromisoformat(note.get('timestamp', ''))
                    if note_date >= cutoff_date:
                        recent_notes.append(note)
                except ValueError:
                    continue
            
            # Ordina per data più recente
            recent_notes.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return recent_notes
            
        except Exception as e:
            print(f"Errore caricamento attività recente: {e}")
            return []
    
    def search_notes(self, user: str, query: str) -> List[Dict]:
        """Cerca nelle note per testo"""
        try:
            query_lower = query.lower()
            results = []
            
            for note in self.notes:
                if note.get('user') != user:
                    continue
                
                # Cerca in argomento, materia e descrizione
                text_fields = [
                    note.get('argomento', ''),
                    note.get('materia', ''), 
                    note.get('descrizione', '')
                ]
                
                if any(query_lower in field.lower() for field in text_fields if field):
                    results.append(note)
            
            results.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return results
            
        except Exception as e:
            print(f"Errore ricerca note: {e}")
            return []
    
    def get_user_notes(self, user: str, materia_filter: Optional[str] = None) -> List[Dict]:
        """Ottieni tutte le note di un utente, opzionalmente filtrate per materia"""
        try:
            user_notes = []
            
            for note in self.notes:
                if note.get('user') != user:
                    continue
                
                # Applica filtro materia se specificato
                if materia_filter and note.get('materia') != materia_filter:
                    continue
                
                user_notes.append(note)
            
            # Ordina per timestamp più recente
            user_notes.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
            return user_notes
            
        except Exception as e:
            print(f"Errore caricamento note utente: {e}")
            return []
    
    def get_subject_statistics(self, user: str, materia: str) -> Dict:
        """Calcola statistiche dettagliate per una materia specifica"""
        try:
            # Filtra note per utente e materia
            subject_notes = [
                note for note in self.notes 
                if note.get('user') == user and note.get('materia') == materia
            ]
            
            if not subject_notes:
                return {
                    'materia': materia,
                    'ore_totali': 0,
                    'sessioni_totali': 0,
                    'argomenti_studiati': 0,
                    'milestone_completate': 0,
                    'copertura_note': 0,
                    'tempo_medio_per_argomento': 0
                }
            
            # Calcola statistiche base
            sessioni_totali = len([n for n in subject_notes if n.get('tipo') == 'sessione'])
            milestone_completate = len([n for n in subject_notes if n.get('tipo') == 'milestone'])
            
            # Argomenti unici
            argomenti_unici = set(n.get('argomento') for n in subject_notes if n.get('argomento'))
            argomenti_studiati = len(argomenti_unici)
            
            # Calcola ore totali dalla sessioni dell'utente
            try:
                all_sessions = dataM.load_sessions(user)
                user_sessions = [s for s in all_sessions if s.get('subject') == materia]
                ore_totali = sum(s.get('duration', 0) for s in user_sessions) / 60.0  # Converti minuti in ore
                
                # Calcola copertura note (percentuale sessioni con note)
                sessions_with_notes = len([s for s in user_sessions if s.get('note_argomento')])
                copertura_note = (sessions_with_notes / len(user_sessions) * 100) if user_sessions else 0
                
            except Exception as e:
                print(f"Errore calcolo ore totali: {e}")
                ore_totali = 0
                copertura_note = 0
            
            # Tempo medio per argomento
            tempo_medio = ore_totali / argomenti_studiati if argomenti_studiati > 0 else 0
            
            return {
                'materia': materia,
                'ore_totali': round(ore_totali, 1),
                'sessioni_totali': sessioni_totali,
                'argomenti_studiati': argomenti_studiati,
                'milestone_completate': milestone_completate,
                'copertura_note': round(copertura_note, 1),
                'tempo_medio_per_argomento': round(tempo_medio, 1)
            }
            
        except Exception as e:
            print(f"Errore calcolo statistiche materia: {e}")
            return {
                'materia': materia,
                'ore_totali': 0,
                'sessioni_totali': 0,
                'argomenti_studiati': 0,
                'milestone_completate': 0,
                'copertura_note': 0,
                'tempo_medio_per_argomento': 0
            }
    
    def add_milestone_note(self, user: str, materia: str, argomento: str, 
                          descrizione: Optional[str] = None) -> bool:
        """Aggiunge una milestone manuale"""
        try:
            # Calcola ore totali per la materia
            try:
                all_sessions = dataM.load_sessions(user)
                user_sessions = [s for s in all_sessions if s.get('subject') == materia]
                ore_totali_materia = sum(s.get('duration', 0) for s in user_sessions) / 60.0
            except:
                ore_totali_materia = 0
            
            # Crea la nota milestone
            note = {
                'id': len(self.notes) + 1,  # ID incrementale
                'user': user,
                'materia': materia,
                'argomento': argomento,
                'tipo': 'milestone',
                'timestamp': datetime.now().isoformat(),
                'ore_totali_materia': round(ore_totali_materia, 2)
            }
            
            # Aggiungi descrizione se fornita
            if descrizione:
                note['descrizione'] = descrizione
            
            self.notes.append(note)
            return self._save_notes()
            
        except Exception as e:
            print(f"Errore aggiunta milestone: {e}")
            return False