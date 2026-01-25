# Application Architecture

## Overview

Voice Helper is a modular desktop application built with Python, Kivy, and SQLite.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                       Voice Helper App                       │
│                         (main.py)                            │
└──────────────┬────────────────────────────────┬──────────────┘
               │                                │
    ┌──────────▼─────────┐           ┌─────────▼──────────┐
    │   User Interface   │           │  Core Components   │
    │    (Kivy UI)       │           │                    │
    └──────────┬─────────┘           └────────┬───────────┘
               │                               │
    ┌──────────▼──────────────────────────────▼───────────┐
    │                                                      │
    │  ┌──────────────┐  ┌──────────────┐  ┌───────────┐ │
    │  │ Main Screen  │  │Models Screen │  │  Settings │ │
    │  │              │  │              │  │   Screen  │ │
    │  │ - Start/Stop │  │ - Download   │  │ - Trigger │ │
    │  │ - Status     │  │ - Activate   │  │ - API     │ │
    │  │ - Logs       │  │ - List       │  │ - Voice   │ │
    │  └──────────────┘  └──────────────┘  └───────────┘ │
    └──────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │              Core Components Layer                    │
    ├──────────────────────────────────────────────────────┤
    │                                                       │
    │  ┌─────────────────┐   ┌──────────────────────┐     │
    │  │ Database        │   │ Voice Processor      │     │
    │  │ (database.py)   │   │ (voice_processor.py) │     │
    │  │                 │   │                      │     │
    │  │ - Models Table  │   │ - Listening Loop     │     │
    │  │ - Settings      │   │ - Trigger Detection  │     │
    │  │ - CRUD Ops      │   │ - Command Capture    │     │
    │  └─────────────────┘   └──────────────────────┘     │
    │                                                       │
    │  ┌─────────────────────────────────────────────┐     │
    │  │ Translation Service                         │     │
    │  │ (translator.py)                             │     │
    │  │                                             │     │
    │  │ - Google Translate                          │     │
    │  │ - DeepL Support                             │     │
    │  │ - Language Detection                        │     │
    │  └─────────────────────────────────────────────┘     │
    └──────────────────────────────────────────────────────┘

    ┌──────────────────────────────────────────────────────┐
    │            External Dependencies Layer                │
    ├──────────────────────────────────────────────────────┤
    │                                                       │
    │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐    │
    │  │  Whisper │  │  Speech  │  │  Translation    │    │
    │  │  (OpenAI)│  │  Recog.  │  │  APIs           │    │
    │  └──────────┘  └──────────┘  └─────────────────┘    │
    │                                                       │
    │  ┌──────────┐  ┌──────────┐  ┌─────────────────┐    │
    │  │  PyAudio │  │  pyttsx3 │  │  SQLite         │    │
    │  │          │  │  (TTS)   │  │  (Database)     │    │
    │  └──────────┘  └──────────┘  └─────────────────┘    │
    └──────────────────────────────────────────────────────┘
```

## Component Details

### Main Application (main.py)
- **VoiceHelperApp**: Main application class
- **MainScreen**: Primary UI screen with start/stop controls
- **ModelsScreen**: Whisper model management interface
- **SettingsScreen**: Configuration interface
- Handles screen navigation and component coordination

### Database (database.py)
- **Database Class**: SQLite wrapper
- **Tables**:
  - `whisper_models`: Model metadata and status
  - `settings`: User preferences
- **Operations**: CRUD for models and settings

### Voice Processor (voice_processor.py)
- **VoiceProcessor Class**: Audio handling and recognition
- **Features**:
  - Background listening thread
  - Trigger phrase detection
  - Command capture after trigger
  - Integration with Speech Recognition library

### Translation Service (translator.py)
- **TranslationService Class**: Translation handling
- **Features**:
  - Google Translate integration (free)
  - DeepL support (requires API key)
  - Command parsing ("translate to [language]")
  - Language code mapping

## Data Flow

### 1. Application Startup
```
User → run.py → Dependency Check → main.py → Database Init → UI Load
```

### 2. Model Download Flow
```
User clicks "Download" → ModelsScreen → Threading → Whisper API → 
Model Downloaded → Database Update → UI Refresh
```

### 3. Voice Command Flow
```
User clicks "Start" → VoiceProcessor.start_listening() → 
Background Thread → Microphone Listening → 
Trigger Detected → Listen for Command → 
Parse Command → Execute Action → Show Result
```

### 4. Translation Flow
```
Command: "translate to Spanish" → Parse Target Language → 
Listen for Text → Capture Audio → 
Translation API → Get Result → 
Show Popup + Optional TTS → User sees/hears translation
```

## Threading Model

- **Main Thread**: UI and Kivy event loop
- **Voice Listening Thread**: Continuous microphone monitoring
- **Download Threads**: Model downloads (non-blocking)
- **Translation Threads**: API calls (non-blocking)

All background threads use `Clock.schedule_once()` to safely update UI.

## Database Schema

### whisper_models Table
```sql
CREATE TABLE whisper_models (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    downloaded INTEGER DEFAULT 0,
    active INTEGER DEFAULT 0,
    download_date TEXT
)
```

### settings Table
```sql
CREATE TABLE settings (
    key TEXT PRIMARY KEY,
    value TEXT
)
```

## Configuration

Settings stored in database:
- `trigger_phrase`: Voice activation phrase
- `translation_api`: 'google' or 'deepl'
- `voice_answer`: 'true' or 'false'
- `target_language`: Default target language code

## Error Handling

- **No Active Model**: Prompt user to download and activate
- **Microphone Issues**: Silent failure with console logging
- **Network Errors**: Graceful degradation with error messages
- **Missing Dependencies**: Pre-flight check in run.py
