import os
import json
from datetime import datetime
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QListWidgetItem
from PyQt5.QtCore import Qt


class NotebookManager:
    def __init__(self, parent):
        self.parent = parent

    def create_notebook(self):
        name, ok = QInputDialog.getText(self.parent, "New Notebook", "Enter notebook name:")
        if ok and name.strip():
            notebook_name = name.strip()
            
            # Check if notebook already exists
            try:
                existing_notebooks = []
                virtual_folders = self.parent.entry_manager.secure_storage.list_virtual_folders()
                existing_notebooks = [folder.replace("notebooks/", "") for folder in virtual_folders if folder.startswith("notebooks/")]
                
                if notebook_name in existing_notebooks:
                    QMessageBox.warning(self.parent, "Duplicate Notebook", 
                                      f"A notebook named '{notebook_name}' already exists!")
                    return
                
            except Exception:
                pass  # Continue if we can't check existing notebooks
            
            # Create virtual folder in secure storage
            try:
                virtual_folder_path = f"notebooks/{notebook_name}"
                self.parent.entry_manager.secure_storage.create_virtual_folder(virtual_folder_path)
                
                QMessageBox.information(self.parent, "Success", f"Notebook '{notebook_name}' created securely!")
                self.load_notebooks()
            except Exception as e:
                QMessageBox.critical(self.parent, "Error", f"Failed to create notebook: {str(e)}")
    
    def load_notebooks(self):
        """Load notebooks with entry counts"""
        notebooks_data = []
        
        # Always have Default notebook first
        default_count = self.parent.entry_manager.get_notebook_entry_count("Default")
        notebooks_data.append({
            'name': "Default",
            'count': default_count
        })
        
        try:
            # Get all virtual folders that start with "notebooks/"
            virtual_folders = self.parent.entry_manager.secure_storage.list_virtual_folders()
            notebook_folders = []
            
            for folder in virtual_folders:
                if folder.startswith("notebooks/"):
                    # Extract just the notebook name, not the full path with dates
                    notebook_name = folder.replace("notebooks/", "")
                    # Only take the first part before any slash (to avoid date subfolders)
                    if "/" in notebook_name:
                        notebook_name = notebook_name.split("/")[0]
                    
                    # Avoid duplicates
                    if notebook_name and notebook_name not in notebook_folders:
                        notebook_folders.append(notebook_name)
            
            # Add other notebooks with their counts
            for notebook_name in sorted(notebook_folders):
                entry_count = self.parent.entry_manager.get_notebook_entry_count(notebook_name)
                notebooks_data.append({
                    'name': notebook_name,
                    'count': entry_count
                })
                
        except Exception as e:
            print(f"Error loading notebooks: {e}")
        
        # Update the UI with notebook data including counts
        self.parent.ui_components.update_notebooks_with_counts(notebooks_data)
    
    def select_notebook(self, item):
        old_notebook = self.parent.current_notebook
        # Get the actual notebook name from UserRole data
        new_notebook = item.data(Qt.UserRole)
        
        if new_notebook is None:  # Fallback to parsing text
            notebook_text = item.text()
            new_notebook = notebook_text.split('  (')[0]  # Extract name before count
            new_notebook = notebook_text.split('\n')[0]   # Extract name before subtitle
        
        # Check for unsaved changes before switching
        if self.parent.unsaved_changes:
            reply = QMessageBox.question(self.parent, "Unsaved Changes", 
                                       "You have unsaved changes. Save before switching notebooks?",
                                       QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            if reply == QMessageBox.Yes:
                self.parent.save_entry()
            elif reply == QMessageBox.Cancel:
                # Revert selection
                for i in range(self.parent.notebooks_list.count()):
                    list_item = self.parent.notebooks_list.item(i)
                    if list_item.data(Qt.UserRole) == old_notebook:
                        self.parent.notebooks_list.setCurrentRow(i)
                        break
                return
        
        # Switch to new notebook
        self.parent.current_notebook = new_notebook
        self.parent.new_entry()  # Clear current entry
        self.parent.entry_manager.load_recent_entries()
        self.parent.status_bar.showMessage(f"Switched to notebook: {new_notebook}", 2000)
        
        # Update storage info
        try:
            stats = self.parent.entry_manager.get_storage_stats()
            self.parent.ui_components.update_storage_info(stats)
        except Exception:
            pass
    
    def delete_notebook(self, notebook_name):
        """Delete a notebook and all its entries"""
        if notebook_name == "Default":
            QMessageBox.warning(self.parent, "Cannot Delete", "The Default notebook cannot be deleted.")
            return
        
        reply = QMessageBox.question(
            self.parent, 
            "Delete Notebook", 
            f"Are you sure you want to delete notebook '{notebook_name}' and ALL its entries?\n\nThis action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                # Get all files in this notebook
                virtual_path_prefix = f"notebooks/{notebook_name}/"
                files_to_delete = self.parent.entry_manager.secure_storage.list_files(virtual_path_prefix)
                
                # Delete all files
                deleted_count = 0
                for file_info in files_to_delete:
                    virtual_path = file_info["virtual_path"]
                    if self.parent.entry_manager.secure_storage.delete_file(virtual_path):
                        deleted_count += 1
                
                # Delete the folder marker
                folder_marker_path = f"notebooks/{notebook_name}/.folder_marker"
                self.parent.entry_manager.secure_storage.delete_file(folder_marker_path)
                
                # Switch to Default notebook if we deleted the current one
                if self.parent.current_notebook == notebook_name:
                    self.parent.current_notebook = "Default"
                    self.parent.new_entry()
                
                self.load_notebooks()
                self.parent.entry_manager.load_recent_entries()
                
                QMessageBox.information(
                    self.parent, 
                    "Notebook Deleted", 
                    f"Notebook '{notebook_name}' and {deleted_count} entries have been securely deleted."
                )
                
            except Exception as e:
                QMessageBox.critical(self.parent, "Delete Error", f"Failed to delete notebook: {str(e)}")
    
    def export_notebook(self, notebook_name):
        """Export a specific notebook"""
        from PyQt5.QtWidgets import QFileDialog
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.parent, 
            f"Export Notebook: {notebook_name}", 
            f"notebook_{notebook_name}_{datetime.now().strftime('%Y%m%d')}.html",
            "HTML Files (*.html);;Text Files (*.txt)"
        )
        
        if file_path:
            try:
                # Get all entries for this notebook
                if notebook_name == "Default":
                    path_prefix = "default/"
                else:
                    path_prefix = f"notebooks/{notebook_name}/"
                
                files = self.parent.entry_manager.secure_storage.list_files(path_prefix)
                entries = []
                
                for file_info in files:
                    try:
                        virtual_path = file_info["virtual_path"]
                        if not virtual_path.endswith('.enc'):
                            continue
                        
                        encrypted_data = self.parent.entry_manager.secure_storage.load_file(virtual_path)
                        if encrypted_data is None:
                            continue
                        
                        entry_data = json.loads(encrypted_data.decode())
                        entries.append(entry_data)
                        
                    except Exception as e:
                        print(f"Error loading entry for export: {e}")
                        continue
                
                # Sort entries by creation time
                entries.sort(key=lambda x: x.get("created_time", ""), reverse=True)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    if file_path.endswith('.html'):
                        # Export as HTML
                        f.write(f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Notebook Export: {notebook_name}</title>
                            <style>
                                body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
                                .entry {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                                .entry-header {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }}
                                .entry-title {{ font-size: 24px; font-weight: bold; color: #333; margin: 0; }}
                                .entry-meta {{ color: #666; font-size: 14px; margin-top: 5px; }}
                                .entry-content {{ line-height: 1.6; color: #444; }}
                                img {{ max-width: 100%; height: auto; border-radius: 4px; margin: 10px 0; }}
                            </style>
                        </head>
                        <body>
                            <h1>📔 Notebook Export: {notebook_name}</h1>
                            <p>Generated on {datetime.now().strftime("%B %d, %Y at %H:%M")}</p>
                            <p>Total entries: {len(entries)}</p>
                        """)
                        
                        for entry in entries:
                            f.write(f"""
                            <div class="entry">
                                <div class="entry-header">
                                    <h2 class="entry-title">{entry.get("title", "Untitled")}</h2>
                                    <div class="entry-meta">{entry.get("date", "")} • {entry.get("word_count", 0)} words</div>
                                </div>
                                <div class="entry-content">
                                    {entry.get("content", "")}
                                </div>
                            </div>
                            """)
                        
                        f.write("</body></html>")
                    else:
                        # Export as plain text
                        f.write(f"=== NOTEBOOK EXPORT: {notebook_name} ===\n\n")
                        f.write(f"Generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}\n")
                        f.write(f"Total entries: {len(entries)}\n\n")
                        
                        for entry in entries:
                            f.write(f"Title: {entry.get('title', 'Untitled')}\n")
                            f.write(f"Date: {entry.get('date', '')}\n")
                            f.write(f"Words: {entry.get('word_count', 0)}\n")
                            f.write("-" * 50 + "\n")
                            f.write(entry.get("plain_text", entry.get("content", "")))
                            f.write("\n\n" + "=" * 50 + "\n\n")
                
                QMessageBox.information(
                    self.parent, 
                    "Export Complete", 
                    f"Notebook '{notebook_name}' exported successfully to:\n{file_path}\n\nEntries exported: {len(entries)}"
                )
                
            except Exception as e:
                QMessageBox.critical(self.parent, "Export Error", f"Failed to export notebook: {str(e)}")
    
    def get_notebook_stats(self, notebook_name):
        """Get statistics for a specific notebook"""
        try:
            if notebook_name == "Default":
                path_prefix = "default/"
            else:
                path_prefix = f"notebooks/{notebook_name}/"
            
            files = self.parent.entry_manager.secure_storage.list_files(path_prefix)
            entry_files = [f for f in files if f["virtual_path"].endswith('.enc')]
            
            total_entries = len(entry_files)
            total_size = sum(f["size"] for f in entry_files)
            
            return {
                "total_entries": total_entries,
                "total_size_bytes": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2) if total_size > 0 else 0.0
            }
            
        except Exception as e:
            print(f"Error getting notebook stats: {e}")
            return {
                "total_entries": 0,
                "total_size_bytes": 0,
                "total_size_mb": 0.0
            }