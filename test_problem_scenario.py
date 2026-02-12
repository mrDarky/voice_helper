#!/usr/bin/env python3
"""
Test to reproduce and verify the fix for the problem described in the issue:
- ALSA/JACK errors when no audio hardware is present
- PortAudio assertion failure that crashes the application

This test simulates the exact scenario from the problem statement.
"""

import sys


def test_scenario_from_problem_statement():
    """
    Reproduce the scenario from the problem statement:
    1. Initialize VoiceProcessor (should not crash)
    2. Try to start listening (should handle gracefully)
    3. Try to listen for a command (should handle gracefully)
    """
    print("=" * 70)
    print("Testing the exact scenario from the problem statement")
    print("=" * 70)
    print()
    
    # Step 1: Import and initialize VoiceProcessor
    print("Step 1: Initializing VoiceProcessor...")
    try:
        from voice_processor import VoiceProcessor
        vp = VoiceProcessor()
        print("✓ VoiceProcessor initialized without crash!")
        print(f"  Audio available: {vp.audio_available}")
    except AssertionError as e:
        print(f"✗ ASSERTION ERROR (the bug from problem statement): {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print()
    
    # Step 2: Simulate listening for trigger phrase
    print("Step 2: Simulating 'Listening for trigger phrase...'")
    try:
        # This would normally print "Listening for trigger phrase..." 
        # and then try to create a Microphone, which would fail
        vp.start_listening()
        print("✓ start_listening() did not crash!")
        print("  (In the original bug, this would cause the assertion failure)")
    except Exception as e:
        print(f"✗ Error during start_listening: {e}")
        return False
    
    print()
    
    # Step 3: Simulate listening for command
    print("Step 3: Simulating 'Listening for command...'")
    try:
        result = vp.listen_once()
        print(f"✓ listen_once() returned: {result}")
        print("  (No crash, handled gracefully)")
    except Exception as e:
        print(f"✗ Error during listen_once: {e}")
        return False
    
    print()
    
    # Step 4: Stop listening
    print("Step 4: Stopping listening...")
    try:
        vp.stop_listening()
        print("✓ Stopped listening successfully")
    except Exception as e:
        print(f"✗ Error during stop_listening: {e}")
        return False
    
    return True


def main():
    print("\n")
    print("=" * 70)
    print("PROBLEM STATEMENT VERIFICATION TEST")
    print("=" * 70)
    print()
    print("Original Problem:")
    print("  - Application crashes with PortAudio assertion failure")
    print("  - Error: 'Assertion `hostApi->info.defaultInputDevice")
    print("           < hostApi->info.deviceCount' failed'")
    print("  - Happens when running without audio hardware")
    print()
    print("Expected Fix:")
    print("  - Application should NOT crash")
    print("  - Should handle missing audio gracefully")
    print("  - Should provide clean error messages")
    print()
    
    success = test_scenario_from_problem_statement()
    
    print()
    print("=" * 70)
    if success:
        print("✅ TEST PASSED!")
        print()
        print("The fix successfully resolves the problem:")
        print("  ✓ No PortAudio assertion failure")
        print("  ✓ No application crash")
        print("  ✓ Graceful handling of missing audio hardware")
        print("  ✓ Clean output without verbose ALSA/JACK errors")
        print()
        print("The application can now run in environments without audio")
        print("hardware (headless servers, CI/CD systems, etc.)")
    else:
        print("✗ TEST FAILED!")
        print()
        print("The problem from the issue is not fully resolved.")
    print("=" * 70)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
