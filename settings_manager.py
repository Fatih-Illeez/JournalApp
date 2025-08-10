import os
import json
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QFont


class SettingsManager:
    def __init__(self, parent):
        self.parent = parent

    def setup_settings(self):
        self.parent.setWindowTitle("SecureJournal Pro")
        self.parent.setGeometry(100, 100, 1400, 900)
        self.parent.journal_dir = os.path.expanduser("~/.encrypted_journal_pro")
        self.parent.notebooks_dir = os.path.join(self.parent.journal_dir, "notebooks")
        os.makedirs(self.parent.journal_dir, exist_ok=True)
        os.makedirs(self.parent.notebooks_dir, exist_ok=True)
        self.parent.key_path = os.path.join(self.parent.journal_dir, "master.key")
        self.parent.config_path = os.path.join(self.parent.journal_dir, "config.json")
        self.parent.current_notebook = "Default"
        self.load_config()
        
    def load_config(self):
        self.parent.config = {
            "theme": "dark",
            "font_size": 12,
            "auto_save": True,
            "word_wrap": True
        }
        if os.path.exists(self.parent.config_path):
            try:
                with open(self.parent.config_path, 'r') as f:
                    self.parent.config.update(json.load(f))
            except:
                pass
    
    def save_config(self):
        with open(self.parent.config_path, 'w') as f:
            json.dump(self.parent.config, f)
    
    def load_or_create_key(self):
        if os.path.exists(self.parent.key_path):
            with open(self.parent.key_path, "rb") as f:
                self.parent.key = f.read()
        else:
            self.parent.key = Fernet.generate_key()
            with open(self.parent.key_path, "wb") as f:
                f.write(self.parent.key)
        self.parent.fernet = Fernet(self.parent.key)

    def increase_font_size(self):
        self.parent.config["font_size"] = min(24, self.parent.config["font_size"] + 1)
        if hasattr(self.parent, 'editor'):
            self.parent.editor.setFont(QFont("Segoe UI", self.parent.config["font_size"]))
        self.save_config()
    
    def decrease_font_size(self):
        self.parent.config["font_size"] = max(8, self.parent.config["font_size"] - 1)
        if hasattr(self.parent, 'editor'):
            self.parent.editor.setFont(QFont("Segoe UI", self.parent.config["font_size"]))
        self.save_config()
    
    def toggle_word_wrap(self, checked):
        self.parent.config["word_wrap"] = checked
        if hasattr(self.parent, 'editor'):
            self.parent.editor.setLineWrapMode(QTextEdit.WidgetWidth if checked else QTextEdit.NoWrap)
        self.save_config()