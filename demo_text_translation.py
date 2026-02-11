#!/usr/bin/env python3
"""
Demo script for text translation feature
Demonstrates the new bidirectional translation without requiring voice input
"""

from translator import TranslationService

def demo_command_parsing():
    """Demonstrate command parsing capabilities"""
    print("=" * 60)
    print("Text Translation Feature Demo")
    print("=" * 60)
    
    ts = TranslationService()
    
    print("\n1. Command Parsing Examples:")
    print("-" * 60)
    
    commands = [
        "translate from russian to english",
        "translate from english to russian",
        "translate to spanish",
        "translate from french to german",
        "translate to russian",
    ]
    
    for cmd in commands:
        source, target = ts.parse_translate_command(cmd)
        print(f"Command: '{cmd}'")
        print(f"  → Source: {source}, Target: {target}")
        print()

def demo_translation():
    """Demonstrate actual translation (requires deep-translator)"""
    print("\n2. Translation Examples:")
    print("-" * 60)
    
    ts = TranslationService()
    
    examples = [
        ("Hello, how are you?", "en", "ru"),
        ("Привет, как дела?", "ru", "en"),
        ("Good morning", "en", "es"),
        ("Bonjour", "fr", "en"),
    ]
    
    try:
        for text, source, target in examples:
            result = ts.translate(text, target, source)
            print(f"Text: '{text}'")
            print(f"From: {source} → To: {target}")
            print(f"Result: '{result}'")
            print()
    except Exception as e:
        print(f"Translation requires 'deep-translator' package")
        print(f"Install with: pip install deep-translator")
        print(f"Error: {e}")

def demo_usage():
    """Show usage instructions"""
    print("\n3. How to Use Text Input Mode:")
    print("-" * 60)
    print("""
    In the Voice Helper application:
    
    1. Launch the application:
       python main.py
    
    2. In the main screen, find the "Text Input Mode" section
    
    3. Enter your text to translate in the first field
       Example: "Hello, how are you?"
    
    4. Enter your command in the second field
       Examples:
       - "translate from english to russian"
       - "translate from russian to english"
       - "translate to spanish"
    
    5. Click the "Execute" button
    
    6. View the translation result in the popup and log
    
    No microphone or voice input required!
    """)

if __name__ == '__main__':
    demo_command_parsing()
    demo_translation()
    demo_usage()
    
    print("=" * 60)
    print("Demo complete!")
    print("=" * 60)
