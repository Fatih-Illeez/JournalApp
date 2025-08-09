import os
import sys
import json
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QTextEdit, QPushButton, QLabel, 
    QHBoxLayout, QVBoxLayout, QInputDialog, QFileDialog, QMessageBox,
    QListWidget, QListWidgetItem, QSplitter, QFrame, QStatusBar,
    QToolBar, QAction, QLineEdit, QCalendarWidget, QDialog, QDialogButtonBox,
    QTabWidget, QScrollArea, QProgressBar
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QPixmap, QTextCharFormat, QColor
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QDate


class AutoSaveThread(QThread):
    save_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        
    def run(self):
        self.running = True
        while self.running:
            self.msleep(30000)  # Auto-save every 30 seconds
            if self.running:
                self.save_signal.emit()
    
    def stop(self):
        self.running = False
        self.quit()


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555;
            }
            QCalendarWidget QTableView {
                selection-background-color: #4a9eff;
                background-color: #333;
                color: #fff;
            }
        """)
        layout.addWidget(self.calendar)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_selected_date(self):
        return self.calendar.selectedDate().toString("yyyy-MM-dd")


class JournalEntry:
    def __init__(self, title, content, date, file_path=None):
        self.title = title
        self.content = content
        self.date = date
        self.file_path = file_path
        self.word_count = len(content.split()) if content else 0
        self.created_time = datetime.now().strftime("%H:%M")


class EncryptedJournal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_entry = None
        self.entries = []
        self.unsaved_changes = False
        self.setup_settings()
        self.load_or_create_key()
        self.initUI()
        self.setup_auto_save()
        self.load_recent_entries()
        
    def setup_settings(self):
        self.setWindowTitle("SecureJournal Pro")
        self.setGeometry(100, 100, 1400, 900)
        self.journal_dir = os.path.expanduser("~/.encrypted_journal_pro")
        os.makedirs(self.journal_dir, exist_ok=True)
        self.key_path = os.path.join(self.journal_dir, "master.key")
        self.config_path = os.path.join(self.journal_dir, "config.json")
        self.load_config()
        
    def load_config(self):
        self.config = {
            "theme": "dark",
            "font_size": 12,
            "auto_save": True,
            "word_wrap": True
        }
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.config.update(json.load(f))
            except:
                pass
    
    def save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f)
    
    def load_or_create_key(self):
        if os.path.exists(self.key_path):
            with open(self.key_path, "rb") as f:
                self.key = f.read()
        else:
            self.key = Fernet.generate_key()
            with open(self.key_path, "wb") as f:
                f.write(self.key)
        self.fernet = Fernet(self.key)

    def initUI(self):
        # Central widget with splitter
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Entry list and controls
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Editor
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 1000])
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        
        # Status bar
        self.create_status_bar()
        
        # Toolbar
        self.create_toolbar()
        
        # Apply styles
        self.apply_styles()
        
    def create_left_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(500)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📔 SecureJournal Pro")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Quick actions
        actions_frame = QFrame()
        actions_layout = QVBoxLayout(actions_frame)
        actions_layout.setSpacing(10)
        
        self.new_entry_btn = QPushButton("✏️ New Entry")
        self.new_entry_btn.setMinimumHeight(45)
        self.new_entry_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        self.calendar_btn = QPushButton("📅 Browse by Date")
        self.calendar_btn.setMinimumHeight(35)
        
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("🔍 Search entries...")
        self.search_box.setMinimumHeight(35)
        
        actions_layout.addWidget(self.new_entry_btn)
        actions_layout.addWidget(self.calendar_btn)
        actions_layout.addWidget(self.search_box)
        layout.addWidget(actions_frame)
        
        # Entry list
        list_label = QLabel("Recent Entries")
        list_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        layout.addWidget(list_label)
        
        self.entry_list = QListWidget()
        self.entry_list.setMinimumHeight(300)
        layout.addWidget(self.entry_list)
        
        # Bottom buttons
        bottom_frame = QFrame()
        bottom_layout = QVBoxLayout(bottom_frame)
        bottom_layout.setSpacing(8)
        
        self.save_btn = QPushButton("💾 Save Entry")
        self.save_btn.setMinimumHeight(35)
        
        self.delete_btn = QPushButton("🗑️ Delete Entry")
        self.delete_btn.setMinimumHeight(35)
        
        self.export_btn = QPushButton("📤 Export Journal")
        self.export_btn.setMinimumHeight(35)
        
        self.lock_btn = QPushButton("🔒 Lock & Exit")
        self.lock_btn.setMinimumHeight(40)
        self.lock_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        bottom_layout.addWidget(self.save_btn)
        bottom_layout.addWidget(self.delete_btn)
        bottom_layout.addWidget(self.export_btn)
        bottom_layout.addWidget(self.lock_btn)
        layout.addWidget(bottom_frame)
        
        # Connect events
        self.new_entry_btn.clicked.connect(self.new_entry)
        self.calendar_btn.clicked.connect(self.show_calendar)
        self.search_box.textChanged.connect(self.filter_entries)
        self.entry_list.itemClicked.connect(self.load_selected_entry)
        self.save_btn.clicked.connect(self.save_entry)
        self.delete_btn.clicked.connect(self.delete_entry)
        self.export_btn.clicked.connect(self.export_journal)
        self.lock_btn.clicked.connect(self.lock_and_exit)
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Entry header
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        self.entry_title = QLineEdit()
        self.entry_title.setPlaceholderText("Enter your entry title...")
        self.entry_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.entry_title.setMinimumHeight(40)
        
        self.date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
        self.date_label.setFont(QFont("Segoe UI", 12))
        self.date_label.setMinimumWidth(150)
        self.date_label.setAlignment(Qt.AlignRight)
        
        header_layout.addWidget(self.entry_title, 1)
        header_layout.addWidget(self.date_label)
        layout.addWidget(header_frame)
        
        # Editor
        self.editor = QTextEdit()
        self.editor.setFont(QFont("Segoe UI", self.config["font_size"]))
        self.editor.setPlaceholderText("Start writing your thoughts here...")
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth if self.config["word_wrap"] else QTextEdit.NoWrap)
        layout.addWidget(self.editor)
        
        # Bottom info bar
        info_frame = QFrame()
        info_layout = QHBoxLayout(info_frame)
        
        self.word_count_label = QLabel("Words: 0")
        self.char_count_label = QLabel("Characters: 0")
        self.last_saved_label = QLabel("Unsaved")
        
        info_layout.addWidget(self.word_count_label)
        info_layout.addWidget(self.char_count_label)
        info_layout.addStretch()
        info_layout.addWidget(self.last_saved_label)
        
        layout.addWidget(info_frame)
        
        # Connect editor events
        self.editor.textChanged.connect(self.on_text_changed)
        self.entry_title.textChanged.connect(self.on_title_changed)
        
        return panel
    
    def create_status_bar(self):
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_bar.showMessage("Ready to write...")
        
        # Add progress bar for operations
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setMaximumWidth(200)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # Font size actions
        decrease_font = QAction("A-", self)
        decrease_font.triggered.connect(self.decrease_font_size)
        toolbar.addAction(decrease_font)
        
        increase_font = QAction("A+", self)
        increase_font.triggered.connect(self.increase_font_size)
        toolbar.addAction(increase_font)
        
        toolbar.addSeparator()
        
        # Word wrap toggle
        word_wrap = QAction("Word Wrap", self)
        word_wrap.setCheckable(True)
        word_wrap.setChecked(self.config["word_wrap"])
        word_wrap.triggered.connect(self.toggle_word_wrap)
        toolbar.addAction(word_wrap)
    
    def setup_auto_save(self):
        if self.config["auto_save"]:
            self.auto_save_thread = AutoSaveThread()
            self.auto_save_thread.save_signal.connect(self.auto_save)
            self.auto_save_thread.start()
    
    def apply_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            QFrame {
                background-color: #2d2d2d;
                border: 1px solid #3e3e3e;
                border-radius: 8px;
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
                border: none;
            }
            
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #4a9eff, stop: 1 #3d8bdb);
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #5aa3ff, stop: 1 #4d95e5);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #3d8bdb, stop: 1 #2a7bc4);
            }
            
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
            }
            
            QLineEdit:focus {
                border-color: #4a9eff;
            }
            
            QTextEdit {
                background-color: #2a2a2a;
                color: #ffffff;
                border: 2px solid #444;
                border-radius: 8px;
                padding: 12px;
                font-family: 'Segoe UI', Arial, sans-serif;
                line-height: 1.5;
            }
            
            QTextEdit:focus {
                border-color: #4a9eff;
            }
            
            QListWidget {
                background-color: #333;
                color: #ffffff;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 5px;
            }
            
            QListWidget::item {
                background-color: #404040;
                border: 1px solid #555;
                border-radius: 4px;
                margin: 2px;
                padding: 8px;
            }
            
            QListWidget::item:hover {
                background-color: #4a4a4a;
                border-color: #4a9eff;
            }
            
            QListWidget::item:selected {
                background-color: #4a9eff;
                border-color: #5aa3ff;
            }
            
            QStatusBar {
                background-color: #252525;
                color: #cccccc;
                border-top: 1px solid #3e3e3e;
            }
            
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                spacing: 3px;
                padding: 5px;
            }
            
            QProgressBar {
                border: 2px solid #555;
                border-radius: 5px;
                text-align: center;
                background-color: #333;
            }
            
            QProgressBar::chunk {
                background-color: #4a9eff;
                border-radius: 3px;
            }
        """)

    def new_entry(self):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, "Unsaved Changes", 
                                       "You have unsaved changes. Save before creating new entry?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_entry()
            elif reply == QMessageBox.Cancel:
                return
        
        self.current_entry = None
        self.entry_title.clear()
        self.editor.clear()
        self.date_label.setText(datetime.now().strftime("%B %d, %Y"))
        self.unsaved_changes = False
        self.update_status()
        self.entry_title.setFocus()
    
    def save_entry(self):
        title = self.entry_title.text().strip()
        content = self.editor.toPlainText()
        
        if not title:
            QMessageBox.warning(self, "Missing Title", "Please enter a title for your entry.")
            return
        
        if not content.strip():
            QMessageBox.warning(self, "Empty Entry", "Please write some content before saving.")
            return
        
        try:
            # Create date folder
            date_str = datetime.now().strftime("%Y-%m-%d")
            folder_path = os.path.join(self.journal_dir, date_str)
            os.makedirs(folder_path, exist_ok=True)
            
            # Create entry data
            entry_data = {
                "title": title,
                "content": content,
                "date": date_str,
                "created_time": datetime.now().isoformat(),
                "word_count": len(content.split())
            }
            
            # Encrypt and save
            json_data = json.dumps(entry_data).encode()
            encrypted = self.fernet.encrypt(json_data)
            
            # Generate filename
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{safe_title}_{timestamp}.enc"
            
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "wb") as f:
                f.write(encrypted)
            
            self.unsaved_changes = False
            self.last_saved_label.setText(f"Saved at {datetime.now().strftime('%H:%M:%S')}")
            self.status_bar.showMessage("Entry saved successfully!", 3000)
            self.load_recent_entries()
            
        except Exception as e:
            QMessageBox.critical(self, "Save Error", f"Failed to save entry: {str(e)}")
    
    def load_recent_entries(self):
        self.entry_list.clear()
        self.entries = []
        
        try:
            # Get recent folders (last 30 days)
            for i in range(30):
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                folder_path = os.path.join(self.journal_dir, date_str)
                
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        if filename.endswith('.enc'):
                            file_path = os.path.join(folder_path, filename)
                            try:
                                with open(file_path, "rb") as f:
                                    encrypted = f.read()
                                decrypted = self.fernet.decrypt(encrypted).decode()
                                entry_data = json.loads(decrypted)
                                
                                # Create entry object
                                entry = JournalEntry(
                                    entry_data.get("title", "Untitled"),
                                    entry_data.get("content", ""),
                                    entry_data.get("date", date_str),
                                    file_path
                                )
                                entry.created_time = entry_data.get("created_time", "")
                                entry.word_count = entry_data.get("word_count", 0)
                                
                                self.entries.append(entry)
                                
                                # Add to list widget
                                item = QListWidgetItem()
                                item.setText(f"{entry.title}\n{entry.date} • {entry.word_count} words")
                                item.setData(Qt.UserRole, len(self.entries) - 1)
                                self.entry_list.addItem(item)
                                
                            except Exception as e:
                                print(f"Error loading entry {filename}: {e}")
                                continue
        except Exception as e:
            print(f"Error loading entries: {e}")
    
    def load_selected_entry(self, item):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, "Unsaved Changes", 
                                       "You have unsaved changes. Save before switching entries?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_entry()
            elif reply == QMessageBox.Cancel:
                return
        
        index = item.data(Qt.UserRole)
        if 0 <= index < len(self.entries):
            entry = self.entries[index]
            self.current_entry = entry
            self.entry_title.setText(entry.title)
            self.editor.setPlainText(entry.content)
            self.date_label.setText(datetime.strptime(entry.date, "%Y-%m-%d").strftime("%B %d, %Y"))
            self.unsaved_changes = False
            self.update_status()
    
    def delete_entry(self):
        if not self.current_entry or not self.current_entry.file_path:
            QMessageBox.information(self, "No Entry", "No entry selected to delete.")
            return
        
        reply = QMessageBox.question(self, "Delete Entry", 
                                   f"Are you sure you want to delete '{self.current_entry.title}'?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(self.current_entry.file_path)
                self.new_entry()
                self.load_recent_entries()
                self.status_bar.showMessage("Entry deleted successfully!", 3000)
            except Exception as e:
                QMessageBox.critical(self, "Delete Error", f"Failed to delete entry: {str(e)}")
    
    def show_calendar(self):
        dialog = CalendarDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            selected_date = dialog.get_selected_date()
            # Filter entries by selected date
            # This is a simplified version - you could implement more sophisticated filtering
            self.status_bar.showMessage(f"Browsing entries for {selected_date}", 3000)
    
    def filter_entries(self, text):
        for i in range(self.entry_list.count()):
            item = self.entry_list.item(i)
            item.setHidden(text.lower() not in item.text().lower())
    
    def export_journal(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Journal", 
                                                  f"journal_export_{datetime.now().strftime('%Y%m%d')}.txt",
                                                  "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=== JOURNAL EXPORT ===\n\n")
                    for entry in sorted(self.entries, key=lambda x: x.date):
                        f.write(f"Title: {entry.title}\n")
                        f.write(f"Date: {entry.date}\n")
                        f.write(f"Words: {entry.word_count}\n")
                        f.write("-" * 50 + "\n")
                        f.write(entry.content)
                        f.write("\n\n" + "=" * 50 + "\n\n")
                
                QMessageBox.information(self, "Export Complete", 
                                      f"Journal exported successfully to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export journal: {str(e)}")
    
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
            self.save_entry()
    
    def increase_font_size(self):
        self.config["font_size"] = min(24, self.config["font_size"] + 1)
        self.editor.setFont(QFont("Segoe UI", self.config["font_size"]))
        self.save_config()
    
    def decrease_font_size(self):
        self.config["font_size"] = max(8, self.config["font_size"] - 1)
        self.editor.setFont(QFont("Segoe UI", self.config["font_size"]))
        self.save_config()
    
    def toggle_word_wrap(self, checked):
        self.config["word_wrap"] = checked
        self.editor.setLineWrapMode(QTextEdit.WidgetWidth if checked else QTextEdit.NoWrap)
        self.save_config()
    
    def lock_and_exit(self):
        if self.unsaved_changes:
            reply = QMessageBox.question(self, "Unsaved Changes", 
                                       "You have unsaved changes. Save before exiting?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_entry()
            elif reply == QMessageBox.Cancel:
                return
        
        # Clear sensitive data
        self.editor.clear()
        self.entry_title.clear()
        
        # Stop auto-save thread
        if hasattr(self, 'auto_save_thread'):
            self.auto_save_thread.stop()
        
        QMessageBox.information(self, "Locked", "🔒 Journal locked securely. Your thoughts are safe!")
        self.close()
    
    def closeEvent(self, event):
        self.lock_and_exit()
        event.ignore()  # Let lock_and_exit handle the closing


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("SecureJournal Pro")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("SecureApps")
    
    journal = EncryptedJournal()
    journal.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()