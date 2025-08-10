import os
import json
import base64
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from journal_entry import JournalEntry
from secure_storage_manager import SecureStorageManager


class EntryManager:
    def __init__(self, parent):
        self.parent = parent
        # Initialize secure storage manager
        self.secure_storage = SecureStorageManager(
            self.parent.journal_dir, 
            self.parent.fernet
        )

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
        content = self.parent.editor.toHtml()  # Save as HTML to preserve images
        
        if not title:
            QMessageBox.warning(self.parent, "Missing Title", "Please enter a title for your entry.")
            return
        
        if not self.parent.editor.toPlainText().strip():
            QMessageBox.warning(self.parent, "Empty Entry", "Please write some content before saving.")
            return
        
        try:
            # Generate virtual file path
            date_str = datetime.now().strftime("%Y-%m-%d")
            timestamp = datetime.now().strftime("%H%M%S")
            safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_title = safe_title.replace(' ', '_')[:50]
            
            # Create virtual path based on notebook
            if self.parent.current_notebook == "Default":
                virtual_path = f"default/{date_str}/{safe_title}_{timestamp}.enc"
            else:
                virtual_path = f"notebooks/{self.parent.current_notebook}/{date_str}/{safe_title}_{timestamp}.enc"
            
            # If updating existing entry, use the same path
            if self.parent.current_entry_path:
                virtual_path = self.parent.current_entry_path
            
            # Create entry data with embedded images
            entry_data = {
                "title": title,
                "content": content,
                "plain_text": self.parent.editor.toPlainText(),  # For word count and search
                "date": datetime.now().strftime("%Y-%m-%d"),
                "created_time": datetime.now().isoformat(),
                "word_count": len(self.parent.editor.toPlainText().split()),
                "has_images": self._has_images(content),
                "notebook": self.parent.current_notebook
            }
            
            # Store the encrypted entry using secure storage
            self.secure_storage.store_file(virtual_path, entry_data)
            
            self.parent.current_entry_path = virtual_path
            self.parent.unsaved_changes = False
            self.parent.last_saved_label.setText(f"Saved at {datetime.now().strftime('%H:%M:%S')}")
            self.parent.status_bar.showMessage("Entry saved successfully!", 3000)
            self.load_recent_entries()
            
        except Exception as e:
            QMessageBox.critical(self.parent, "Save Error", f"Failed to save entry: {str(e)}")
    
    def _has_images(self, html_content):
        """Check if HTML content contains images"""
        return "<img" in html_content.lower()
    
    def get_notebook_entry_count(self, notebook_name):
        """Get the number of entries in a specific notebook"""
        try:
            if notebook_name == "Default":
                path_prefix = "default/"
            else:
                path_prefix = f"notebooks/{notebook_name}/"
            
            files = self.secure_storage.list_files(path_prefix)
            entry_files = [f for f in files if f["virtual_path"].endswith('.enc')]
            return len(entry_files)
            
        except Exception as e:
            print(f"Error counting entries for notebook {notebook_name}: {e}")
            return 0
    
    def load_recent_entries(self):
        self.parent.entry_list.clear()
        self.parent.entries = []
        
        try:
            # Determine path prefix based on current notebook
            if self.parent.current_notebook == "Default":
                path_prefix = "default/"
            else:
                path_prefix = f"notebooks/{self.parent.current_notebook}/"
            
            # Get all files for the current notebook
            files = self.secure_storage.list_files(path_prefix)
            
            # Filter for recent entries (last 30 days)
            recent_entries = []
            cutoff_date = datetime.now() - timedelta(days=30)
            
            for file_info in files:
                try:
                    virtual_path = file_info["virtual_path"]
                    if not virtual_path.endswith('.enc'):
                        continue
                    
                    # Load the entry data
                    encrypted_data = self.secure_storage.load_file(virtual_path)
                    if encrypted_data is None:
                        continue
                    
                    entry_data = json.loads(encrypted_data.decode())
                    created_time = datetime.fromisoformat(entry_data.get("created_time", datetime.now().isoformat()))
                    
                    # Check if it's within the recent period
                    if created_time >= cutoff_date:
                        entry = JournalEntry(
                            entry_data.get("title", "Untitled"),
                            entry_data.get("plain_text", entry_data.get("content", "")),  # Use plain text for display
                            entry_data.get("date", created_time.strftime("%Y-%m-%d")),
                            virtual_path
                        )
                        entry.created_time = entry_data.get("created_time", "")
                        entry.word_count = entry_data.get("word_count", 0)
                        entry.has_images = entry_data.get("has_images", False)
                        entry.html_content = entry_data.get("content", "")  # Store HTML content separately
                        
                        recent_entries.append(entry)
                        
                except Exception as e:
                    print(f"Error loading entry {file_info.get('virtual_path', 'unknown')}: {e}")
                    continue
            
            # Sort entries by created_time (newest first)
            recent_entries.sort(key=lambda x: x.created_time, reverse=True)
            self.parent.entries = recent_entries
            
            # Add sorted entries to list widget
            for i, entry in enumerate(self.parent.entries):
                item = QListWidgetItem()
                image_indicator = " 📷" if entry.has_images else ""
                item.setText(f"{entry.title}{image_indicator}\n{entry.date} • {entry.word_count} words")
                item.setData(Qt.UserRole, i)
                self.parent.entry_list.addItem(item)
                                
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
            
            # Load HTML content if available, otherwise use plain text
            if hasattr(entry, 'html_content') and entry.html_content:
                self.parent.editor.setHtml(entry.html_content)
            else:
                self.parent.editor.setPlainText(entry.content)
            
            self.parent.date_label.setText(datetime.strptime(entry.date, "%Y-%m-%d").strftime("%B %d, %Y"))
            self.parent.unsaved_changes = False
            self.parent.update_status()
    
    def delete_entry(self):
        if not self.parent.current_entry_path:
            QMessageBox.information(self.parent, "No Entry", "No entry selected to delete.")
            return
        
        reply = QMessageBox.question(self.parent, "Delete Entry", 
                                   f"Are you sure you want to delete this entry?",
                                   QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                self.secure_storage.delete_file(self.parent.current_entry_path)
                self.new_entry()
                self.load_recent_entries()
                self.parent.status_bar.showMessage("Entry deleted successfully!", 3000)
            except Exception as e:
                QMessageBox.critical(self.parent, "Delete Error", f"Failed to delete entry: {str(e)}")
    
    def export_journal(self):
        file_path, _ = QFileDialog.getSaveFileName(self.parent, "Export Journal", 
                                                  f"journal_export_{datetime.now().strftime('%Y%m%d')}.html",
                                                  "HTML Files (*.html);;Text Files (*.txt)")
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.html'):
                        # Export as HTML to preserve images
                        f.write("""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Journal Export</title>
                            <style>
                                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
                                .entry { background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
                                .entry-header { border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }
                                .entry-title { font-size: 24px; font-weight: bold; color: #333; margin: 0; }
                                .entry-meta { color: #666; font-size: 14px; margin-top: 5px; }
                                .entry-content { line-height: 1.6; color: #444; }
                                img { max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }
                            </style>
                        </head>
                        <body>
                            <h1>📔 Journal Export</h1>
                            <p>Generated on {}</p>
                        """.format(datetime.now().strftime("%B %d, %Y at %H:%M")))
                        
                        # Sort entries by date for export (newest first)
                        sorted_entries = sorted(self.parent.entries, key=lambda x: x.created_time, reverse=True)
                        for entry in sorted_entries:
                            f.write(f"""
                            <div class="entry">
                                <div class="entry-header">
                                    <h2 class="entry-title">{entry.title}</h2>
                                    <div class="entry-meta">{entry.date} • {entry.word_count} words</div>
                                </div>
                                <div class="entry-content">
                                    {getattr(entry, 'html_content', entry.content.replace('\n', '<br>'))}
                                </div>
                            </div>
                            """)
                        
                        f.write("</body></html>")
                    else:
                        # Export as plain text
                        f.write("=== JOURNAL EXPORT ===\n\n")
                        sorted_entries = sorted(self.parent.entries, key=lambda x: x.created_time, reverse=True)
                        for entry in sorted_entries:
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
    
    def insert_image(self):
        """Insert an image into the current entry"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "Insert Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)"
        )
        
        if file_path:
            try:
                # Read and encode the image
                with open(file_path, "rb") as img_file:
                    img_data = img_file.read()
                
                # Convert to base64 for embedding
                img_base64 = base64.b64encode(img_data).decode()
                
                # Determine the image type
                file_ext = os.path.splitext(file_path)[1].lower()
                if file_ext == '.jpg':
                    file_ext = '.jpeg'
                
                # Create the data URL
                data_url = f"data:image/{file_ext[1:]};base64,{img_base64}"
                
                # Insert the image into the editor
                cursor = self.parent.editor.textCursor()
                
                # Create an HTML img tag with the embedded image
                img_html = f'<img src="{data_url}" style="max-width: 600px; height: auto;" alt="Embedded Image">'
                cursor.insertHtml(img_html)
                
                # Mark as having unsaved changes
                self.parent.unsaved_changes = True
                self.parent.update_status()
                self.parent.status_bar.showMessage("Image inserted successfully!", 2000)
                
            except Exception as e:
                QMessageBox.critical(self.parent, "Image Error", f"Failed to insert image: {str(e)}")
    
    def get_storage_stats(self):
        """Get statistics about the secure storage"""
        try:
            return self.secure_storage.get_storage_stats()
        except Exception as e:
            print(f"Error getting storage stats: {e}")
            return {
                "virtual_files": 0,
                "physical_files": 0,
                "total_size_bytes": 0,
                "total_size_mb": 0.0
            }
    
    def cleanup_storage(self):
        """Clean up orphaned files in storage"""
        try:
            cleaned = self.secure_storage.cleanup_orphaned_files()
            QMessageBox.information(
                self.parent, 
                "Cleanup Complete", 
                f"Cleaned up {cleaned} orphaned files from secure storage."
            )
            return cleaned
        except Exception as e:
            QMessageBox.critical(self.parent, "Cleanup Error", f"Failed to cleanup storage: {str(e)}")
            return 0