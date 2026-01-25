# Contributing to Voice Helper

Thank you for your interest in contributing to Voice Helper! This document provides guidelines and information for contributors.

## Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mrDarky/voice_helper.git
cd voice_helper
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate.bat  # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Run Tests

```bash
python test_components.py
```

### 4. Run Examples

```bash
python examples.py
```

## Project Structure

```
voice_helper/
├── main.py              # Main application entry point
├── database.py          # Database management
├── voice_processor.py   # Voice recognition and processing
├── translator.py        # Translation service
├── voicehelper.kv      # Kivy UI design
├── run.py              # Application launcher with dependency checks
├── test_components.py  # Component tests
├── examples.py         # Usage examples
├── requirements.txt    # Python dependencies
├── setup.sh           # Linux/macOS setup script
├── setup.bat          # Windows setup script
├── README.md          # Main documentation
├── QUICKSTART.md      # Quick start guide
├── ARCHITECTURE.md    # Architecture documentation
└── .gitignore        # Git ignore rules
```

## Coding Standards

### Python Style

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use docstrings for all classes and functions

Example:
```python
def my_function(param1, param2):
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    """
    # Implementation
    pass
```

### Imports

Order imports as follows:
1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import os
import sys

import kivy
from kivy.app import App

from database import Database
```

## Adding New Features

### 1. Voice Commands

To add a new voice command:

1. Add command detection in `main.py` → `on_command_received()`
2. Create handler method (e.g., `handle_new_command()`)
3. Update documentation

Example:
```python
def on_command_received(self, command):
    command_lower = command.lower()
    
    if 'translate' in command_lower:
        self.handle_translate_command(command)
    elif 'new_command' in command_lower:
        self.handle_new_command(command)
```

### 2. Database Schema Changes

If you need to modify the database:

1. Update `database.py` → `init_db()` method
2. Handle migration for existing databases
3. Update relevant methods

### 3. UI Changes

To modify the UI:

1. Edit `voicehelper.kv` for layout changes
2. Update corresponding Screen class in `main.py`
3. Test on different screen sizes

### 4. Settings

To add new settings:

1. Add default value in `database.py` → `init_db()`
2. Add UI controls in `SettingsScreen`
3. Update `load_settings()` and `save_settings()` methods

## Testing

### Running Tests

```bash
# Run component tests
python test_components.py

# Run examples
python examples.py

# Test without dependencies (core functionality)
python -c "from database import Database; db = Database(); print(db.get_all_models())"
```

### Manual Testing Checklist

- [ ] App starts without errors
- [ ] Can navigate between screens
- [ ] Can download and activate models
- [ ] Can modify and save settings
- [ ] Start/Stop listening works
- [ ] Voice commands are recognized
- [ ] Translation popup appears
- [ ] Voice answer works (if enabled)

## Debugging

### Enable Debug Logging

```python
# Add to main.py before imports
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Microphone not detected**: Check system permissions
2. **Model download fails**: Check internet connection
3. **UI not updating**: Ensure using `Clock.schedule_once()` for updates from threads
4. **Database locked**: Close other instances accessing the database

## Pull Request Process

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Make your changes**
4. **Test thoroughly**
5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: brief description"
   ```
6. **Push to your fork**
   ```bash
   git push origin feature/my-new-feature
   ```
7. **Create Pull Request**
   - Describe what changes were made
   - List any new dependencies
   - Note any breaking changes

## Code Review Guidelines

### What We Look For

- Code follows style guidelines
- Changes are well-tested
- Documentation is updated
- No unnecessary dependencies
- Error handling is present
- Thread-safe UI updates

### What to Avoid

- Large, unfocused PRs
- Breaking changes without migration path
- Hardcoded values that should be configurable
- Blocking operations on main thread
- Missing error handling

## Areas for Contribution

### High Priority

- [ ] Add more voice commands
- [ ] Improve translation accuracy
- [ ] Add language auto-detection
- [ ] Better error messages
- [ ] Unit test coverage

### Medium Priority

- [ ] Dark/light theme support
- [ ] Custom keyboard shortcuts
- [ ] Export translation history
- [ ] Multiple translation APIs
- [ ] Voice command history

### Nice to Have

- [ ] Plugin system
- [ ] Cloud sync settings
- [ ] Mobile app companion
- [ ] Batch translation
- [ ] Voice profiles

## Documentation

When adding features, update:

1. **README.md** - Main documentation
2. **QUICKSTART.md** - If affecting user workflow
3. **ARCHITECTURE.md** - If changing architecture
4. **Code comments** - For complex logic

## Questions?

If you have questions:

1. Check existing documentation
2. Review closed issues/PRs
3. Open a new issue with `[Question]` prefix

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Thank You!

Your contributions make Voice Helper better for everyone!
