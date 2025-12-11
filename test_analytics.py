"""
Test per verificare il funzionamento dell'Analytics
"""

# Test import moduli
try:
    from analytics_engine import AnalyticsEngine
    print("✓ AnalyticsEngine importato correttamente")
except Exception as e:
    print(f"✗ Errore import AnalyticsEngine: {e}")

try:
    from chart_generator import ChartGenerator
    print("✓ ChartGenerator importato correttamente")
except Exception as e:
    print(f"✗ Errore import ChartGenerator: {e}")

# Test caricamento dati
try:
    engine = AnalyticsEngine("Gianni")
    print(f"✓ Analytics engine creato - {len(engine.sessions)} sessioni caricate")
    
    if engine.sessions:
        print(f"✓ Prima sessione: {engine.sessions[0]}")
    else:
        print("⚠ Nessuna sessione trovata per Gianni")
        
except Exception as e:
    print(f"✗ Errore creazione AnalyticsEngine: {e}")

# Test statistiche
try:
    insights = engine.get_productivity_insights()
    print(f"✓ Insights calcolate: {insights}")
except Exception as e:
    print(f"✗ Errore calcolo insights: {e}")

# Test grafico
try:
    chart_gen = ChartGenerator(engine)
    fig = chart_gen.create_productivity_dashboard()
    print("✓ Dashboard creata correttamente")
except Exception as e:
    print(f"✗ Errore creazione dashboard: {e}")

print("\n🎯 Test completato!")