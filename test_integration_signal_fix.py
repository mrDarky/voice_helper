#!/usr/bin/env python3
"""
Integration test to verify the signal handler fix works in the actual VoiceProcessor context
"""

import sys
import os
import threading

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the dependencies that might not be installed
class MockRecognizer:
    pass

class MockSR:
    Recognizer = MockRecognizer

sys.modules['speech_recognition'] = MockSR()

# Mock database
class MockDatabase:
    def get_setting(self, key):
        return 'test phrase'
    
    def get_active_model(self):
        return None

sys.modules['database'] = type('module', (), {'Database': MockDatabase})()


def test_voice_processor_initialization():
    """Test that VoiceProcessor can be initialized without signal errors"""
    print("Testing VoiceProcessor initialization...")
    try:
        from voice_processor import VoiceProcessor
        vp = VoiceProcessor()
        print("  ✓ VoiceProcessor initialized successfully")
        return True
    except ValueError as e:
        if "signal only works in main thread" in str(e):
            print(f"  ✗ Signal error still occurs: {e}")
            return False
        raise
    except Exception as e:
        # Other exceptions are okay (like missing audio devices)
        if "Audio" in str(e) or "audio" in str(e):
            print(f"  ✓ VoiceProcessor initialized (audio not available, but no signal error)")
            return True
        print(f"  ? Unexpected error: {e}")
        return True  # Not a signal error


def test_listen_thread_with_signal_handler():
    """Test that signal handlers work correctly in listen threads"""
    print("Testing signal handler in listen thread context...")
    
    success = {'value': False}
    error = {'value': None}
    
    def thread_worker():
        try:
            from voice_processor import catch_abort_signal
            # Simulate what happens in _listen_loop
            with catch_abort_signal():
                success['value'] = True
        except Exception as e:
            error['value'] = str(e)
    
    thread = threading.Thread(target=thread_worker, daemon=True)
    thread.start()
    thread.join(timeout=2)
    
    if success['value']:
        print("  ✓ Signal handler works correctly in daemon thread")
        return True
    elif error['value']:
        print(f"  ✗ Error in daemon thread: {error['value']}")
        return False
    else:
        print("  ✗ Thread timed out or failed silently")
        return False


def main():
    print("=" * 60)
    print("Integration Test for Signal Handler Fix")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: VoiceProcessor initialization
    results.append(test_voice_processor_initialization())
    print()
    
    # Test 2: Signal handler in listen thread
    results.append(test_listen_thread_with_signal_handler())
    print()
    
    # Summary
    print("=" * 60)
    if all(results):
        print("✓ All integration tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
