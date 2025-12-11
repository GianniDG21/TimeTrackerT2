"""
Analytics Engine per TimeTrackerT2
Modulo per l'analisi dei dati delle sessioni di studio
"""

import json
import datetime
from collections import defaultdict, Counter
from dataM import load_sessions
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class AnalyticsEngine:
    """Motore per l'analisi dei dati delle sessioni di studio"""
    
    def __init__(self, user):
        self.user = user
        self.sessions = self._load_user_sessions()
        self.df = self._create_dataframe()
    
    def _load_user_sessions(self):
        """Carica le sessioni dell'utente"""
        try:
            return load_sessions(self.user)
        except Exception as e:
            print(f"Errore nel caricamento sessioni: {e}")
            return []
    
    def _create_dataframe(self):
        """Crea un DataFrame pandas dalle sessioni"""
        if not self.sessions:
            return pd.DataFrame()
        
        # Converte le sessioni in DataFrame
        df = pd.DataFrame(self.sessions)
        
        if not df.empty:
            # Converte timestamp in datetime
            df['datetime'] = pd.to_datetime(df['timestamp'])
            df['date'] = df['datetime'].dt.date
            df['hour'] = df['datetime'].dt.hour
            df['weekday'] = df['datetime'].dt.day_name()
            df['week'] = df['datetime'].dt.isocalendar().week.astype(int)
            df['month'] = df['datetime'].dt.month
            df['year'] = df['datetime'].dt.year
            
            # Converte durata in minuti (assumendo che sia in formato HH:MM:SS)
            df['durata_minuti'] = df['durata'].apply(self._parse_duration)
            df['durata_ore'] = df['durata_minuti'] / 60
        
        return df
    
    def _parse_duration(self, duration_str):
        """Converte la durata da stringa a minuti"""
        try:
            if isinstance(duration_str, str):
                # Formato HH:MM:SS o MM:SS
                parts = duration_str.split(':')
                if len(parts) == 3:  # HH:MM:SS
                    hours, minutes, seconds = map(float, parts)
                    return hours * 60 + minutes + seconds / 60
                elif len(parts) == 2:  # MM:SS
                    minutes, seconds = map(float, parts)
                    return minutes + seconds / 60
                else:
                    return float(duration_str)
            return float(duration_str)
        except (ValueError, AttributeError, TypeError):
            print(f"Errore parsing durata: {duration_str}")
            return 0
    
    def get_total_study_time(self, period="all"):
        """Calcola il tempo totale di studio"""
        if self.df.empty:
            return 0
        
        filtered_df = self._filter_by_period(period)
        return filtered_df['durata_ore'].sum() if not filtered_df.empty else 0
    
    def get_study_time_by_subject(self, period="all"):
        """Tempo di studio per materia"""
        if self.df.empty:
            return {}
        
        filtered_df = self._filter_by_period(period)
        if filtered_df.empty:
            return {}
        
        return filtered_df.groupby('materia')['durata_ore'].sum().to_dict()
    
    def get_daily_study_stats(self, days=30):
        """Statistiche giornaliere degli ultimi N giorni"""
        if self.df.empty:
            return []
        
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        # Filtra per periodo
        mask = (self.df['date'] >= start_date) & (self.df['date'] <= end_date)
        filtered_df = self.df[mask]
        
        if filtered_df.empty:
            return []
        
        # Raggruppa per data
        daily_stats = filtered_df.groupby('date').agg({
            'durata_ore': 'sum',
            'id': 'count',  # numero sessioni
            'materia': lambda x: len(x.unique())  # numero materie diverse
        }).reset_index()
        
        daily_stats.columns = ['data', 'ore_totali', 'sessioni', 'materie_diverse']
        
        return daily_stats.to_dict('records')
    
    def get_weekly_study_stats(self, weeks=4):
        """Statistiche settimanali"""
        if self.df.empty:
            return []
        
        # Filtra per le ultime N settimane
        current_week = datetime.now().isocalendar().week
        current_year = datetime.now().year
        
        filtered_df = self.df[
            (self.df['year'] == current_year) & 
            (self.df['week'] >= current_week - weeks)
        ]
        
        if filtered_df.empty:
            return []
        
        weekly_stats = filtered_df.groupby(['year', 'week']).agg({
            'durata_ore': 'sum',
            'materia': 'count'
        }).reset_index()
        
        weekly_stats.columns = ['anno', 'settimana', 'ore_totali', 'sessioni']
        
        return weekly_stats.to_dict('records')
    
    def get_monthly_study_stats(self, months=6):
        """Statistiche mensili"""
        if self.df.empty:
            return []
        
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Filtra per gli ultimi N mesi
        filtered_df = self.df[
            ((self.df['year'] == current_year) & (self.df['month'] >= current_month - months)) |
            ((self.df['year'] == current_year - 1) & (self.df['month'] >= 12 - (months - current_month)))
        ]
        
        if filtered_df.empty:
            return []
        
        monthly_stats = filtered_df.groupby(['year', 'month']).agg({
            'durata_ore': 'sum',
            'materia': 'count'
        }).reset_index()
        
        monthly_stats.columns = ['anno', 'mese', 'ore_totali', 'sessioni']
        
        return monthly_stats.to_dict('records')
    
    def get_study_pattern_by_hour(self):
        """Pattern di studio per ora del giorno"""
        if self.df.empty:
            return {}
        
        return self.df.groupby('hour')['durata_ore'].sum().to_dict()
    
    def get_study_pattern_by_weekday(self):
        """Pattern di studio per giorno della settimana"""
        if self.df.empty:
            return {}
        
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday_stats = self.df.groupby('weekday')['durata_ore'].sum()
        
        return {day: weekday_stats.get(day, 0) for day in weekday_order}
    
    def get_productivity_insights(self):
        """Insights sulla produttività"""
        if self.df.empty:
            return {
                'total_sessions': 0,
                'total_hours': 0,
                'avg_session_length': 0,
                'most_studied_subject': 'N/A',
                'most_productive_hour': 'N/A',
                'most_productive_day': 'N/A'
            }
        
        subject_stats = self.df.groupby('materia')['durata_ore'].sum()
        hour_stats = self.df.groupby('hour')['durata_ore'].sum()
        day_stats = self.df.groupby('weekday')['durata_ore'].sum()
        
        return {
            'total_sessions': len(self.df),
            'total_hours': self.df['durata_ore'].sum(),
            'avg_session_length': self.df['durata_ore'].mean(),
            'most_studied_subject': subject_stats.idxmax() if not subject_stats.empty else 'N/A',
            'most_productive_hour': f"{hour_stats.idxmax()}:00" if not hour_stats.empty else 'N/A',
            'most_productive_day': day_stats.idxmax() if not day_stats.empty else 'N/A'
        }
    
    def _filter_by_period(self, period):
        """Filtra il DataFrame per periodo"""
        if self.df.empty or period == "all":
            return self.df
        
        now = datetime.now()
        
        if period == "today":
            return self.df[self.df['date'] == now.date()]
        elif period == "week":
            start_week = now - timedelta(days=7)
            return self.df[self.df['datetime'] >= start_week]
        elif period == "month":
            start_month = now - timedelta(days=30)
            return self.df[self.df['datetime'] >= start_month]
        else:
            return self.df