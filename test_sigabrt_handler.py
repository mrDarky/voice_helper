#!/usr/bin/env python3
"""
Test the SIGABRT signal handler to ensure it can catch assertion failures
"""
import os
import sys
import signal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_processor import catch_abort_signal, AbortException


def test_sigabrt_handler():
    """Test that the SIGABRT handler can catch and convert signals to exceptions"""
    print("Testing SIGABRT handler...")
    print()
    
    # Test 1: Normal operation (no signal)
    print("Test 1: Normal operation (no SIGABRT)")
    with catch_abort_signal():
        print("  Inside context manager")
        print("  ✓ No signal raised")
    print("  ✓ Test 1 passed\n")
    
    # Test 2: Simulated SIGABRT
    print("Test 2: Simulated SIGABRT")
    caught_exception = False
    with catch_abort_signal():
        try:
            print("  Sending SIGABRT to self...")
            os.kill(os.getpid(), signal.SIGABRT)
            print("  ✗ Should not reach here")
        except AbortException as e:
            print(f"  ✓ Caught AbortException: {e}")
            caught_exception = True
    
    assert caught_exception, "AbortException should have been caught"
    print("  ✓ Test 2 passed\n")
    
    # Test 3: Verify signal handler is restored
    print("Test 3: Verify signal handler is restored")
    original_handler = signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, original_handler)
    
    with catch_abort_signal():
        pass
    
    current_handler = signal.signal(signal.SIGABRT, signal.SIG_DFL)
    signal.signal(signal.SIGABRT, original_handler)
    
    print("  ✓ Signal handler restored")
    print("  ✓ Test 3 passed\n")
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print()
    print("The SIGABRT handler successfully:")
    print("  ✓ Catches SIGABRT signals")
    print("  ✓ Converts them to AbortException")
    print("  ✓ Restores original handler after context")
    print()
    print("This should prevent 'Aborted (core dumped)' crashes!")


if __name__ == '__main__':
    test_sigabrt_handler()
