#!/usr/bin/env python3
"""
Example: Testing Voice Helper components without full UI

This script demonstrates how to use the core components
for testing or integration into other applications.
"""

import sys
import os

# Ensure we can import from current directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def example_database_usage():
    """Example of using the Database class"""
    print("\n=== Database Usage Example ===\n")
    
    from database import Database
    
    # Create database instance
    db = Database('example.db')
    print("✓ Database initialized: example.db")
    
    # Get all available models
    models = db.get_all_models()
    print(f"\nAvailable Whisper models: {len(models)}")
    for model in models:
        model_id, name, downloaded, active, date = model
        status = "Downloaded" if downloaded else "Not Downloaded"
        active_str = "ACTIVE" if active else ""
        print(f"  - {name}: {status} {active_str}")
    
    # Set a model as active
    db.set_active_model('base')
    print(f"\n✓ Set 'base' as active model")
    
    # Get active model
    active = db.get_active_model()
    print(f"  Current active model: {active}")
    
    # Work with settings
    db.set_setting('my_custom_setting', 'test_value')
    value = db.get_setting('my_custom_setting')
    print(f"\n✓ Stored setting: my_custom_setting = {value}")
    
    # Clean up example database
    os.remove('example.db')
    print("\n✓ Cleaned up example database")

def example_translation_parsing():
    """Example of parsing translation commands"""
    print("\n=== Translation Command Parsing Example ===\n")
    
    from translator import TranslationService
    
    ts = TranslationService()
    
    # Test command parsing
    commands = [
        "translate to spanish",
        "translate to french",
        "translate to german",
        "hey assistant translate to italian",
    ]
    
    for command in commands:
        lang_code = ts.parse_translate_command(command)
        print(f"Command: '{command}'")
        print(f"  → Target language: {lang_code}\n")
    
    # Test language code mapping
    languages = ['english', 'spanish', 'french', 'german', 'japanese']
    print("Language name to code mapping:")
    for lang in languages:
        code = ts._language_to_code(lang)
        print(f"  {lang} → {code}")

def example_model_info():
    """Display information about Whisper models"""
    print("\n=== Whisper Model Information ===\n")
    
    models_info = {
        'tiny': {'size': '39 MB', 'speed': 'Fastest', 'accuracy': 'Basic'},
        'base': {'size': '74 MB', 'speed': 'Fast', 'accuracy': 'Good'},
        'small': {'size': '244 MB', 'speed': 'Medium', 'accuracy': 'Better'},
        'medium': {'size': '769 MB', 'speed': 'Slow', 'accuracy': 'Very Good'},
        'large': {'size': '1550 MB', 'speed': 'Slowest', 'accuracy': 'Best'},
    }
    
    print("Available Whisper models:\n")
    print(f"{'Model':<10} {'Size':<12} {'Speed':<10} {'Accuracy':<12}")
    print("-" * 50)
    
    for model, info in models_info.items():
        print(f"{model:<10} {info['size']:<12} {info['speed']:<10} {info['accuracy']:<12}")
    
    print("\nRecommendations:")
    print("  • For quick responses: Use 'tiny' or 'base'")
    print("  • For balanced performance: Use 'small'")
    print("  • For best accuracy: Use 'large' (requires more RAM)")

def main():
    """Run all examples"""
    print("=" * 60)
    print("Voice Helper - Component Usage Examples")
    print("=" * 60)
    
    try:
        example_database_usage()
        example_translation_parsing()
        example_model_info()
        
        print("\n" + "=" * 60)
        print("✓ All examples completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("  1. Install dependencies: pip install -r requirements.txt")
        print("  2. Run the app: python main.py")
        print("  3. Or use launcher: python run.py")
        print()
        
    except Exception as e:
        print(f"\n✗ Error running examples: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
