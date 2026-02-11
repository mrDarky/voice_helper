import sys
import traceback
from datetime import datetime
import threading

def print_error_message(title, details, suggestions=None):
    """Helper function to print formatted error messages"""
    print(f"\n{'='*60}")
    print(f"ERROR: {title}")
    print(f"{'='*60}")
    print(details)
    if suggestions is not None:
        print(f"\n{suggestions}")
    print(f"{'='*60}\n")

# Check for critical dependencies first
try:
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager, Screen
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.button import Button
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.graphics import Color, RoundedRectangle
except ImportError as e:
    print_error_message(
        "Missing required dependency",
        f"Failed to import: {e}",
        "Please install all dependencies:\n"
        "  pip install -r requirements.txt\n"
        "\n"
        "Or run the setup script:\n"
        "  ./setup.sh (Linux/macOS)\n"
        "  setup.bat (Windows)"
    )
    sys.exit(1)

try:
    from database import Database
    from voice_processor import VoiceProcessor
    from translator import TranslationService
except ImportError as e:
    print_error_message(
        "Failed to import application modules",
        f"Error: {e}",
        "Please ensure you're running from the correct directory\n"
        "and all project files are present."
    )
    sys.exit(1)

try:
    import pyttsx3
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False

class MainScreen(Screen):
    # Predefined command list for the dropdown
    PREDEFINED_COMMANDS = [
        'translate from russian to english',
        'translate from english to russian',
        'translate from spanish to english',
        'translate from french to english',
        'translate to spanish',
        'translate to french',
        'translate to german',
        'Custom command...'
    ]
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.app = None
        self.is_listening = False
    
    def on_kv_post(self, base_widget):
        """Called after the kv file is loaded"""
        # Set the command values from Python for better maintainability
        if 'command_spinner' in self.ids:
            self.ids.command_spinner.values = self.PREDEFINED_COMMANDS
    
    def on_enter(self):
        """Called when screen is displayed"""
        if self.app:
            self.update_status()
    
    def update_status(self):
        """Update status display"""
        active_model = self.app.db.get_active_model()
        self.ids.active_model_label.text = f'Active Model: {active_model if active_model else "None"}'
    
    def on_command_selected(self, command_text):
        """Handle command selection from spinner"""
        if command_text and command_text != 'Select command...' and command_text != 'Custom command...':
            # Auto-fill the text input with the selected command
            self.ids.text_command_input.text = command_text
    
    def toggle_listening(self):
        """Toggle listening on/off"""
        if self.is_listening:
            self.stop_listening()
        else:
            self.start_listening()
    
    def start_listening(self):
        """Start voice listening"""
        if not self.app.db.get_active_model():
            self.show_popup('Error', 'Please select an active Whisper model first!')
            return
        
        if not self.app.voice_processor.audio_available:
            self.show_popup('Error', 
                'No audio input devices available.\n\n'
                'Please check:\n'
                '  1. Microphone is connected\n'
                '  2. System audio permissions are granted\n'
                '  3. Audio drivers are installed')
            return
        
        self.is_listening = True
        self.ids.start_button.text = '⏹️ Stop Listening'
        self.ids.start_button.background_color = (0.8, 0.2, 0.2, 1)
        self.ids.status_label.text = 'Status: Listening for trigger...'
        self.add_log('Started listening for trigger phrase')
        
        self.app.voice_processor.start_listening()
    
    def stop_listening(self):
        """Stop voice listening"""
        self.is_listening = False
        self.ids.start_button.text = '🎤 Start Listening'
        self.ids.start_button.background_color = (0.18, 0.7, 0.18, 1)
        self.ids.status_label.text = 'Status: Stopped'
        self.add_log('Stopped listening')
        
        self.app.voice_processor.stop_listening()
    
    def process_text_command(self):
        """Process text command entered in text field"""
        command = self.ids.text_command_input.text.strip()
        if not command:
            self.show_popup('Error', 'Please select or enter a command')
            return
        
        self.add_log(f'Text command: {command}')
        # Keep command in field for reference, but user can clear it manually if needed
        
        # Process the command
        command_lower = command.lower()
        
        if 'translate' in command_lower:
            self.handle_text_translate_command(command)
        else:
            self.add_log('Unknown command. Try: "translate from russian to english"')
    
    def handle_text_translate_command(self, command):
        """Handle text-based translation command"""
        source_lang, target_lang = self.app.translator.parse_translate_command(command)
        self.add_log(f'Translation from {source_lang} to {target_lang} requested')
        
        # Get the text to translate from the text input field
        text_to_translate = self.ids.text_input_field.text.strip()
        
        if not text_to_translate:
            self.show_popup('Info', 'Please enter text to translate in the input field')
            return
        
        self.ids.text_input_field.text = ''  # Clear input
        self.app.do_translate(text_to_translate, target_lang, source_lang)
    
    def add_log(self, message):
        """Add message to log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        current_text = self.ids.log_label.text
        if current_text == 'Waiting to start...':
            current_text = ''
        new_text = f'[{timestamp}] {message}\n{current_text}'
        self.ids.log_label.text = new_text
    
    def show_popup(self, title, message):
        """Show popup message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text='Close', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class ModelsScreen(Screen):
    def __init__(self, **kwargs):
        super(ModelsScreen, self).__init__(**kwargs)
        self.app = None
    
    def on_enter(self):
        """Called when screen is displayed"""
        if self.app:
            self.refresh_models()
    
    def refresh_models(self):
        """Refresh model lists"""
        self.ids.available_models.clear_widgets()
        self.ids.downloaded_models.clear_widgets()
        
        # Define update function once for reuse
        def update_rect(instance, value):
            instance.rect.pos = instance.pos
            instance.rect.size = instance.size
        
        models = self.app.db.get_all_models()
        
        for model in models:
            model_id, name, downloaded, active, download_date = model
            
            # Add to available models
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=8, padding=[5, 5])
            
            # Add canvas styling to the box
            with box.canvas.before:
                Color(0.25, 0.25, 0.3, 1)
                box.rect = RoundedRectangle(pos=box.pos, size=box.size, radius=[8])
            
            box.bind(pos=update_rect, size=update_rect)
            
            box.add_widget(Label(text=name, size_hint_x=0.4, color=(1, 1, 1, 0.9), bold=True))
            
            if downloaded:
                status_label = Label(text='✓ Downloaded', size_hint_x=0.3, color=(0.18, 0.7, 0.18, 1), bold=True)
            else:
                status_label = Label(text='Not Downloaded', size_hint_x=0.3, color=(1, 1, 1, 0.6))
            box.add_widget(status_label)
            
            download_btn = Button(
                text='Download' if not downloaded else 'Re-download',
                size_hint_x=0.3,
                background_normal='',
                background_color=(0.2, 0.6, 0.9, 1) if not downloaded else (0.6, 0.6, 0.6, 1),
                bold=True
            )
            download_btn.bind(on_press=lambda btn, m=name: self.download_model(m))
            box.add_widget(download_btn)
            
            self.ids.available_models.add_widget(box)
            
            # Add to downloaded models if downloaded
            if downloaded:
                dl_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=8, padding=[5, 5])
                
                # Add canvas styling to the dl_box
                with dl_box.canvas.before:
                    Color(0.25, 0.25, 0.3, 1)
                    dl_box.rect = RoundedRectangle(pos=dl_box.pos, size=dl_box.size, radius=[8])
                
                dl_box.bind(pos=update_rect, size=update_rect)
                
                dl_box.add_widget(Label(text=name, size_hint_x=0.4, color=(1, 1, 1, 0.9), bold=True))
                dl_box.add_widget(Label(
                    text=f'⭐ Active' if active else 'Inactive',
                    size_hint_x=0.3,
                    color=(0.18, 0.7, 0.18, 1) if active else (1, 1, 1, 0.6),
                    bold=active
                ))
                
                activate_btn = Button(
                    text='Set Active',
                    size_hint_x=0.3,
                    disabled=active,
                    background_normal='',
                    background_color=(0.18, 0.7, 0.18, 1) if not active else (0.4, 0.4, 0.4, 1),
                    bold=True
                )
                activate_btn.bind(on_press=lambda btn, m=name: self.set_active_model(m))
                dl_box.add_widget(activate_btn)
                
                self.ids.downloaded_models.add_widget(dl_box)
    
    def download_model(self, model_name):
        """Download a Whisper model"""
        self.show_popup('Downloading', f'Downloading {model_name} model...\nThis may take a while.')
        
        def download_thread():
            try:
                import whisper
                whisper.load_model(model_name)
                self.app.db.update_model_downloaded(model_name, True)
                Clock.schedule_once(lambda dt: self.download_complete(model_name), 0)
            except Exception as e:
                Clock.schedule_once(lambda dt: self.download_error(model_name, str(e)), 0)
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def download_complete(self, model_name):
        """Handle download completion"""
        self.show_popup('Success', f'{model_name} model downloaded successfully!')
        self.refresh_models()
    
    def download_error(self, model_name, error):
        """Handle download error"""
        self.show_popup('Error', f'Failed to download {model_name}:\n{error}')
    
    def set_active_model(self, model_name):
        """Set a model as active"""
        self.app.db.set_active_model(model_name)
        self.show_popup('Success', f'{model_name} set as active model')
        self.refresh_models()
    
    def show_popup(self, title, message):
        """Show popup message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text='Close', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.app = None
    
    def on_enter(self):
        """Called when screen is displayed"""
        if self.app:
            self.load_settings()
    
    def load_settings(self):
        """Load settings from database"""
        self.ids.trigger_phrase.text = self.app.db.get_setting('trigger_phrase')
        self.ids.translation_api.text = self.app.db.get_setting('translation_api')
        voice_answer = self.app.db.get_setting('voice_answer')
        self.ids.voice_answer.active = voice_answer == 'true'
    
    def save_settings(self):
        """Save settings to database"""
        self.app.db.set_setting('trigger_phrase', self.ids.trigger_phrase.text)
        self.app.db.set_setting('translation_api', self.ids.translation_api.text)
        self.app.db.set_setting('voice_answer', 'true' if self.ids.voice_answer.active else 'false')
        
        self.show_popup('Success', 'Settings saved successfully!')
    
    def show_popup(self, title, message):
        """Show popup message"""
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=message))
        close_btn = Button(text='Close', size_hint_y=0.3)
        content.add_widget(close_btn)
        
        popup = Popup(title=title, content=content, size_hint=(0.7, 0.4))
        close_btn.bind(on_press=popup.dismiss)
        popup.open()


class VoiceHelperApp(App):
    def build(self):
        Window.size = (1000, 700)
        Window.clearcolor = (0.12, 0.12, 0.15, 1)
        
        # Initialize components
        self.db = Database()
        self.voice_processor = VoiceProcessor()
        self.translator = TranslationService()
        
        # Set up voice callbacks
        self.voice_processor.on_trigger_detected = self.on_trigger_detected
        self.voice_processor.on_command_received = self.on_command_received
        
        # Create screen manager
        sm = ScreenManager()
        
        # Create screens
        self.main_screen = MainScreen()
        self.main_screen.app = self
        sm.add_widget(self.main_screen)
        
        self.models_screen = ModelsScreen()
        self.models_screen.app = self
        sm.add_widget(self.models_screen)
        
        self.settings_screen = SettingsScreen()
        self.settings_screen.app = self
        sm.add_widget(self.settings_screen)
        
        return sm
    
    def on_trigger_detected(self):
        """Handle trigger phrase detection"""
        Clock.schedule_once(lambda dt: self.main_screen.add_log('🎤 Trigger detected! Listening for command...'), 0)
    
    def on_command_received(self, command):
        """Handle command after trigger"""
        Clock.schedule_once(lambda dt: self.main_screen.add_log(f'Command received: {command}'), 0)
        
        # Process command
        command_lower = command.lower()
        
        if 'translate' in command_lower:
            Clock.schedule_once(lambda dt: self.handle_translate_command(command), 0)
        else:
            Clock.schedule_once(lambda dt: self.main_screen.add_log('Unknown command'), 0)
    
    def handle_translate_command(self, command):
        """Handle translation command"""
        source_lang, target_lang = self.translator.parse_translate_command(command)
        self.main_screen.add_log(f'Translation from {source_lang} to {target_lang} requested')
        self.main_screen.add_log('Please speak the text to translate...')
        
        def listen_and_translate():
            text = self.voice_processor.listen_once()
            if text:
                Clock.schedule_once(lambda dt: self.do_translate(text, target_lang, source_lang), 0)
            else:
                Clock.schedule_once(lambda dt: self.main_screen.add_log('Failed to capture text'), 0)
        
        threading.Thread(target=listen_and_translate, daemon=True).start()
    
    def do_translate(self, text, target_lang, source_lang='auto'):
        """Perform translation"""
        self.main_screen.add_log(f'Translating: "{text}"')
        
        def translate_thread():
            result = self.translator.translate(text, target_lang, source_lang)
            Clock.schedule_once(lambda dt: self.show_translation_result(text, result, target_lang), 0)
        
        threading.Thread(target=translate_thread, daemon=True).start()
    
    def show_translation_result(self, original, translation, lang):
        """Show translation result in popup"""
        self.main_screen.add_log(f'Translation: "{translation}"')
        
        # Create popup content
        content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        content.add_widget(Label(text=f'Original: {original}'))
        content.add_widget(Label(text=f'Translation ({lang}): {translation}'))
        
        close_btn = Button(text='Close', size_hint_y=0.2)
        content.add_widget(close_btn)
        
        popup = Popup(
            title='Translation Result',
            content=content,
            size_hint=(0.8, 0.5)
        )
        close_btn.bind(on_press=popup.dismiss)
        popup.open()
        
        # Voice answer if enabled
        voice_answer = self.db.get_setting('voice_answer')
        if voice_answer == 'true' and TTS_AVAILABLE:
            try:
                engine = pyttsx3.init()
                engine.say(translation)
                engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")


if __name__ == '__main__':
    try:
        VoiceHelperApp().run()
    except Exception as e:
        print_error_message(
            "Failed to start Voice Helper",
            f"{traceback.format_exc()}",
            "Please ensure all dependencies are installed:\n"
            "  pip install -r requirements.txt\n"
            "\n"
            "For more information, see README.md"
        )
        sys.exit(1)
