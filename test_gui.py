"""
Test rapido delle funzionalità TimeTrackerT GUI
"""

import dataM
import user
from gui_utils import StatsCalculator, UIHelpers, DataValidator

def test_basic_functionality():
    """Test delle funzionalità di base"""
    
    print("=== Test TimeTrackerT GUI ===\n")
    
    # Test 1: Caricamento dati utente
    print("📊 Test 1: Caricamento dati utente")
    print(f"Utente attuale: {user.act_user}")
    
    # Test 2: Caricamento sessioni
    print("\n📈 Test 2: Caricamento sessioni")
    sessions = dataM.load_sessions(user.act_user)
    print(f"Sessioni caricate: {len(sessions)}")
    
    # Test 3: Statistiche
    print("\n📊 Test 3: Calcolo statistiche")
    stats = StatsCalculator.calculate_session_stats(sessions)
    print(f"Totale ore: {stats['total_hours']:.1f}h")
    print(f"Materia preferita: {stats['favorite_subject']}")
    print(f"Sessioni questa settimana: {UIHelpers.format_duration(stats['weekly_total'])}")
    
    # Test 4: Validazione materie
    print("\n✅ Test 4: Validazione nomi materie")
    test_names = ["Matematica", "", "A" * 100, "Test/Invalid", "Python 🐍"]
    
    for name in test_names:
        is_valid, result = DataValidator.validate_subject_name(name)
        status = "✅" if is_valid else "❌"
        print(f"{status} '{name[:20]}...' -> {result if is_valid else 'ERRORE: ' + result}")
    
    # Test 5: Formattazione
    print("\n🎨 Test 5: Formattazione UI")
    test_durations = [5, 25, 65, 150, 1500]
    for duration in test_durations:
        formatted = UIHelpers.format_duration(duration)
        print(f"{duration} minuti -> {formatted}")
    
    # Test 6: Emoji materie
    print("\n😀 Test 6: Emoji per materie")
    test_subjects = ["Matematica", "Python", "GoLang", "Storia", "Fisica", "Gioco"]
    for subject in test_subjects:
        emoji = UIHelpers.get_subject_emoji(subject)
        print(f"{emoji} {subject}")
    
    # Test 7: Insights
    print("\n💡 Test 7: Insights personalizzati")
    if len(sessions) >= 5:
        insights = StatsCalculator.get_productivity_insights(sessions)
        for i, insight in enumerate(insights, 1):
            print(f"{i}. {insight}")
    else:
        print("Non abbastanza sessioni per insights personalizzati")
    
    print("\n🎉 Tutti i test completati!")
    print(f"📱 Ora puoi avviare l'app GUI con: python main_gui.py")
    print(f"🚀 Oppure usa il launcher: AVVIA_GUI.bat")

if __name__ == "__main__":
    test_basic_functionality()