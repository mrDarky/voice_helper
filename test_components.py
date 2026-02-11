#!/usr/bin/env python3
"""
Demo/Test script for Voice Helper components
Tests each component without requiring full UI or microphone
"""

import sys

def test_database():
    """Test database functionality"""
    print("\n=== Testing Database ===")
    try:
        from database import Database
        db = Database()
        
        # Test model operations
        models = db.get_all_models()
        print(f"✓ Found {len(models)} Whisper models")
        
        # Test setting active model
        db.set_active_model('base')
        active = db.get_active_model()
        assert active == 'base', "Failed to set active model"
        print(f"✓ Active model set to: {active}")
        
        # Test settings
        db.set_setting('test_setting', 'test_value')
        value = db.get_setting('test_setting')
        assert value == 'test_value', "Failed to store setting"
        print("✓ Settings storage working")
        
        # Test marking model as downloaded
        db.update_model_downloaded('tiny', True)
        models = db.get_all_models()
        tiny_model = [m for m in models if m[1] == 'tiny'][0]
        assert tiny_model[2] == 1, "Failed to mark model as downloaded"
        print("✓ Model download tracking working")
        
        return True
    except Exception as e:
        print(f"✗ Database test failed: {e}")
        return False

def test_translator():
    """Test translator functionality"""
    print("\n=== Testing Translator ===")
    try:
        from translator import TranslationService
        ts = TranslationService()
        
        # Test command parsing - old format
        source, target = ts.parse_translate_command("translate to spanish")
        assert source == 'auto' and target == 'es', f"Expected ('auto', 'es'), got ('{source}', '{target}')"
        print(f"✓ Command parsing: 'translate to spanish' -> ('{source}', '{target}')")
        
        source, target = ts.parse_translate_command("translate to french")
        assert source == 'auto' and target == 'fr', f"Expected ('auto', 'fr'), got ('{source}', '{target}')"
        print(f"✓ Command parsing: 'translate to french' -> ('{source}', '{target}')")
        
        # Test new bidirectional command parsing
        source, target = ts.parse_translate_command("translate from russian to english")
        assert source == 'ru' and target == 'en', f"Expected ('ru', 'en'), got ('{source}', '{target}')"
        print(f"✓ Command parsing: 'translate from russian to english' -> ('{source}', '{target}')")
        
        source, target = ts.parse_translate_command("translate from english to russian")
        assert source == 'en' and target == 'ru', f"Expected ('en', 'ru'), got ('{source}', '{target}')"
        print(f"✓ Command parsing: 'translate from english to russian' -> ('{source}', '{target}')")
        
        # Test language code mapping
        code = ts._language_to_code('german')
        assert code == 'de', f"Expected 'de', got '{code}'"
        print("✓ Language code mapping working")
        
        code = ts._language_to_code('russian')
        assert code == 'ru', f"Expected 'ru', got '{code}'"
        print("✓ Russian language code mapping: 'russian' -> 'ru'")
        
        print("✓ Translation service initialized (actual translation requires API)")
        
        return True
    except Exception as e:
        print(f"✗ Translator test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_imports():
    """Test if all required modules can be imported"""
    print("\n=== Testing Imports ===")
    modules = {
        'sqlite3': 'SQLite (builtin)',
        'threading': 'Threading (builtin)',
        'datetime': 'Datetime (builtin)',
    }
    
    optional_modules = {
        'kivy': 'Kivy UI Framework',
        'whisper': 'OpenAI Whisper',
        'speech_recognition': 'Speech Recognition',
        'deep_translator': 'Deep Translator',
        'pyttsx3': 'Text-to-Speech',
    }
    
    all_ok = True
    
    for module, name in modules.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - REQUIRED")
            all_ok = False
    
    print("\nOptional modules:")
    for module, name in optional_modules.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"✗ {name} - Install with: pip install {module}")
    
    return all_ok

def test_kivy_file():
    """Test if Kivy file is valid"""
    print("\n=== Testing Kivy UI File ===")
    try:
        with open('voicehelper.kv', 'r') as f:
            content = f.read()
        
        # Basic validation
        assert '<ModelsScreen>' in content, "ModelsScreen not found"
        assert '<SettingsScreen>' in content, "SettingsScreen not found"
        assert '<MainScreen>' in content, "MainScreen not found"
        
        print("✓ Kivy file structure valid")
        print(f"✓ File size: {len(content)} characters")
        
        return True
    except Exception as e:
        print(f"✗ Kivy file test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Voice Helper - Component Tests")
    print("=" * 50)
    
    results = []
    
    results.append(("Import Test", test_imports()))
    results.append(("Database Test", test_database()))
    results.append(("Translator Test", test_translator()))
    results.append(("Kivy File Test", test_kivy_file()))
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("=" * 50)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 50)
    if all_passed:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        print("\nNote: Optional module failures are OK if you haven't installed dependencies yet.")
        print("Run: pip install -r requirements.txt")
        return 1

if __name__ == '__main__':
    sys.exit(main())
