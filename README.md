# Voice Helper

A desktop voice assistant application built with Python, Kivy, and OpenAI Whisper. This app allows you to control various functions using voice commands, including translation services.

## Features

- **Whisper Model Management**: Download and manage different Whisper model versions (tiny, base, small, medium, large)
- **Voice Trigger**: Activate the assistant with a customizable trigger phrase
- **Translation**: Translate spoken text to different languages using Google Translate or DeepL
- **Voice Response**: Optional text-to-speech for translation results
- **Settings**: Configure trigger phrases, translation API, and voice output

## Installation

### Prerequisites

- Python 3.8 or higher
- PyAudio system dependencies
- FFmpeg (required by Whisper)

#### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev ffmpeg xclip
```

Note: `xclip` is optional but recommended for clipboard functionality in Kivy applications.

#### macOS
```bash
brew install portaudio ffmpeg
```

#### Windows
- Install FFmpeg from https://ffmpeg.org/download.html
- PyAudio may require additional setup

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
python main.py
```

### Getting Started

1. **Download a Whisper Model**:
   - Click "Models" button
   - Select a model size (tiny is fastest, large is most accurate)
   - Click "Download" button
   - Wait for the download to complete
   - Click "Set Active" to enable the model

2. **Configure Settings**:
   - Click "Settings" button
   - Set your trigger phrase (e.g., "hey assistant")
   - Choose translation API (Google or DeepL)
   - Enable/disable voice answers
   - Click "Save"

3. **Start Using Voice Commands**:
   - Click "Start Listening" on the main screen
   - Say your trigger phrase (e.g., "hey assistant")
   - Give a command, for example:
      - "Translate to Spanish" - then speak the text you want to translate
      - "Translate from Russian to English" - then speak the text you want to translate
      - "Translate from English to Russian" - then speak the text you want to translate

4. **Use Text Input Mode** (No Voice Required):
   - On the main screen, find the "Text Input Mode" section
   - Enter the text you want to translate in the "Text to translate" field
   - Enter a command in the "Command" field (e.g., "translate from russian to english")
   - Click "Execute" button
   - The translation will appear in the log and in a popup

## Commands

### Translation Commands

#### Voice Mode
```
[Trigger Phrase] translate to [language]
[Trigger Phrase] translate from [source_language] to [target_language]
```

Examples:
1. Say: "hey assistant"
2. Say: "translate to Spanish"
3. The app will prompt you to speak the text to translate
4. Say: "Hello, how are you?"
5. The app will show and optionally speak the translation

Or for bidirectional translation:
1. Say: "hey assistant"
2. Say: "translate from russian to english"
3. The app will prompt you to speak the text to translate
4. Say the Russian text
5. The app will show the English translation

#### Text Mode (No Voice Required)
1. Enter text to translate in the "Text to translate" field
2. Enter command in the "Command" field:
   - `translate from russian to english`
   - `translate from english to russian`
   - `translate to spanish`
3. Click "Execute" button
4. View the translation in the popup

### Supported Command Formats
- `translate to [language]` - Auto-detects source language
- `translate from [source] to [target]` - Explicit source and target languages
- Examples:
  - `translate from russian to english`
  - `translate from english to russian`
  - `translate from spanish to french`
  - `translate to german`

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh-CN)
- Japanese (ja)
- Korean (ko)
- Arabic (ar)
- Hindi (hi)

## Database

The app uses SQLite to store:
- Whisper model information (downloaded status, active model)
- User settings (trigger phrase, API preferences)

Database file: `voice_helper.db`

## Troubleshooting

### PyAudio Installation Issues
If you encounter errors installing PyAudio:
```bash
# Ubuntu/Debian
sudo apt-get install python3-dev portaudio19-dev
pip install pyaudio

# macOS
brew install portaudio
pip install pyaudio
```

### Clipboard Warning (Linux)
If you see a warning about "Cutbuffer provider" or "xclip not found":
```bash
# Ubuntu/Debian
sudo apt-get install xclip

# Fedora/RHEL
sudo dnf install xclip

# Arch Linux
sudo pacman -S xclip
```
This warning is not critical and won't affect the main functionality of the application.

### Signal Handler Error
If you encounter "ValueError: signal only works in main thread":
- This has been fixed in the latest version
- Ensure you're running the latest code from the repository
- The signal handler now gracefully handles being called from non-main threads

### Microphone Permission
Make sure your application has microphone access permissions in your system settings.

### Model Download Issues
- Ensure you have a stable internet connection
- First download may take time depending on model size
- Models are cached by the Whisper library

## Project Structure

```
voice_helper/
├── main.py              # Main application file
├── database.py          # Database management
├── voice_processor.py   # Voice recognition and processing
├── translator.py        # Translation service
├── voicehelper.kv      # Kivy UI design file
├── requirements.txt     # Python dependencies
└── voice_helper.db     # SQLite database (created at runtime)
```

## License

MIT License