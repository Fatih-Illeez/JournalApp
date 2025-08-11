from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QDialog, QColorDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

from auto_save_thread import AutoSaveThread
from ui_components import UIComponents
from entry_manager import EntryManager
from notebook_manager import NotebookManager
from settings_manager import SettingsManager
from security_manager import SecurityManager
from calendar_dialog import CalendarDialog
from password_dialog import PasswordDialog
from styles import get_app_stylesheet


class EncryptedJournal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_entry = None
        self.current_entry_path = None
        self.entries = []
        self.unsaved_changes = False
        self.left_panel_visible = True
        
        # Initialize settings manager first
        self.settings_manager = SettingsManager(self)
        
        # Setup settings and create key - this creates journal_dir and fernet
        self.settings_manager.setup_settings()
        
        # Check password before proceeding
        if not self.authenticate_user():
            return
        
        self.settings_manager.load_or_create_key()
        
        # Now initialize other managers that depend on journal_dir and fernet
        self.ui_components = UIComponents(self)
        self.entry_manager = EntryManager(self)
        self.notebook_manager = NotebookManager(self)
        self.security_manager = SecurityManager(self)
        
        # Setup UI
        self.initUI()
        self.setup_auto_save()
        self.entry_manager.load_recent_entries()
        
        # Update initial storage info
        self.update_storage_display()
    
    def authenticate_user(self):
        """Authenticate user with password. Delete everything after 3 failed attempts."""
        # Check if password file exists
        import os
        password_file = os.path.join(self.settings_manager.parent.journal_dir, "auth.enc")
        
        if os.path.exists(password_file):
            # Password exists, verify it
            return self.verify_existing_password()
        else:
            # First time setup, create password
            return self.create_new_password()
    
    def create_new_password(self):
        """Create a new password for first-time setup"""
        dialog = PasswordDialog(self, mode="create")
        if dialog.exec_() == QDialog.Accepted:
            password = dialog.get_password()
            if self.save_password_hash(password):
                QMessageBox.information(self, "Password Set", "Your password has been set successfully!")
                return True
            else:
                QMessageBox.critical(self, "Error", "Failed to save password. Please try again.")
                return False
        return False
    
    def verify_existing_password(self):
        """Verify existing password with 3 attempts limit"""
        attempts = 0
        max_attempts = 3
        
        while attempts < max_attempts:
            dialog = PasswordDialog(self, mode="verify", attempts=attempts+1)
            if dialog.exec_() != QDialog.Accepted:
                return False
            
            password = dialog.get_password()
            if self.check_password_hash(password):
                return True
            
            attempts += 1
            if attempts < max_attempts:
                QMessageBox.warning(self, "Incorrect Password", 
                                  f"Incorrect password. {max_attempts - attempts} attempts remaining.")
            else:
                # Maximum attempts reached - delete everything
                self.delete_all_data()
                QMessageBox.critical(self, "Access Denied", 
                                   "Maximum password attempts exceeded. Application will close.")
                return False
        
        return False
    
    def save_password_hash(self, password):
        """Save password hash securely"""
        try:
            import hashlib
            import os
            
            # Create a salt and hash the password
            salt = os.urandom(32)
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            
            # Save salt + hash to file
            password_file = os.path.join(self.settings_manager.parent.journal_dir, "auth.enc")
            with open(password_file, 'wb') as f:
                f.write(salt + password_hash)
            
            return True
        except Exception as e:
            print(f"Error saving password: {e}")
            return False
    
    def check_password_hash(self, password):
        """Check password against stored hash"""
        try:
            import hashlib
            import os
            
            password_file = os.path.join(self.settings_manager.parent.journal_dir, "auth.enc")
            if not os.path.exists(password_file):
                return False
            
            with open(password_file, 'rb') as f:
                stored_data = f.read()
            
            # Extract salt and hash
            salt = stored_data[:32]
            stored_hash = stored_data[32:]
            
            # Hash the provided password with the stored salt
            password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            
            return password_hash == stored_hash
        except Exception as e:
            print(f"Error checking password: {e}")
            return False
    
    def delete_all_data(self):
        """Delete all journal data after failed authentication"""
        try:
            import shutil
            import os
            
            # Remove the entire journal directory
            if os.path.exists(self.settings_manager.parent.journal_dir):
                shutil.rmtree(self.settings_manager.parent.journal_dir)
            
        except Exception as e:
            print(f"Error deleting data: {e}")
        
    def initUI(self):
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter
        self.splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Left panel - Entry list and controls
        self.left_panel = self.ui_components.create_left_panel()
        self.splitter.addWidget(self.left_panel)
        
        # Right panel - Editor
        right_panel = self.ui_components.create_right_panel()
        self.splitter.addWidget(right_panel)
        
        # Set splitter proportions
        self.splitter.setSizes([400, 1000])
        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, False)
        
        # Status bar
        self.ui_components.create_status_bar()
        
        # Toolbar
        self.ui_components.create_toolbar()
        
        # Apply styles
        self.apply_styles()
        
    def setup_auto_save(self):
        if self.config["auto_save"]:
            self.auto_save_thread = AutoSaveThread()
            self.auto_save_thread.save_signal.connect(self.auto_save)
            self.auto_save_thread.start()
    
    def apply_styles(self):
        self.setStyleSheet(get_app_stylesheet())

    def toggle_left_panel(self):
        if self.left_panel_visible:
            self.left_panel.hide()
            self.toggle_btn.setText("▶")
            self.left_panel_visible = False
        else:
            self.left_panel.show()
            self.toggle_btn.setText("◀")
            self.left_panel_visible = True
    
    def update_storage_display(self):
        """Update the storage information display"""
        try:
            stats = self.entry_manager.get_storage_stats()
            self.ui_components.update_storage_info(stats)
        except Exception as e:
            print(f"Error updating storage display: {e}")
    
    # Delegate methods to managers
    def create_notebook(self):
        self.notebook_manager.create_notebook()
        self.update_storage_display()
    
    def load_notebooks(self):
        self.notebook_manager.load_notebooks()
    
    def select_notebook(self, item):
        self.notebook_manager.select_notebook(item)
        self.update_storage_display()

    def new_entry(self):
        self.entry_manager.new_entry()
    
    def save_entry(self):
        self.entry_manager.save_entry()
        self.update_storage_display()
    
    def load_selected_entry(self, item):
        self.entry_manager.load_selected_entry(item)
    
    def delete_entry(self):
        self.entry_manager.delete_entry()
        self.update_storage_display()
    
    def show_calendar(self):
        dialog = CalendarDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.get_selected_date()
            self.status_bar.showMessage(f"Browsing entries for {selected_date}", 3000)
    
    def export_journal(self):
        self.entry_manager.export_journal()
    
    def insert_image(self):
        """Insert an image into the current entry"""
        self.entry_manager.insert_image()
    
    def show_storage_stats(self):
        """Show detailed storage statistics"""
        try:
            stats = self.entry_manager.get_storage_stats()
            
            # Get notebook-specific stats
            notebook_stats = []
            notebooks = ["Default"]
            
            # Get all notebooks
            try:
                virtual_folders = self.entry_manager.secure_storage.list_virtual_folders()
                notebook_folders = [folder.replace("notebooks/", "") for folder in virtual_folders if folder.startswith("notebooks/")]
                notebooks.extend(sorted(notebook_folders))
            except Exception:
                pass
            
            for notebook in notebooks:
                nb_stats = self.notebook_manager.get_notebook_stats(notebook)
                notebook_stats.append(f"{notebook}: {nb_stats['total_entries']} entries ({nb_stats['total_size_mb']} MB)")
            
            message = f"""Storage Statistics:
            
Total Files: {stats['virtual_files']}
Physical Files: {stats['physical_files']}
Total Size: {stats['total_size_mb']} MB

Notebook Breakdown:
{chr(10).join(notebook_stats)}

Note: All files and folder names are encrypted and secure."""
            
            QMessageBox.information(self, "Storage Statistics", message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to get storage statistics: {str(e)}")
    
    def cleanup_storage(self):
        """Clean up orphaned files"""
        try:
            self.entry_manager.cleanup_storage()
            self.update_storage_display()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to cleanup storage: {str(e)}")
    
    def on_text_changed(self):
        self.unsaved_changes = True
        self.update_status()
    
    def on_title_changed(self):
        self.unsaved_changes = True
        self.update_status()
    
    def update_status(self):
        """Update word count, character count, and save status with Evernote styling"""
        text = self.editor.toPlainText()
        word_count = len(text.split()) if text.strip() else 0
        char_count = len(text)
        
        # Format counts in a more Evernote-like way
        if word_count == 0:
            word_text = "No words"
        elif word_count == 1:
            word_text = "1 word"
        else:
            word_text = f"{word_count:,} words"
        
        if char_count == 0:
            char_text = "No characters"
        elif char_count == 1:
            char_text = "1 character"
        else:
            char_text = f"{char_count:,} characters"
        
        self.word_count_label.setText(word_text)
        self.char_count_label.setText(char_text)
        
        # Update save status with appropriate styling
        if self.unsaved_changes:
            self.last_saved_label.setText("Unsaved changes")
            self.last_saved_label.setProperty("saved", "false")
            # Apply red color for unsaved
            self.last_saved_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
        else:
            if hasattr(self, 'last_save_time'):
                self.last_saved_label.setText(f"Saved")
            else:
                self.last_saved_label.setText("No changes")
            
            self.last_saved_label.setProperty("saved", "true")
            # Apply green color for saved
            self.last_saved_label.setStyleSheet("color: #2dbe60; font-weight: bold;")
        
        # Force style refresh
        self.last_saved_label.style().unpolish(self.last_saved_label)
        self.last_saved_label.style().polish(self.last_saved_label)
    
    def auto_save(self):
        if self.unsaved_changes and self.entry_title.text().strip() and self.editor.toPlainText().strip():
            self.entry_manager.save_entry()
            self.update_storage_display()
    
    def increase_font_size(self):
        self.settings_manager.increase_font_size()
    
    def decrease_font_size(self):
        self.settings_manager.decrease_font_size()
    
    def toggle_word_wrap(self, checked):
        self.settings_manager.toggle_word_wrap(checked)
    
    def lock_and_exit(self):
        self.security_manager.lock_and_exit()
    
    def closeEvent(self, event):
        self.security_manager.handle_close_event(event)

    # Formatting methods for the rich text toolbar
    def change_font_family(self, font_name):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontFamily(font_name)
            cursor.mergeCharFormat(format)
        else:
            font = self.editor.currentFont()
            font.setFamily(font_name)
            self.editor.setCurrentFont(font)
    
    def change_font_size(self, size):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            format = QTextCharFormat()
            format.setFontPointSize(size)
            cursor.mergeCharFormat(format)
        else:
            font = self.editor.currentFont()
            font.setPointSize(size)
            self.editor.setCurrentFont(font)
    
    def toggle_bold(self):
        cursor = self.editor.textCursor()
        format = QTextCharFormat()
        
        if self.bold_btn.isChecked():
            format.setFontWeight(QFont.Bold)
        else:
            format.setFontWeight(QFont.Normal)
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.editor.mergeCurrentCharFormat(format)
    
    def toggle_italic(self):
        cursor = self.editor.textCursor()
        format = QTextCharFormat()
        format.setFontItalic(self.italic_btn.isChecked())
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.editor.mergeCurrentCharFormat(format)
    
    def toggle_underline(self):
        cursor = self.editor.textCursor()
        format = QTextCharFormat()
        format.setFontUnderline(self.underline_btn.isChecked())
        
        if cursor.hasSelection():
            cursor.mergeCharFormat(format)
        else:
            self.editor.mergeCurrentCharFormat(format)
    
    def insert_bullet_list(self):
        cursor = self.editor.textCursor()
        cursor.insertText("• ")
    
    def insert_numbered_list(self):
        cursor = self.editor.textCursor()
        cursor.insertText("1. ")
    
    def change_text_color(self):
        color = QColorDialog.getColor(QColor(255, 255, 255), self)
        if color.isValid():
            cursor = self.editor.textCursor()
            format = QTextCharFormat()
            format.setForeground(color)
            
            if cursor.hasSelection():
                cursor.mergeCharFormat(format)
            else:
                self.editor.mergeCurrentCharFormat(format)
    
    def change_background_color(self):
        color = QColorDialog.getColor(QColor(0, 0, 0), self)
        if color.isValid():
            cursor = self.editor.textCursor()
            format = QTextCharFormat()
            format.setBackground(color)
            
            if cursor.hasSelection():
                cursor.mergeCharFormat(format)
            else:
                self.editor.mergeCurrentCharFormat(format)