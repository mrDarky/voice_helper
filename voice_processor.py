try:
    import speech_recognition as sr
    SR_AVAILABLE = True
except ImportError:
    SR_AVAILABLE = False
    
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    
import threading
import time
from database import Database

class VoiceProcessor:
    def __init__(self):
        if not SR_AVAILABLE:
            print("Warning: SpeechRecognition not available")
        if not WHISPER_AVAILABLE:
            print("Warning: Whisper not available")
            
        self.recognizer = sr.Recognizer() if SR_AVAILABLE else None
        self.is_listening = False
        self.db = Database()
        self.whisper_model = None
        self.listen_thread = None
        self.on_trigger_detected = None
        self.on_command_received = None
        
    def load_whisper_model(self):
        """Load the active Whisper model"""
        if not WHISPER_AVAILABLE:
            print("Error: Whisper not installed")
            return False
            
        active_model = self.db.get_active_model()
        if active_model:
            try:
                self.whisper_model = whisper.load_model(active_model)
                return True
            except Exception as e:
                print(f"Error loading model: {e}")
                return False
        return False
    
    def start_listening(self):
        """Start listening for trigger phrase"""
        if not SR_AVAILABLE:
            print("Error: SpeechRecognition not installed")
            return
            
        if self.is_listening:
            return
        
        self.is_listening = True
        self.listen_thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.listen_thread.start()
    
    def stop_listening(self):
        """Stop listening"""
        self.is_listening = False
        if self.listen_thread:
            self.listen_thread.join(timeout=2)
    
    def _listen_loop(self):
        """Main listening loop"""
        trigger_phrase = self.db.get_setting('trigger_phrase').lower()
        
        # Create a new microphone instance for ambient noise adjustment
        microphone = sr.Microphone() if SR_AVAILABLE else None
        with microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while self.is_listening:
            try:
                # Create a new microphone instance for each listening iteration
                microphone = sr.Microphone() if SR_AVAILABLE else None
                with microphone as source:
                    print("Listening for trigger phrase...")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                
                # Use Google Speech Recognition for trigger detection
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                if trigger_phrase in text:
                    print("Trigger detected!")
                    if self.on_trigger_detected:
                        self.on_trigger_detected()
                    
                    # Listen for command
                    self._listen_for_command()
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Error in listen loop: {e}")
                time.sleep(1)
    
    def _listen_for_command(self):
        """Listen for actual command after trigger"""
        try:
            # Create a new microphone instance for command listening
            microphone = sr.Microphone() if SR_AVAILABLE else None
            with microphone as source:
                print("Listening for command...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"Command: {text}")
            
            if self.on_command_received:
                self.on_command_received(text)
                
        except Exception as e:
            print(f"Error listening for command: {e}")
    
    def listen_once(self):
        """Listen for a single phrase (for translation input)"""
        try:
            # Create a new microphone instance for single listening
            microphone = sr.Microphone() if SR_AVAILABLE else None
            with microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return text
        except Exception as e:
            print(f"Error in listen_once: {e}")
            return None
