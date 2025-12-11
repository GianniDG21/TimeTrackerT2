"""
Chart Generator per TimeTrackerT2
Modulo per la generazione di grafici per l'analisi dei dati
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import tkinter as tk

# Configurazione tema scuro per matplotlib
try:
    plt.style.use('dark_background')
    sns.set_palette("husl")
except Exception as e:
    print(f"Avviso: configurazione stile matplotlib - {e}")
    # Usa configurazione di default se dark_background non è disponibile

class ChartGenerator:
    """Generatore di grafici per l'analisi dei dati"""
    
    def __init__(self, analytics_engine):
        self.engine = analytics_engine
        self.colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD', '#98D8C8', '#F7DC6F']
        
    def create_subject_distribution_chart(self, period="all", chart_type="pie"):
        """Crea grafico distribuzione tempo per materia"""
        data = self.engine.get_study_time_by_subject(period)
        
        if not data:
            return self._create_empty_chart("Nessun dato disponibile")
        
        fig = Figure(figsize=(10, 6), facecolor='#2b2b2b')
        
        if chart_type == "pie":
            ax = fig.add_subplot(111)
            wedges, texts, autotexts = ax.pie(
                data.values(), 
                labels=data.keys(),
                autopct='%1.1f%%',
                colors=self.colors[:len(data)],
                startangle=90
            )
            
            # Personalizza i testi
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
            
            for text in texts:
                text.set_color('white')
                text.set_fontsize(11)
            
            ax.set_title(f'Distribuzione Tempo per Materia ({period})', 
                        color='white', fontsize=14, pad=20)
                        
        else:  # bar chart
            ax = fig.add_subplot(111)
            bars = ax.bar(data.keys(), data.values(), color=self.colors[:len(data)])
            
            ax.set_title(f'Ore di Studio per Materia ({period})', 
                        color='white', fontsize=14, pad=20)
            ax.set_xlabel('Materie', color='white')
            ax.set_ylabel('Ore di Studio', color='white')
            
            # Personalizza l'aspetto
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            # Aggiungi valori sopra le barre
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.1f}h', ha='center', va='bottom', color='white')
        
        fig.patch.set_facecolor('#2b2b2b')
        fig.tight_layout()
        return fig
    
    def create_daily_trend_chart(self, days=30):
        """Crea grafico trend giornaliero"""
        data = self.engine.get_daily_study_stats(days)
        
        if not data:
            return self._create_empty_chart("Nessun dato per il trend giornaliero")
        
        df = pd.DataFrame(data)
        df['data'] = pd.to_datetime(df['data'])
        
        fig = Figure(figsize=(12, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        
        # Crea il grafico a linee
        ax.plot(df['data'], df['ore_totali'], 
               marker='o', linewidth=2, markersize=6, 
               color='#4ECDC4', markerfacecolor='#FF6B6B')
        
        # Personalizza l'aspetto
        ax.set_title(f'Trend Studio Giornaliero ({days} giorni)', 
                    color='white', fontsize=14, pad=20)
        ax.set_xlabel('Data', color='white')
        ax.set_ylabel('Ore di Studio', color='white')
        
        # Formatta le date sull'asse x
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//10)))
        
        # Personalizza colori
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Aggiungi griglia
        ax.grid(True, alpha=0.3, color='white')
        
        fig.patch.set_facecolor('#2b2b2b')
        fig.tight_layout()
        return fig
    
    def create_weekly_comparison_chart(self):
        """Crea grafico comparativo settimanale"""
        data = self.engine.get_weekly_study_stats(4)
        
        if not data:
            return self._create_empty_chart("Nessun dato per il confronto settimanale")
        
        df = pd.DataFrame(data)
        
        fig = Figure(figsize=(10, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        
        # Crea etichette per le settimane
        labels = [f"Sett. {row['settimana']}" for _, row in df.iterrows()]
        
        bars = ax.bar(labels, df['ore_totali'], color=self.colors[:len(df)])
        
        ax.set_title('Confronto Studio Settimanale', color='white', fontsize=14, pad=20)
        ax.set_xlabel('Settimane', color='white')
        ax.set_ylabel('Ore Totali', color='white')
        
        # Personalizza l'aspetto
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Aggiungi valori sopra le barre
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}h', ha='center', va='bottom', color='white')
        
        fig.patch.set_facecolor('#2b2b2b')
        fig.tight_layout()
        return fig
    
    def create_hourly_heatmap(self):
        """Crea heatmap delle ore di studio"""
        pattern = self.engine.get_study_pattern_by_hour()
        
        if not pattern:
            return self._create_empty_chart("Nessun dato per il pattern orario")
        
        # Prepara i dati per la heatmap
        hours = list(range(24))
        study_hours = [pattern.get(hour, 0) for hour in hours]
        
        fig = Figure(figsize=(12, 4), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        
        # Crea matrice per heatmap
        data_matrix = np.array(study_hours).reshape(1, -1)
        
        im = ax.imshow(data_matrix, cmap='YlOrRd', aspect='auto')
        
        # Personalizza assi
        ax.set_xticks(range(24))
        ax.set_xticklabels([f"{h}:00" for h in hours])
        ax.set_yticks([])
        ax.set_xlabel('Ora del Giorno', color='white')
        ax.set_title('Pattern di Studio per Ora', color='white', fontsize=14, pad=20)
        
        # Aggiungi colorbar
        cbar = fig.colorbar(im, ax=ax)
        cbar.set_label('Ore di Studio', color='white')
        cbar.ax.yaxis.label.set_color('white')
        cbar.ax.tick_params(colors='white')
        
        # Personalizza colori
        ax.tick_params(colors='white')
        
        fig.patch.set_facecolor('#2b2b2b')
        fig.tight_layout()
        return fig
    
    def create_weekday_pattern_chart(self):
        """Crea grafico pattern settimanale"""
        pattern = self.engine.get_study_pattern_by_weekday()
        
        if not pattern:
            return self._create_empty_chart("Nessun dato per il pattern settimanale")
        
        # Giorni in italiano
        italian_days = {
            'Monday': 'Lunedì', 'Tuesday': 'Martedì', 'Wednesday': 'Mercoledì',
            'Thursday': 'Giovedì', 'Friday': 'Venerdì', 'Saturday': 'Sabato', 'Sunday': 'Domenica'
        }
        
        days = list(pattern.keys())
        values = list(pattern.values())
        italian_labels = [italian_days.get(day, day) for day in days]
        
        fig = Figure(figsize=(10, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        
        bars = ax.bar(italian_labels, values, color=self.colors[:len(days)])
        
        ax.set_title('Pattern di Studio per Giorno della Settimana', 
                    color='white', fontsize=14, pad=20)
        ax.set_xlabel('Giorno', color='white')
        ax.set_ylabel('Ore di Studio', color='white')
        
        # Personalizza l'aspetto
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Ruota le etichette per leggibilità
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
        
        # Aggiungi valori sopra le barre
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}h', ha='center', va='bottom', color='white')
        
        fig.patch.set_facecolor('#2b2b2b')
        fig.tight_layout()
        return fig
    
    def create_productivity_dashboard(self):
        """Crea dashboard riassuntiva"""
        insights = self.engine.get_productivity_insights()
        
        fig = Figure(figsize=(12, 8), facecolor='#2b2b2b')
        
        # Crea subplot per le statistiche principali
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)
        
        # Statistiche testuali
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        stats_text = f"""
        DASHBOARD PRODUTTIVITA'
        
        Sessioni Totali: {insights['total_sessions']}
        Ore Totali: {insights['total_hours']:.1f}h
        Media Sessione: {insights['avg_session_length']:.1f}h
        
        Materia Top: {insights['most_studied_subject']}
        Ora piu' Produttiva: {insights['most_productive_hour']}
        Giorno piu' Produttivo: {insights['most_productive_day']}
        """
        
        ax1.text(0.1, 0.5, stats_text, fontsize=14, color='white', 
                verticalalignment='center', fontfamily='monospace')
        
        # Grafico materie (se ci sono dati)
        subject_data = self.engine.get_study_time_by_subject()
        if subject_data:
            ax2 = fig.add_subplot(gs[1, 0])
            ax2.pie(subject_data.values(), labels=subject_data.keys(),
                   autopct='%1.1f%%', colors=self.colors[:len(subject_data)])
            ax2.set_title('Distribuzione Materie', color='white', fontsize=12)
        
        # Pattern orario (se ci sono dati)
        hourly_data = self.engine.get_study_pattern_by_hour()
        if hourly_data:
            ax3 = fig.add_subplot(gs[1, 1])
            hours = list(hourly_data.keys())
            values = list(hourly_data.values())
            ax3.bar(hours, values, color='#4ECDC4')
            ax3.set_title('Pattern Orario', color='white', fontsize=12)
            ax3.set_xlabel('Ora', color='white', fontsize=10)
            ax3.tick_params(colors='white', labelsize=8)
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
        
        fig.patch.set_facecolor('#2b2b2b')
        return fig
    
    def _create_empty_chart(self, message):
        """Crea grafico vuoto con messaggio"""
        fig = Figure(figsize=(8, 6), facecolor='#2b2b2b')
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, message, ha='center', va='center', 
               fontsize=16, color='white', transform=ax.transAxes)
        ax.set_facecolor('#2b2b2b')
        ax.axis('off')
        return fig