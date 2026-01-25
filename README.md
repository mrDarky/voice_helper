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
sudo apt-get install python3-pyaudio portaudio19-dev ffmpeg
```

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
     - "Translate to French" - then speak the text you want to translate

## Commands

### Translation Command
```
[Trigger Phrase] translate to [language]
```

Example:
1. Say: "hey assistant"
2. Say: "translate to Spanish"
3. The app will prompt you to speak the text to translate
4. Say: "Hello, how are you?"
5. The app will show and optionally speak the translation

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