#!/usr/bin/env python3
"""
Simple launcher script for Voice Helper
Checks dependencies before launching
"""

import sys
import subprocess

def check_dependency(module_name, package_name=None):
    """Check if a Python module is installed"""
    if package_name is None:
        package_name = module_name
    
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def main():
    print("Voice Helper Launcher")
    print("=" * 50)
    
    # Check critical dependencies
    critical = [
        ('kivy', 'kivy'),
        ('speech_recognition', 'SpeechRecognition'),
        ('whisper', 'openai-whisper'),
    ]
    
    optional = [
        ('deep_translator', 'deep-translator'),
        ('pyttsx3', 'pyttsx3'),
    ]
    
    missing_critical = []
    missing_optional = []
    
    print("\nChecking dependencies...")
    
    for module, package in critical:
        if check_dependency(module):
            print(f"✓ {package}")
        else:
            print(f"✗ {package} (REQUIRED)")
            missing_critical.append(package)
    
    for module, package in optional:
        if check_dependency(module):
            print(f"✓ {package}")
        else:
            print(f"✗ {package} (optional)")
            missing_optional.append(package)
    
    if missing_critical:
        print("\n" + "=" * 50)
        print("ERROR: Missing required dependencies!")
        print("=" * 50)
        print("\nPlease install them with:")
        print(f"  pip install {' '.join(missing_critical)}")
        print("\nOr run the setup script:")
        print("  ./setup.sh (Linux/macOS)")
        print("  setup.bat (Windows)")
        return 1
    
    if missing_optional:
        print("\nNote: Some optional features may not work without:")
        print(f"  pip install {' '.join(missing_optional)}")
    
    print("\n" + "=" * 50)
    print("Starting Voice Helper...")
    print("=" * 50 + "\n")
    
    # Launch the application
    try:
        from main import VoiceHelperApp
        VoiceHelperApp().run()
        return 0
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
