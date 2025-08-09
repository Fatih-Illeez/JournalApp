from datetime import datetime
from PyQt5.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QSplitter, QDialog, QColorDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QTextCursor

from auto_save_thread import AutoSaveThread
from ui_components import UIComponents
from entry_manager import EntryManager
from notebook_manager import NotebookManager
from settings_manager import SettingsManager
from security_manager import SecurityManager
from calendar_dialog import CalendarDialog
from styles import get_app_stylesheet


class EncryptedJournal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_entry = None
        self.current_entry_path = None
        self.entries = []
        self.unsaved_changes = False
        self.left_panel_visible = True
        
        # Initialize managers
        self.settings_manager = SettingsManager(self)
        self.ui_components = UIComponents(self)
        self.entry_manager = EntryManager(self)
        self.notebook_manager = NotebookManager(self)
        self.security_manager = SecurityManager(self)
        
        # Setup
        self.settings_manager.setup_settings()
        self.settings_manager.load_or_create_key()
        self.initUI()
        self.setup_auto_save()
        self.entry_manager.load_recent_entries()
        
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
    
    # Delegate methods to managers
    def create_notebook(self):
        self.notebook_manager.create_notebook()
    
    def load_notebooks(self):
        self.notebook_manager.load_notebooks()
    
    def select_notebook(self, item):
        self.notebook_manager.select_notebook(item)

    def new_entry(self):
        self.entry_manager.new_entry()
    
    def save_entry(self):
        self.entry_manager.save_entry()
    
    def load_selected_entry(self, item):
        self.entry_manager.load_selected_entry(item)
    
    def delete_entry(self):
        self.entry_manager.delete_entry()
    
    def show_calendar(self):
        dialog = CalendarDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.get_selected_date()
            self.status_bar.showMessage(f"Browsing entries for {selected_date}", 3000)
    
    def export_journal(self):
        self.entry_manager.export_journal()
    
    def on_text_changed(self):
        self.unsaved_changes = True
        self.update_status()
    
    def on_title_changed(self):
        self.unsaved_changes = True
        self.update_status()
    
    def update_status(self):
        text = self.editor.toPlainText()
        word_count = len(text.split()) if text.strip() else 0
        char_count = len(text)
        
        self.word_count_label.setText(f"Words: {word_count}")
        self.char_count_label.setText(f"Characters: {char_count}")
        
        if self.unsaved_changes:
            self.last_saved_label.setText("● Unsaved")
            self.last_saved_label.setStyleSheet("color: #ff6b6b;")
        else:
            self.last_saved_label.setStyleSheet("color: #51cf66;")
    
    def auto_save(self):
        if self.unsaved_changes and self.entry_title.text().strip() and self.editor.toPlainText().strip():
            self.entry_manager.save_entry()
    
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