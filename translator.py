from deep_translator import GoogleTranslator
import requests
from database import Database

class TranslationService:
    def __init__(self):
        self.db = Database()
    
    def translate(self, text, target_lang):
        """Translate text to target language"""
        api = self.db.get_setting('translation_api')
        
        try:
            if api == 'google':
                return self._translate_google(text, target_lang)
            elif api == 'deepl':
                return self._translate_deepl(text, target_lang)
            else:
                return self._translate_google(text, target_lang)
        except Exception as e:
            return f"Translation error: {e}"
    
    def _translate_google(self, text, target_lang):
        """Translate using Google Translate (free)"""
        translator = GoogleTranslator(source='auto', target=target_lang)
        return translator.translate(text)
    
    def _translate_deepl(self, text, target_lang):
        """Translate using DeepL free API"""
        # Note: This would require a DeepL API key
        # For now, fall back to Google
        return self._translate_google(text, target_lang)
    
    def parse_translate_command(self, command):
        """Parse translate command to extract target language"""
        command_lower = command.lower()
        
        # Simple parsing for "translate to [language]"
        if 'translate to' in command_lower:
            parts = command_lower.split('translate to')
            if len(parts) > 1:
                lang_part = parts[1].strip().split()[0]
                return self._language_to_code(lang_part)
        
        return 'en'  # Default to English
    
    def _language_to_code(self, language):
        """Convert language name to code"""
        lang_map = {
            'english': 'en',
            'spanish': 'es',
            'french': 'fr',
            'german': 'de',
            'italian': 'it',
            'portuguese': 'pt',
            'russian': 'ru',
            'chinese': 'zh-CN',
            'japanese': 'ja',
            'korean': 'ko',
            'arabic': 'ar',
            'hindi': 'hi',
        }
        return lang_map.get(language, language)
