try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False
    
import requests
from database import Database

class TranslationService:
    def __init__(self):
        self.db = Database()
    
    def translate(self, text, target_lang, source_lang='auto'):
        """Translate text from source language to target language"""
        api = self.db.get_setting('translation_api')
        
        try:
            if api == 'google':
                return self._translate_google(text, target_lang, source_lang)
            elif api == 'deepl':
                return self._translate_deepl(text, target_lang, source_lang)
            else:
                return self._translate_google(text, target_lang, source_lang)
        except Exception as e:
            return f"Translation error: {e}"
    
    def _translate_google(self, text, target_lang, source_lang='auto'):
        """Translate using Google Translate (free)"""
        if not TRANSLATOR_AVAILABLE:
            return f"Translation not available - install deep-translator: pip install deep-translator"
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    
    def _translate_deepl(self, text, target_lang, source_lang='auto'):
        """Translate using DeepL free API"""
        # Note: This would require a DeepL API key
        # For now, fall back to Google
        return self._translate_google(text, target_lang, source_lang)
    
    def parse_translate_command(self, command):
        """Parse translate command to extract source and target languages
        
        Returns tuple: (source_lang, target_lang)
        Supports formats:
        - "translate to [language]" -> (auto, language)
        - "translate from [lang1] to [lang2]" -> (lang1, lang2)
        - "translate russian to english" -> (ru, en)
        - "translate english to russian" -> (en, ru)
        """
        command_lower = command.lower()
        
        # Check for "from X to Y" pattern
        if 'from' in command_lower and 'to' in command_lower:
            # Split by 'from' and 'to'
            parts = command_lower.split('from')
            if len(parts) > 1:
                from_to_parts = parts[1].split('to')
                if len(from_to_parts) >= 2:
                    source_lang = from_to_parts[0].strip()
                    target_lang = from_to_parts[1].strip().split()[0]
                    return (self._language_to_code(source_lang), self._language_to_code(target_lang))
        
        # Check for simple "to [language]" pattern
        if 'to' in command_lower:
            parts = command_lower.split('to')
            if len(parts) > 1:
                target_lang = parts[1].strip().split()[0]
                return ('auto', self._language_to_code(target_lang))
        
        # Default to auto-detect to English
        return ('auto', 'en')
    
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
