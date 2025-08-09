import os
from PyQt5.QtWidgets import QInputDialog, QMessageBox, QListWidgetItem


class NotebookManager:
    def __init__(self, parent):
        self.parent = parent

    def create_notebook(self):
        name, ok = QInputDialog.getText(self.parent, "New Notebook", "Enter notebook name:")
        if ok and name.strip():
            notebook_path = os.path.join(self.parent.notebooks_dir, name.strip())

            if not os.path.exists(notebook_path):
                os.makedirs(notebook_path)
                QMessageBox.information(self.parent, "Success", f"Notebook '{name}' created!")
                self.load_notebooks()
            else:
                QMessageBox.warning(self.parent, "Error", "A notebook with that name already exists.")
    
    def load_notebooks(self):
        self.parent.notebooks_list.clear()
        notebooks = ["Default"]  # Always have a default notebook
        
        if os.path.exists(self.parent.notebooks_dir):
            for item in os.listdir(self.parent.notebooks_dir):
                if os.path.isdir(os.path.join(self.parent.notebooks_dir, item)):
                    notebooks.append(item)
        
        for notebook in sorted(notebooks):
            item = QListWidgetItem(notebook)
            self.parent.notebooks_list.addItem(item)
        
        # Select current notebook
        for i in range(self.parent.notebooks_list.count()):
            if self.parent.notebooks_list.item(i).text() == self.parent.current_notebook:
                self.parent.notebooks_list.setCurrentRow(i)
                break
    
    def select_notebook(self, item):
        self.parent.current_notebook = item.text()
        self.parent.entry_manager.load_recent_entries()