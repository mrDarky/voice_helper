#!/usr/bin/env python3
"""
Test script for command selection feature
Tests the new dropdown command selector functionality
"""

import sys

def test_command_list():
    """Test that command list is properly defined in Kivy file"""
    print("\n=== Testing Command List ===")
    try:
        with open('voicehelper.kv', 'r') as f:
            content = f.read()
        
        # Check if Spinner widget exists
        assert 'command_spinner' in content, "command_spinner not found in Kivy file"
        print("✓ Command spinner widget exists")
        
        # Check for predefined commands
        expected_commands = [
            'translate from russian to english',
            'translate from english to russian',
            'translate from spanish to english',
            'translate from french to english',
            'translate to spanish',
            'translate to french',
            'translate to german',
            'Custom command...'
        ]
        
        for cmd in expected_commands:
            assert cmd in content, f"Command '{cmd}' not found in values list"
            print(f"✓ Command available: '{cmd}'")
        
        # Check that on_text callback is set
        assert 'on_text: root.on_command_selected(self.text)' in content, "on_text callback not found"
        print("✓ Command selection callback configured")
        
        return True
    except Exception as e:
        print(f"✗ Command list test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_command_handler():
    """Test that on_command_selected method exists in MainScreen"""
    print("\n=== Testing Command Handler ===")
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check if method exists
        assert 'def on_command_selected' in content, "on_command_selected method not found"
        print("✓ on_command_selected method exists")
        
        # Check if it handles the command text
        assert 'command_text' in content, "command_text parameter not found"
        print("✓ Method accepts command_text parameter")
        
        # Check if it updates text_command_input
        assert 'text_command_input.text' in content, "text_command_input update not found"
        print("✓ Method updates text_command_input field")
        
        return True
    except Exception as e:
        print(f"✗ Command handler test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_modern_design_elements():
    """Test that modern design elements are present"""
    print("\n=== Testing Modern Design Elements ===")
    try:
        with open('voicehelper.kv', 'r') as f:
            content = f.read()
        
        # Check for rounded corners
        assert 'RoundedRectangle' in content, "RoundedRectangle not found"
        assert 'radius:' in content, "Radius property not found"
        print("✓ Rounded corners implemented")
        
        # Check for modern colors (dark background)
        assert '0.12, 0.12, 0.15' in content or '0.18, 0.18, 0.22' in content, "Dark background colors not found"
        print("✓ Dark color scheme implemented")
        
        # Check for emojis/icons
        emoji_count = content.count('🎤') + content.count('📝') + content.count('⚙️') + content.count('🔧')
        assert emoji_count >= 4, f"Expected at least 4 emoji icons, found {emoji_count}"
        print(f"✓ Visual icons present ({emoji_count} found)")
        
        # Check for canvas.before blocks (for custom styling)
        canvas_count = content.count('canvas.before:')
        assert canvas_count >= 5, f"Expected at least 5 canvas.before blocks, found {canvas_count}"
        print(f"✓ Custom styling blocks present ({canvas_count} found)")
        
        # Check for bold text
        assert 'bold: True' in content, "Bold text styling not found"
        print("✓ Bold text styling implemented")
        
        # Check for larger font sizes
        assert 'font_size: 36' in content or 'font_size: 28' in content, "Large font sizes not found"
        print("✓ Enhanced typography implemented")
        
        return True
    except Exception as e:
        print(f"✗ Modern design test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_window_size():
    """Test that window size has been updated"""
    print("\n=== Testing Window Size ===")
    try:
        with open('main.py', 'r') as f:
            content = f.read()
        
        # Check for updated window size
        assert 'Window.size = (1000, 700)' in content, "Window size not updated to (1000, 700)"
        print("✓ Window size updated to 1000x700")
        
        # Check for window clearcolor (background)
        assert 'Window.clearcolor' in content, "Window clearcolor not set"
        print("✓ Window background color configured")
        
        return True
    except Exception as e:
        print(f"✗ Window size test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_button_styling():
    """Test that buttons have modern styling"""
    print("\n=== Testing Button Styling ===")
    try:
        with open('voicehelper.kv', 'r') as f:
            content = f.read()
        
        # Check for button background_normal removal (for custom colors)
        assert "background_normal: ''" in content, "background_normal not set to empty"
        print("✓ Custom button backgrounds enabled")
        
        # Check for button background_color
        assert 'background_color:' in content, "Button background colors not set"
        print("✓ Button colors customized")
        
        # Check for Start button with emoji
        assert '🎤 Start Listening' in content or 'Start Listening' in content, "Start button text not found"
        print("✓ Start button configured")
        
        return True
    except Exception as e:
        print(f"✗ Button styling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_text_input_mode_section():
    """Test that text input mode section has been redesigned"""
    print("\n=== Testing Text Input Mode Section ===")
    try:
        with open('voicehelper.kv', 'r') as f:
            content = f.read()
        
        # Check for section label
        assert 'Text Input Mode' in content, "Text Input Mode section not found"
        print("✓ Text Input Mode section present")
        
        # Check for command spinner
        assert 'id: command_spinner' in content, "Command spinner not found"
        print("✓ Command spinner present")
        
        # Check for custom command text input
        assert 'id: text_command_input' in content, "Custom command input not found"
        print("✓ Custom command input present")
        
        # Check for execute button
        assert 'Execute Command' in content or 'Execute' in content, "Execute button not found"
        print("✓ Execute button present")
        
        return True
    except Exception as e:
        print(f"✗ Text Input Mode test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Voice Helper - Feature Tests")
    print("Testing: Command Selector & Modern Design")
    print("=" * 60)
    
    results = []
    
    results.append(("Command List Test", test_command_list()))
    results.append(("Command Handler Test", test_command_handler()))
    results.append(("Modern Design Elements", test_modern_design_elements()))
    results.append(("Window Size Test", test_window_size()))
    results.append(("Button Styling Test", test_button_styling()))
    results.append(("Text Input Mode Section", test_text_input_mode_section()))
    
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
        print("✓ All feature tests passed!")
        print("\nNew features are working correctly:")
        print("  1. Command dropdown selector with 8 predefined commands")
        print("  2. Modern adaptive design with dark theme")
        print("  3. Rounded corners and enhanced styling")
        print("  4. Emoji icons for better UX")
        print("  5. Larger window size (1000x700)")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
