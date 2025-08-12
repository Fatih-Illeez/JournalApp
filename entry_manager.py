import os
import json
import base64
import re
from datetime import datetime, timedelta
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem, QFileDialog, QInputDialog, QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QTextCursor
from journal_entry import JournalEntry
from secure_storage_manager import SecureStorageManager


class ImageResizeDialog(QDialog):
    def __init__(self, parent=None, current_size=(600, 400)):
        super().__init__(parent)
        self.setWindowTitle("Resize Image")
        self.setModal(True)
        self.resize(400, 200)
        
        # Current image dimensions
        self.original_width = current_size[0]
        self.original_height = current_size[1]
        self.aspect_ratio = self.original_width / self.original_height
        
        layout = QVBoxLayout(self)
        
        # Size info
        info_label = QLabel(f"Original size: {self.original_width} × {self.original_height} px")
        layout.addWidget(info_label)
        
        # Size presets
        presets_layout = QHBoxLayout()
        
        small_btn = QPushButton("Small (300px)")
        small_btn.clicked.connect(lambda: self.set_width(300))
        
        medium_btn = QPushButton("Medium (600px)")
        medium_btn.clicked.connect(lambda: self.set_width(600))
        
        large_btn = QPushButton("Large (900px)")
        large_btn.clicked.connect(lambda: self.set_width(900))
        
        original_btn = QPushButton("Original")
        original_btn.clicked.connect(lambda: self.set_width(self.original_width))
        
        presets_layout.addWidget(small_btn)
        presets_layout.addWidget(medium_btn)
        presets_layout.addWidget(large_btn)
        presets_layout.addWidget(original_btn)
        
        layout.addLayout(presets_layout)
        
        # Width slider
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("Width:"))
        
        self.width_slider = QSlider(Qt.Horizontal)
        self.width_slider.setRange(100, min(1200, self.original_width * 2))
        self.width_slider.setValue(600)
        self.width_slider.valueChanged.connect(self.update_size_labels)
        
        self.width_label = QLabel("600px")
        self.width_label.setMinimumWidth(80)
        
        width_layout.addWidget(self.width_slider)
        width_layout.addWidget(self.width_label)
        layout.addLayout(width_layout)
        
        # Height display
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("Height:"))
        self.height_label = QLabel("400px")
        height_layout.addWidget(self.height_label)
        height_layout.addStretch()
        layout.addLayout(height_layout)
        
        # Maintain aspect ratio
        self.maintain_aspect = QCheckBox("Maintain aspect ratio")
        self.maintain_aspect.setChecked(True)
        self.maintain_aspect.stateChanged.connect(self.update_size_labels)
        layout.addWidget(self.maintain_aspect)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        ok_btn = QPushButton("Apply")
        ok_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(ok_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
        
        self.update_size_labels()
        
        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QPushButton {
                background-color: #404040;
                color: #e0e0e0;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #505050;
                border-color: #6366f1;
            }
            QPushButton:pressed {
                background-color: #6366f1;
            }
            QSlider::groove:horizontal {
                border: 1px solid #555;
                height: 4px;
                background: #333;
                border-radius: 2px;
            }
            QSlider::handle:horizontal {
                background: #6366f1;
                border: 1px solid #6366f1;
                width: 18px;
                margin: -7px 0;
                border-radius: 9px;
            }
            QCheckBox {
                color: #e0e0e0;
            }
        """)
    
    def set_width(self, width):
        self.width_slider.setValue(width)
        self.update_size_labels()
    
    def update_size_labels(self):
        width = self.width_slider.value()
        
        if self.maintain_aspect.isChecked():
            height = int(width / self.aspect_ratio)
        else:
            height = int(width * 0.75)  # Default 4:3 ratio
        
        self.width_label.setText(f"{width}px")
        self.height_label.setText(f"{height}px")
    
    def get_size(self):
        width = self.width_slider.value()
        if self.maintain_aspect.isChecked():
            height = int(width / self.aspect_ratio)
        else:
            height = int(width * 0.75)
        return width, height


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
            now = datetime.now()  # Use a single datetime instance
            date_str = now.strftime("%Y-%m-%d")
            timestamp = now.strftime("%H%M%S")
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
                "date": date_str,
                "created_time": now.isoformat(),
                "word_count": len(self.parent.editor.toPlainText().split()),
                "has_images": self._has_images(content),
                "notebook": self.parent.current_notebook
            }
            
            # Store the encrypted entry using secure storage
            self.secure_storage.store_file(virtual_path, entry_data)
            
            self.parent.current_entry_path = virtual_path
            self.parent.unsaved_changes = False
            
            # Store the save time for status display
            self.parent.last_save_time = now
            
            # Update status with save time
            save_time_str = now.strftime("%H:%M:%S")
            self.parent.last_saved_label.setText(f"Saved at {save_time_str}")
            
            self.parent.status_bar.showMessage("Entry saved successfully!", 3000)
            self.load_recent_entries()
            self.parent.notebook_manager.load_notebooks()
            
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
                self.parent.notebook_manager.load_notebooks()
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
        """Insert an image into the current entry with size options"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.parent, 
            "Insert Image", 
            "", 
            "Image Files (*.png *.jpg *.jpeg *.gif *.bmp);;All Files (*)"
        )
        
        if file_path:
            try:
                # Load image to get dimensions
                pixmap = QPixmap(file_path)
                original_width = pixmap.width()
                original_height = pixmap.height()
                
                # Show resize dialog
                dialog = ImageResizeDialog(self.parent, (original_width, original_height))
                if dialog.exec_() != QDialog.Accepted:
                    return
                
                width, height = dialog.get_size()
                
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
                
                # Create comprehensive style string
                style = (
                    f"width: {width}px; "
                    f"height: {height}px; "
                    f"max-width: 100%; "
                    f"display: block; "
                    f"margin: 10px auto; "
                    f"border-radius: 4px; "
                    f"box-shadow: 0 2px 8px rgba(0,0,0,0.3); "
                    f"cursor: pointer; "
                    f"object-fit: contain;"
                )
                
                # Insert the image into the editor
                cursor = self.parent.editor.textCursor()
                
                # Create an HTML img tag with the embedded image and styling
                img_html = (
                    f'<p><img src="{data_url}" '
                    f'style="{style}" '
                    f'width="{width}" '
                    f'height="{height}" '
                    f'alt="Embedded Image" '
                    f'title="Click and use Ctrl+T to resize" '
                    f'></p>'
                )
                
                cursor.insertHtml(img_html)
                
                # Mark as having unsaved changes
                self.parent.unsaved_changes = True
                self.parent.update_status()
                self.parent.status_bar.showMessage(
                    f"Image inserted at {width}×{height}px! Use Ctrl+T to resize.", 3000
                )
                
            except Exception as e:
                QMessageBox.critical(self.parent, "Image Error", f"Failed to insert image: {str(e)}")
    
    def resize_selected_image(self):
        """Properly resize the currently selected image in the editor"""
        cursor = self.parent.editor.textCursor()
        
        # First, try to find if cursor is inside an image element
        selected_html = ""
        image_found = False
        
        if cursor.hasSelection():
            # User has selected text, check if it contains an image
            selected_html = cursor.selection().toHtml()
            image_found = "<img" in selected_html.lower()
        else:
            # No selection, try to find image at cursor position
            # Get the entire document HTML and cursor position
            document = self.parent.editor.document()
            cursor_position = cursor.position()
            
            # Move cursor to find nearby image tags
            original_position = cursor_position
            
            # Search backwards and forwards for image tags
            test_cursor = QTextCursor(cursor)
            
            # Try different selection strategies
            for _ in range(50):  # Look up to 50 characters in each direction
                test_cursor.setPosition(max(0, cursor_position - 25))
                test_cursor.setPosition(min(document.characterCount(), cursor_position + 25), QTextCursor.KeepAnchor)
                test_html = test_cursor.selection().toHtml()
                
                if "<img" in test_html.lower():
                    cursor = test_cursor
                    selected_html = test_html
                    image_found = True
                    break
        
        if not image_found:
            # Try to select the entire line/paragraph containing cursor
            cursor.select(QTextCursor.BlockUnderCursor)
            selected_html = cursor.selection().toHtml()
            image_found = "<img" in selected_html.lower()
        
        if not image_found:
            QMessageBox.information(
                self.parent, 
                "No Image Found", 
                "No image found at cursor position. To resize an image:\n\n"
                "1. Click inside an image or select text containing an image\n"
                "2. Use Ctrl+T or the resize button\n"
                "3. Or double-click directly on an image"
            )
            return
        
        # Extract current image dimensions from the HTML
        current_width, current_height = self._extract_image_dimensions(selected_html)
        
        # Show resize dialog with current dimensions
        dialog = ImageResizeDialog(self.parent, (current_width, current_height))
        
        if dialog.exec_() != QDialog.Accepted:
            return
        
        new_width, new_height = dialog.get_size()
        
        # Update the image in the HTML
        updated_html = self._update_image_dimensions(selected_html, new_width, new_height)
        
        if updated_html != selected_html:
            # Replace the selected HTML with updated HTML
            cursor.removeSelectedText()
            cursor.insertHtml(updated_html)
            
            # Mark as having unsaved changes
            self.parent.unsaved_changes = True
            self.parent.update_status()
            
            self.parent.status_bar.showMessage(
                f"Image resized to {new_width}×{new_height}px!", 3000
            )
        else:
            QMessageBox.warning(
                self.parent, 
                "Resize Failed", 
                "Could not resize the image. The image may not have proper formatting."
            )
    
    def _extract_image_dimensions(self, html_content):
        """Extract width and height from image HTML"""
        # Default dimensions
        default_width, default_height = 600, 400
        
        # Look for style attribute with width/height
        style_match = re.search(r'style="([^"]*)"', html_content, re.IGNORECASE)
        if style_match:
            style_content = style_match.group(1)
            
            # Extract width from style
            width_match = re.search(r'width:\s*(\d+)px', style_content, re.IGNORECASE)
            height_match = re.search(r'height:\s*(\d+)px', style_content, re.IGNORECASE)
            
            if width_match and height_match:
                return int(width_match.group(1)), int(height_match.group(1))
            elif width_match:
                width = int(width_match.group(1))
                # Estimate height based on common aspect ratio
                height = int(width * 0.67)  # 3:2 ratio
                return width, height
        
        # Look for direct width/height attributes
        width_match = re.search(r'width="(\d+)"', html_content, re.IGNORECASE)
        height_match = re.search(r'height="(\d+)"', html_content, re.IGNORECASE)
        
        if width_match and height_match:
            return int(width_match.group(1)), int(height_match.group(1))
        elif width_match:
            width = int(width_match.group(1))
            height = int(width * 0.67)
            return width, height
        
        return default_width, default_height

    def _update_image_dimensions(self, html_content, new_width, new_height):
        """Update the width and height in image HTML"""
        
        # Create the new style string
        new_style_parts = [
            f"width: {new_width}px",
            f"height: {new_height}px",
            "max-width: 100%",
            "display: block",
            "margin: 10px auto",
            "border-radius: 4px",
            "box-shadow: 0 2px 8px rgba(0,0,0,0.3)",
            "cursor: pointer"
        ]
        new_style = "; ".join(new_style_parts) + ";"
        
        # Try to update existing style attribute
        if 'style="' in html_content:
            # Replace the existing style attribute
            updated_html = re.sub(
                r'style="[^"]*"', 
                f'style="{new_style}"', 
                html_content, 
                flags=re.IGNORECASE
            )
        else:
            # Add style attribute to img tag
            updated_html = re.sub(
                r'(<img[^>]*?)(/?>)', 
                rf'\1 style="{new_style}"\2', 
                html_content, 
                flags=re.IGNORECASE
            )
        
        # Also update any direct width/height attributes
        updated_html = re.sub(r'width="[^"]*"', f'width="{new_width}"', updated_html, flags=re.IGNORECASE)
        updated_html = re.sub(r'height="[^"]*"', f'height="{new_height}"', updated_html, flags=re.IGNORECASE)
        
        return updated_html
    
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