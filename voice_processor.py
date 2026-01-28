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
        self.audio_available = self._check_audio_availability()
    
    def _check_audio_availability(self):
        """Check if audio input devices are available"""
        if not SR_AVAILABLE:
            return False
        
        try:
            # Try to create a microphone instance to check if audio devices are available
            # This will fail with an OSError or assertion if no audio hardware is present
            import pyaudio
            p = pyaudio.PyAudio()
            
            try:
                # Check if there are any input devices
                device_count = p.get_device_count()
                has_input_device = False
                
                for i in range(device_count):
                    try:
                        device_info = p.get_device_info_by_index(i)
                        if device_info.get('maxInputChannels', 0) > 0:
                            has_input_device = True
                            break
                    except Exception:
                        continue
                
                if not has_input_device:
                    print("Warning: No audio input devices found")
                    return False
                
                return True
            finally:
                # Always terminate PyAudio instance to avoid resource leaks
                p.terminate()
            
        except (OSError, AssertionError) as e:
            print(f"Warning: Audio hardware not available: {e}")
            return False
        except Exception as e:
            print(f"Warning: Could not check audio availability: {e}")
            return False
        
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
        
        if not self.audio_available:
            print("Error: No audio input devices available")
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
        if not SR_AVAILABLE:
            print("Error: SpeechRecognition not available")
            return
        
        if not self.audio_available:
            print("Error: No audio input devices available")
            return
            
        trigger_phrase = self.db.get_setting('trigger_phrase').lower()
        
        # Adjust for ambient noise once at the start
        # Note: This adjusts the recognizer's energy_threshold, which persists
        # across all microphone instances, so we only need to do it once
        try:
            microphone = sr.Microphone()
            with microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Error initializing microphone: {e}")
            self.is_listening = False
            if self.on_command_received:
                # Notify that listening failed
                import kivy.clock
                kivy.clock.Clock.schedule_once(
                    lambda dt: print("Listening stopped due to audio error"), 0)
            return
        
        while self.is_listening:
            try:
                # Create a new microphone instance for each listening iteration
                microphone = sr.Microphone()
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
                # Don't break on transient errors, but add a delay
                time.sleep(1)
    
    def _listen_for_command(self):
        """Listen for actual command after trigger"""
        if not SR_AVAILABLE:
            print("Error: SpeechRecognition not available")
            return
        
        if not self.audio_available:
            print("Error: No audio input devices available")
            return
            
        try:
            # Create a new microphone instance for command listening
            microphone = sr.Microphone()
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
        if not SR_AVAILABLE:
            print("Error: SpeechRecognition not available")
            return None
        
        if not self.audio_available:
            print("Error: No audio input devices available")
            return None
            
        try:
            # Create a new microphone instance for single listening
            microphone = sr.Microphone()
            with microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            return text
        except Exception as e:
            print(f"Error in listen_once: {e}")
            return None
