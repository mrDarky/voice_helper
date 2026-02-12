#!/usr/bin/env python3
"""
Test script to verify signal handler fix works in both main and non-main threads
"""

import threading
import signal
import sys
import os

# Add the current directory to the path to import voice_processor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from voice_processor import catch_abort_signal, AbortException


def test_in_main_thread():
    """Test catch_abort_signal in main thread"""
    print("Testing catch_abort_signal in main thread...")
    try:
        with catch_abort_signal():
            print("  ✓ Signal handler context manager works in main thread")
        print("  ✓ Successfully exited context manager in main thread")
        return True
    except Exception as e:
        print(f"  ✗ Error in main thread: {e}")
        return False


def test_in_worker_thread():
    """Test catch_abort_signal in worker thread"""
    result = {'success': False, 'error': None}
    
    def worker():
        try:
            with catch_abort_signal():
                result['success'] = True
        except Exception as e:
            result['error'] = str(e)
    
    print("Testing catch_abort_signal in worker thread...")
    thread = threading.Thread(target=worker)
    thread.start()
    thread.join()
    
    if result['success']:
        print("  ✓ Signal handler context manager works in worker thread")
        return True
    else:
        print(f"  ✗ Error in worker thread: {result['error']}")
        return False


def test_nested_contexts():
    """Test nested catch_abort_signal contexts"""
    print("Testing nested catch_abort_signal contexts...")
    try:
        with catch_abort_signal():
            with catch_abort_signal():
                print("  ✓ Nested signal handler contexts work")
        print("  ✓ Successfully exited nested contexts")
        return True
    except Exception as e:
        print(f"  ✗ Error with nested contexts: {e}")
        return False


def main():
    print("=" * 60)
    print("Signal Handler Fix Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Main thread
    results.append(test_in_main_thread())
    print()
    
    # Test 2: Worker thread (this was the problem)
    results.append(test_in_worker_thread())
    print()
    
    # Test 3: Nested contexts
    results.append(test_nested_contexts())
    print()
    
    # Summary
    print("=" * 60)
    if all(results):
        print("✓ All tests passed!")
        print("=" * 60)
        return 0
    else:
        print("✗ Some tests failed")
        print("=" * 60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
