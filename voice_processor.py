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
import os
import sys
import signal
from contextlib import contextmanager
from database import Database


@contextmanager
def suppress_alsa_errors():
    """Context manager to suppress ALSA/JACK error messages"""
    original_stderr_fd = None
    
    try:
        # Try to redirect file descriptor level stderr to devnull
        # This suppresses C-level ALSA/JACK errors that can't be caught in Python
        original_stderr_fd = os.dup(2)
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, 2)
        os.close(devnull)
        
        yield
    finally:
        # Restore original stderr file descriptor
        if original_stderr_fd is not None:
            os.dup2(original_stderr_fd, 2)
            os.close(original_stderr_fd)


class AbortException(Exception):
    """Custom exception to convert SIGABRT into a catchable Python exception"""
    pass


@contextmanager
def catch_abort_signal():
    """Context manager to catch SIGABRT and convert it to an exception
    
    This is critical for catching PortAudio assertion failures that would
    otherwise kill the process with "Aborted (core dumped)".
    
    Note: Signal handlers can only be installed in the main thread.
    When called from a non-main thread, this context manager will still
    work but won't install the signal handler (it will just yield).
    """
    original_handler = None
    signal_installed = False
    
    def abort_handler(signum, frame):
        """Signal handler that raises an exception instead of terminating"""
        raise AbortException("SIGABRT caught - PortAudio assertion failure detected")
    
    try:
        # Only install signal handler if we're in the main thread
        # signal.signal() raises ValueError if called from non-main thread
        if threading.current_thread() is threading.main_thread():
            try:
                original_handler = signal.signal(signal.SIGABRT, abort_handler)
                signal_installed = True
            except ValueError:
                # Can't install signal handler (not in main thread or main interpreter)
                pass
        yield
    finally:
        # Restore original SIGABRT handler only if we installed one
        if signal_installed and original_handler is not None:
            try:
                signal.signal(signal.SIGABRT, original_handler)
            except ValueError:
                # Can't restore signal handler
                pass

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
        """Check if audio input devices are available
        
        This method carefully validates audio hardware availability to prevent
        the PortAudio assertion failure that causes "Aborted (core dumped)".
        
        Uses a SIGABRT signal handler to catch assertion failures that would
        otherwise kill the process.
        """
        if not SR_AVAILABLE:
            return False
        
        # Suppress ALSA/JACK error messages during audio hardware detection
        with suppress_alsa_errors():
            # Catch SIGABRT to prevent process termination from PortAudio assertions
            with catch_abort_signal():
                try:
                    import pyaudio
                    p = pyaudio.PyAudio()
                    
                    try:
                        # Get device count
                        device_count = p.get_device_count()
                        
                        # Check if there are actual devices
                        if device_count == 0:
                            print("Warning: No audio devices found")
                            return False
                        
                        # Check for valid input devices
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
                    
                except AbortException:
                    # PortAudio assertion was caught - audio not available
                    print("Warning: Audio hardware initialization failed (assertion caught)")
                    return False
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
        with suppress_alsa_errors():
            with catch_abort_signal():
                try:
                    microphone = sr.Microphone()
                    with microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=1)
                except AbortException:
                    print("Error: Audio hardware assertion failure during initialization")
                    self.is_listening = False
                    return
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
            with suppress_alsa_errors():
                with catch_abort_signal():
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
                    
                    except AbortException:
                        print("Error: Audio hardware assertion failure")
                        time.sleep(1)
                        continue
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
            
        with suppress_alsa_errors():
            with catch_abort_signal():
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
                
                except AbortException:
                    print("Error: Audio hardware assertion failure during command listening")
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
            
        with suppress_alsa_errors():
            # Also catch SIGABRT in case audio hardware state changed
            with catch_abort_signal():
                try:
                    # Create a new microphone instance for single listening
                    microphone = sr.Microphone()
                    with microphone as source:
                        self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                        print("Listening...")
                        audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    
                    text = self.recognizer.recognize_google(audio)
                    return text
                except AbortException:
                    print("Error: Audio hardware assertion failure")
                    return None
                except Exception as e:
                    print(f"Error in listen_once: {e}")
                    return None
