# Quick Start Guide

## Quick Installation (Linux/macOS)

```bash
# 1. Clone the repository (if not already cloned)
git clone https://github.com/mrDarky/voice_helper.git
cd voice_helper

# 2. Run setup script
./setup.sh

# 3. Activate virtual environment
source venv/bin/activate

# 4. Run the application
python main.py
```

## Quick Installation (Windows)

```cmd
REM 1. Clone the repository (if not already cloned)
git clone https://github.com/mrDarky/voice_helper.git
cd voice_helper

REM 2. Run setup script
setup.bat

REM 3. Activate virtual environment
venv\Scripts\activate.bat

REM 4. Run the application
python main.py
```

## First Time Setup

### 1. Download a Whisper Model

When you first open the application:

1. Click the **"Models"** button
2. Choose a model size:
   - **tiny** (39 MB) - Fastest, least accurate
   - **base** (74 MB) - Fast, good for simple commands
   - **small** (244 MB) - Balanced
   - **medium** (769 MB) - More accurate
   - **large** (1550 MB) - Most accurate, slowest
3. Click **"Download"** next to your chosen model
4. Wait for download to complete
5. Click **"Set Active"** to enable the model

### 2. Configure Settings

1. Click **"Settings"** button
2. Configure your preferences:
   - **Trigger Phrase**: The phrase to activate the assistant (default: "hey assistant")
   - **Translation API**: Choose Google or DeepL
   - **Voice Answer**: Enable to hear translations spoken back
3. Click **"Save"**

### 3. Start Using Voice Commands

1. Return to main screen (click **"Main"** button)
2. Click **"Start Listening"**
3. Say your trigger phrase
4. Give a command

## Example Usage

### Translation Example

1. Say: **"hey assistant"** (your trigger phrase)
2. Wait for beep/confirmation
3. Say: **"translate to Spanish"**
4. Wait for prompt
5. Say: **"Hello, how are you today?"**
6. See the translation in a popup window

### Supported Commands

- **translate to [language]**: Translates spoken text to target language

### Supported Languages

English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi

## Troubleshooting

### "No active model" error
- Go to Models screen and download + activate a model

### Microphone not working
- Check system permissions
- Make sure microphone is connected
- Test microphone in system settings

### Translation not working
- Check internet connection (required for translation APIs)
- Try switching between Google and DeepL in settings

### App crashes on startup
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Check that FFmpeg is installed on your system
- Try a different model (tiny is most reliable)

## System Requirements

- Python 3.8 or higher
- 2GB RAM minimum (4GB recommended)
- Internet connection (for downloading models and translations)
- Microphone
- Speakers (optional, for voice answers)

## Performance Tips

- Use **tiny** or **base** models for faster response
- Disable voice answers if you only need text translations
- Close other applications for better microphone quality
- Speak clearly and at a normal pace
