import speech_recognition as sr
import threading
import time
import whisper
from database import Database

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.db = Database()
        self.whisper_model = None
        self.listen_thread = None
        self.on_trigger_detected = None
        self.on_command_received = None
        
    def load_whisper_model(self):
        """Load the active Whisper model"""
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
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while self.is_listening:
            try:
                with self.microphone as source:
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
            with self.microphone as source:
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
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return text
        except Exception as e:
            print(f"Error in listen_once: {e}")
            return None
