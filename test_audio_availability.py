#!/usr/bin/env python3
"""
Test to verify that the PortAudio assertion failure is fixed.
This test ensures that the application can start even when no audio hardware is available.
"""

import sys

def test_voice_processor_no_crash():
    """Test that VoiceProcessor doesn't crash when no audio is available"""
    print("\n=== Testing VoiceProcessor No-Crash Behavior ===")
    try:
        from voice_processor import VoiceProcessor
        
        # This should NOT crash even without audio hardware
        vp = VoiceProcessor()
        print("✓ VoiceProcessor created without crashing")
        
        # Check audio availability status
        print(f"  Audio available: {vp.audio_available}")
        
        # Try to start listening - should fail gracefully
        print("\n  Testing start_listening...")
        vp.start_listening()
        print("  ✓ start_listening handled gracefully (no crash)")
        
        # Try listen_once - should fail gracefully
        print("\n  Testing listen_once...")
        result = vp.listen_once()
        print(f"  ✓ listen_once returned: {result} (no crash)")
        
        return True
    except AssertionError as e:
        print(f"✗ ASSERTION ERROR (this is the bug we're fixing): {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_main_app_initialization():
    """Test that main app components can initialize"""
    print("\n=== Testing Main App Initialization ===")
    try:
        from database import Database
        from voice_processor import VoiceProcessor
        from translator import TranslationService
        
        db = Database()
        print("✓ Database initialized")
        
        vp = VoiceProcessor()
        print("✓ VoiceProcessor initialized")
        
        translator = TranslationService()
        print("✓ TranslationService initialized")
        
        print("\n✓ All core components initialized successfully")
        return True
    except Exception as e:
        print(f"✗ Failed to initialize components: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Audio Availability Fix - Verification Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("No-Crash Test", test_voice_processor_no_crash()))
    results.append(("App Initialization Test", test_main_app_initialization()))
    
    print("\n" + "=" * 60)
    print("Test Summary:")
    print("=" * 60)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ All tests passed!")
        print("\nThe fix successfully prevents the PortAudio assertion failure.")
        print("The application can now run in environments without audio hardware.")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
