from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QLineEdit, QMessageBox, QFrame, QTextEdit
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class NotebookContextDialog(QDialog):
    def __init__(self, parent, notebook_name, notebook_stats):
        super().__init__(parent)
        self.notebook_name = notebook_name
        self.notebook_stats = notebook_stats
        self.parent = parent
        self.result_action = None
        
        self.setWindowTitle(f"Manage Notebook: {notebook_name}")
        self.setModal(True)
        self.setFixedSize(450, 350)
        
        self.init_ui()
        self.apply_dark_theme()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Header with notebook icon and title
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Notebook icon
        icon_label = QLabel("📔")
        icon_label.setFont(QFont("Segoe UI", 24))
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setFixedSize(50, 50)
        
        # Title section
        title_section = QFrame()
        title_layout = QVBoxLayout(title_section)
        title_layout.setContentsMargins(15, 0, 0, 0)
        title_layout.setSpacing(5)
        
        notebook_label = QLabel(f"Notebook: {self.notebook_name}")
        notebook_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        notebook_label.setStyleSheet("color: #e0e0e0;")
        
        # Stats info
        stats_text = f"{self.notebook_stats['total_entries']} notes • {self.notebook_stats['total_size_mb']} MB"
        stats_label = QLabel(stats_text)
        stats_label.setFont(QFont("Segoe UI", 11))
        stats_label.setStyleSheet("color: #9ca3af;")
        
        title_layout.addWidget(notebook_label)
        title_layout.addWidget(stats_label)
        
        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_section, 1)
        
        layout.addWidget(header_frame)
        
        # Edit name section
        edit_section = QFrame()
        edit_section.setStyleSheet("""
            QFrame {
                background-color: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        edit_layout = QVBoxLayout(edit_section)
        edit_layout.setSpacing(10)
        
        edit_label = QLabel("Edit Notebook Name")
        edit_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        edit_label.setStyleSheet("color: #c7d2fe; background: transparent; border: none; padding: 0;")
        
        self.name_edit = QLineEdit(self.notebook_name)
        self.name_edit.setFont(QFont("Segoe UI", 11))
        self.name_edit.setMinimumHeight(35)
        self.name_edit.setStyleSheet("""
            QLineEdit {
                background-color: #1e1e1e;
                color: #e0e0e0;
                border: 2px solid #555555;
                border-radius: 6px;
                padding: 8px 12px;
            }
            QLineEdit:focus {
                border-color: #6366f1;
            }
        """)
        
        edit_layout.addWidget(edit_label)
        edit_layout.addWidget(self.name_edit)
        
        layout.addWidget(edit_section)
        
        # Notebook info section
        info_section = QFrame()
        info_section.setStyleSheet("""
            QFrame {
                background-color: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout(info_section)
        info_layout.setSpacing(8)
        
        info_label = QLabel("Notebook Information")
        info_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        info_label.setStyleSheet("color: #c7d2fe; background: transparent; border: none; padding: 0;")
        
        # Detailed stats
        created_info = QLabel(f"• Total Notes: {self.notebook_stats['total_entries']}")
        created_info.setStyleSheet("color: #d1d5db; background: transparent; border: none; padding: 0;")
        
        size_info = QLabel(f"• Storage Used: {self.notebook_stats['total_size_mb']} MB")
        size_info.setStyleSheet("color: #d1d5db; background: transparent; border: none; padding: 0;")
        
        type_info = QLabel(f"• Type: {'Default Notebook' if self.notebook_name == 'Default' else 'Custom Notebook'}")
        type_info.setStyleSheet("color: #d1d5db; background: transparent; border: none; padding: 0;")
        
        info_layout.addWidget(info_label)
        info_layout.addWidget(created_info)
        info_layout.addWidget(size_info)
        info_layout.addWidget(type_info)
        
        layout.addWidget(info_section)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        # Save changes button
        self.save_btn = QPushButton("💾 Save Changes")
        self.save_btn.setMinimumHeight(40)
        self.save_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.save_btn.clicked.connect(self.save_changes)
        
        # Export button
        self.export_btn = QPushButton("📤 Export")
        self.export_btn.setMinimumHeight(40)
        self.export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.export_btn.clicked.connect(self.export_notebook)
        
        # Delete button (disabled for Default notebook)
        self.delete_btn = QPushButton("🗑️ Delete")
        self.delete_btn.setMinimumHeight(40)
        self.delete_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.delete_btn.clicked.connect(self.delete_notebook)
        if self.notebook_name == "Default":
            self.delete_btn.setEnabled(False)
            self.delete_btn.setToolTip("Default notebook cannot be deleted")
        
        # Cancel button
        self.cancel_btn = QPushButton("❌ Cancel")
        self.cancel_btn.setMinimumHeight(40)
        self.cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.export_btn)
        buttons_layout.addWidget(self.delete_btn)
        buttons_layout.addWidget(self.cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def save_changes(self):
        new_name = self.name_edit.text().strip()
        
        if not new_name:
            QMessageBox.warning(self, "Invalid Name", "Notebook name cannot be empty!")
            return
        
        if new_name == self.notebook_name:
            # No changes made
            self.reject()
            return
        
        if new_name == "Default":
            QMessageBox.warning(self, "Invalid Name", "Cannot use 'Default' as a notebook name!")
            return
        
        # Check if name already exists
        try:
            existing_notebooks = []
            virtual_folders = self.parent.entry_manager.secure_storage.list_virtual_folders()
            existing_notebooks = [folder.replace("notebooks/", "") for folder in virtual_folders if folder.startswith("notebooks/")]
            
            if new_name in existing_notebooks:
                QMessageBox.warning(self, "Duplicate Name", f"A notebook named '{new_name}' already exists!")
                return
        except Exception:
            pass
        
        self.result_action = ("rename", new_name)
        self.accept()
    
    def export_notebook(self):
        self.result_action = ("export", None)
        self.accept()
    
    def delete_notebook(self):
        if self.notebook_name == "Default":
            return
        
        reply = QMessageBox.question(
            self, 
            "Confirm Deletion", 
            f"Are you sure you want to delete notebook '{self.notebook_name}'?\n\n"
            f"This will permanently delete {self.notebook_stats['total_entries']} notes and cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.result_action = ("delete", None)
            self.accept()
    
    def apply_dark_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #404040, stop: 1 #2b2b2b);
                color: #e0e0e0;
                border: 2px solid #555555;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #505050, stop: 1 #3a3a3a);
                border: 2px solid #6366f1;
                color: #c7d2fe;
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #6366f1, stop: 1 #4f46e5);
                color: #ffffff;
                border: 2px solid #4f46e5;
            }
            
            QPushButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
                border: 2px solid #333333;
            }
            
            QPushButton[text*="Save"] {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #10b981, stop: 1 #059669);
                border: 2px solid #34d399;
            }
            
            QPushButton[text*="Save"]:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #34d399, stop: 1 #10b981);
                border: 2px solid #6ee7b7;
            }
            
            QPushButton[text*="Delete"] {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #ef4444, stop: 1 #dc2626);
                border: 2px solid #f87171;
            }
            
            QPushButton[text*="Delete"]:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #f87171, stop: 1 #ef4444);
                border: 2px solid #fca5a5;
            }
            
            QLabel {
                background: transparent;
                border: none;
            }
        """)
    
    def get_result(self):
        return self.result_action