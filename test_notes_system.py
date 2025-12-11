#!/usr/bin/env python3
"""
Test script per il sistema di note di progresso
Verifica l'integrazione completa delle funzionalità di tracciamento argomenti
"""

import sys
import traceback
from datetime import datetime

def test_progress_manager():
    """Test del ProgressManager"""
    print("🔍 Testing ProgressManager...")
    
    try:
        from progress_manager import ProgressManager
        pm = ProgressManager()
        
        print("✅ ProgressManager importato correttamente")
        
        # Test aggiunta nota sessione
        success = pm.add_session_note(
            user="TestUser",
            materia="Matematica", 
            argomento="Derivate parziali",
            durata_sessione=45
        )
        print(f"✅ add_session_note: {success}")
        
        # Test milestone
        success = pm.add_milestone_note(
            user="TestUser",
            materia="Matematica",
            argomento="Completato capitolo derivate",
            descrizione="Capiti tutti gli esercizi del capitolo 5"
        )
        print(f"✅ add_milestone_note: {success}")
        
        # Test recupero note
        notes = pm.get_user_notes("TestUser")
        print(f"✅ get_user_notes: {len(notes)} note trovate")
        
        # Test statistiche
        stats = pm.get_subject_statistics("TestUser", "Matematica")
        print(f"✅ get_subject_statistics: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore ProgressManager: {e}")
        traceback.print_exc()
        return False

def test_dataM_integration():
    """Test integrazione con dataM"""
    print("\n🔍 Testing dataM integration...")
    
    try:
        import dataM
        
        # Test salvataggio sessione con nota
        success = dataM.save_session(
            user="TestUser",
            materia="Fisica",
            durata=60,
            note_argomento="Meccanica quantistica - Equazione di Schrödinger"
        )
        print(f"✅ save_session con note: {success}")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore dataM integration: {e}")
        traceback.print_exc()
        return False

def test_gui_imports():
    """Test importazione componenti GUI"""
    print("\n🔍 Testing GUI imports...")
    
    try:
        from gui_windows import NotesWindow, MilestoneDialog, NoteDialog
        print("✅ Importazione NotesWindow: OK")
        print("✅ Importazione MilestoneDialog: OK") 
        print("✅ Importazione NoteDialog: OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Errore GUI imports: {e}")
        traceback.print_exc()
        return False

def test_json_files():
    """Test esistenza e validità file JSON"""
    print("\n🔍 Testing JSON files...")
    
    import os
    import json
    
    try:
        # Test progress_notes.json
        if os.path.exists("progress_notes.json"):
            with open("progress_notes.json", 'r', encoding='utf-8') as f:
                notes_data = json.load(f)
            print(f"✅ progress_notes.json: {len(notes_data)} notes")
        else:
            print("ℹ️ progress_notes.json: File non esistente (verrà creato al primo uso)")
        
        # Test goals.json
        if os.path.exists("goals.json"):
            with open("goals.json", 'r', encoding='utf-8') as f:
                goals_data = json.load(f)
            print(f"✅ goals.json: {len(goals_data)} goals")
        else:
            print("ℹ️ goals.json: File non esistente")
            
        return True
        
    except Exception as e:
        print(f"❌ Errore JSON files: {e}")
        return False

def main():
    """Esegue tutti i test"""
    print("🚀 INIZIO TEST SISTEMA NOTE TIMETRACKERT2")
    print("=" * 50)
    
    tests = [
        ("ProgressManager", test_progress_manager),
        ("dataM Integration", test_dataM_integration), 
        ("GUI Imports", test_gui_imports),
        ("JSON Files", test_json_files)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 CRASH in {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 RISULTATI TEST:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 RISULTATO FINALE: {passed}/{total} test passati")
    
    if passed == total:
        print("🎉 TUTTI I TEST SONO PASSATI! Il sistema è pronto.")
    else:
        print("⚠️ Alcuni test sono falliti. Controllare gli errori sopra.")
        
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)