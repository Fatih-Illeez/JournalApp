import os
import json
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from journal_entry import JournalEntry


class EntryManager:
    def __init__(self, parent):
        self.parent = parent

    def new_entry(self):
        if self.parent.unsaved_changes:
            reply = QMessageBox.question(self.parent, "Unsaved Changes", 
                                       "You have unsaved changes. Save before creating new entry?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_entry()
            elif reply == QMessageBox.Cancel:
                return
        
        self.parent.current_entry = None
        self.parent.current_entry_path = None
        self.parent.entry_title.clear()
        self.parent.editor.clear()
        self.parent.date_label.setText(datetime.now().strftime("%B %d, %Y"))
        self.parent.unsaved_changes = False
        self.parent.update_status()
        self.parent.entry_title.setFocus()
    
    def save_entry(self):
        title = self.parent.entry_title.text().strip()
        content = self.parent.editor.toPlainText()
        
        if not title:
            QMessageBox.warning(self.parent, "Missing Title", "Please enter a title for your entry.")
            return
        
        if not content.strip():
            QMessageBox.warning(self.parent, "Empty Entry", "Please write some content before saving.")
            return
        
        try:
            # Check if we're updating an existing entry
            if self.parent.current_entry_path and os.path.exists(self.parent.current_entry_path):
                file_path = self.parent.current_entry_path
            else:
                # Create new file
                if self.parent.current_notebook == "Default":
                    base_path = self.parent.journal_dir
                else:
                    base_path = os.path.join(self.parent.notebooks_dir, self.parent.current_notebook)
                
                # Create date folder
                date_str = datetime.now().strftime("%Y-%m-%d")
                folder_path = os.path.join(base_path, date_str)
                os.makedirs(folder_path, exist_ok=True)
                
                # Generate filename
                safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
                safe_title = safe_title.replace(' ', '_')[:50]
                timestamp = datetime.now().strftime("%H%M%S")
                filename = f"{safe_title}_{timestamp}.enc"
                
                file_path = os.path.join(folder_path, filename)
                self.parent.current_entry_path = file_path
            
            
            # Create entry data
            entry_data = {
                "title": title,
                "content": content,
                "date": datetime.now().strftime("%Y-%m-%d"),
                "created_time": datetime.now().isoformat(),
                "word_count": len(content.split())
            }
            
            # Encrypt and save
            json_data = json.dumps(entry_data).encode()
            encrypted = self.parent.fernet.encrypt(json_data)
            
            with open(file_path, "wb") as f:
                f.write(encrypted)
            
            self.parent.unsaved_changes = False
            self.parent.last_saved_label.setText(f"Saved at {datetime.now().strftime('%H:%M:%S')}")
            self.parent.status_bar.showMessage("Entry saved successfully!", 3000)
            self.load_recent_entries()
            
        except Exception as e:
            QMessageBox.critical(self.parent, "Save Error", f"Failed to save entry: {str(e)}")
    
    def load_recent_entries(self):
        self.parent.entry_list.clear()
        self.parent.entries = []
        
        try:
            # Determine base path based on current notebook
            if self.parent.current_notebook == "Default":
                base_path = self.parent.journal_dir
            else:
                base_path = os.path.join(self.parent.notebooks_dir, self.parent.current_notebook)
            
            # Get recent folders (last 30 days)
            for i in range(30):
                date = datetime.now() - timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                folder_path = os.path.join(base_path, date_str)
                
                if os.path.exists(folder_path):
                    for filename in os.listdir(folder_path):
                        if filename.endswith('.enc'):
                            file_path = os.path.join(folder_path, filename)
                            try:
                                with open(file_path, "rb") as f:
                                    encrypted = f.read()
                                decrypted = self.parent.fernet.decrypt(encrypted).decode()
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
                                
                                self.parent.entries.append(entry)
                                
                                # Add to list widget
                                item = QListWidgetItem()
                                item.setText(f"{entry.title}\n{entry.date} • {entry.word_count} words")
                                item.setData(Qt.UserRole, len(self.parent.entries) - 1)
                                self.parent.entry_list.addItem(item)
                                
                            except Exception as e:
                                print(f"Error loading entry {filename}: {e}")
                                continue
        except Exception as e:
            print(f"Error loading entries: {e}")
    
    def load_selected_entry(self, item):
        if self.parent.unsaved_changes:
            reply = QMessageBox.question(self.parent, "Unsaved Changes", 
                                       "You have unsaved changes. Save before switching entries?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.save_entry()
            elif reply == QMessageBox.Cancel:
                return
        
        index = item.data(Qt.UserRole)
        if 0 <= index < len(self.parent.entries):
            entry = self.parent.entries[index]
            self.parent.current_entry = entry
            self.parent.current_entry_path = entry.file_path
            self.parent.entry_title.setText(entry.title)
            self.parent.editor.setPlainText(entry.content)
            self.parent.date_label.setText(datetime.strptime(entry.date, "%Y-%m-%d").strftime("%B %d, %Y"))
            self.parent.unsaved_changes = False
            self.parent.update_status()
    
    def delete_entry(self):
        if not self.parent.current_entry_path or not os.path.exists(self.parent.current_entry_path):
            QMessageBox.information(self.parent, "No Entry", "No entry selected to delete.")
            return
        
        reply = QMessageBox.question(self.parent, "Delete Entry", 
                                   f"Are you sure you want to delete this entry?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                os.remove(self.parent.current_entry_path)
                self.new_entry()
                self.load_recent_entries()
                self.parent.status_bar.showMessage("Entry deleted successfully!", 3000)
            except Exception as e:
                QMessageBox.critical(self.parent, "Delete Error", f"Failed to delete entry: {str(e)}")
    
    def export_journal(self):
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Export Journal", 
                                                  f"journal_export_{datetime.now().strftime('%Y%m%d')}.txt",
                                                  "Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("=== JOURNAL EXPORT ===\n\n")
                    for entry in sorted(self.parent.entries, key=lambda x: x.date):
                        f.write(f"Title: {entry.title}\n")
                        f.write(f"Date: {entry.date}\n")
                        f.write(f"Words: {entry.word_count}\n")
                        f.write("-" * 50 + "\n")
                        f.write(entry.content)
                        f.write("\n\n" + "=" * 50 + "\n\n")
                
                QMessageBox.information(self.parent, "Export Complete", 
                                      f"Journal exported successfully to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self.parent, "Export Error", f"Failed to export journal: {str(e)}")