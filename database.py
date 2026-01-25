import sqlite3
import os

class Database:
    def __init__(self, db_path='voice_helper.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with necessary tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table for Whisper models
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whisper_models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                downloaded INTEGER DEFAULT 0,
                active INTEGER DEFAULT 0,
                download_date TEXT
            )
        ''')
        
        # Table for settings
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        # Initialize default settings
        cursor.execute('''
            INSERT OR IGNORE INTO settings (key, value) VALUES
            ('trigger_phrase', 'hey assistant'),
            ('translation_api', 'google'),
            ('voice_answer', 'false'),
            ('target_language', 'en')
        ''')
        
        # Initialize available Whisper models
        models = ['tiny', 'base', 'small', 'medium', 'large']
        for model in models:
            cursor.execute('''
                INSERT OR IGNORE INTO whisper_models (name) VALUES (?)
            ''', (model,))
        
        conn.commit()
        conn.close()
    
    def get_all_models(self):
        """Get all Whisper models"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM whisper_models')
        models = cursor.fetchall()
        conn.close()
        return models
    
    def update_model_downloaded(self, model_name, downloaded=True):
        """Mark model as downloaded"""
        from datetime import datetime
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if downloaded else None
        cursor.execute('''
            UPDATE whisper_models SET downloaded=?, download_date=?
            WHERE name=?
        ''', (1 if downloaded else 0, date_str, model_name))
        conn.commit()
        conn.close()
    
    def set_active_model(self, model_name):
        """Set a model as active (deactivate others)"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Deactivate all models
        cursor.execute('UPDATE whisper_models SET active=0')
        
        # Activate selected model
        cursor.execute('UPDATE whisper_models SET active=1 WHERE name=?', (model_name,))
        
        conn.commit()
        conn.close()
    
    def get_active_model(self):
        """Get the currently active model"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT name FROM whisper_models WHERE active=1')
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def get_setting(self, key):
        """Get a setting value"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT value FROM settings WHERE key=?', (key,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None
    
    def set_setting(self, key, value):
        """Set a setting value"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)
        ''', (key, value))
        conn.commit()
        conn.close()
