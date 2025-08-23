from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QMessageBox, QFrame, QGroupBox, QGridLayout
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

        self.setWindowTitle("Notebook Settings")
        self.setModal(True)
        self.setFixedSize(630, 630)

        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(25, 25, 25, 25)

        # Header with clean design
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 20, 20, 20)
        header_layout.setSpacing(8)
        header_layout.setAlignment(Qt.AlignCenter)

        # Notebook icon - larger and cleaner
        icon_label = QLabel("📔")
        icon_label.setFont(QFont("Segoe UI", 36))
        icon_label.setAlignment(Qt.AlignCenter)

        # Title
        title_label = QLabel(f"{self.notebook_name}")
        title_label.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #e0e0e0; background: transparent;")

        # Subtitle with stats
        stats_text = f"{self.notebook_stats['total_entries']} notes • {self.notebook_stats['total_size_mb']} MB"
        subtitle_label = QLabel(stats_text)
        subtitle_label.setFont(QFont("Segoe UI", 12))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #9ca3af; background: transparent;")

        header_layout.addWidget(icon_label)
        header_layout.addWidget(title_label)
        header_layout.addWidget(subtitle_label)

        layout.addWidget(header_frame)

        # Main content area with tabs-like sections
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(15)

        # Edit Name Section
        name_group = QGroupBox("Notebook Name")
        name_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        name_layout = QVBoxLayout(name_group)
        name_layout.setContentsMargins(15, 20, 15, 15)
        name_layout.setSpacing(8)

        self.name_edit = QLineEdit(self.notebook_name)
        self.name_edit.setFont(QFont("Segoe UI", 12))
        self.name_edit.setMinimumHeight(40)

        name_layout.addWidget(self.name_edit)
        content_layout.addWidget(name_group)

        # Information Section
        info_group = QGroupBox("Information")
        info_group.setFont(QFont("Segoe UI", 11, QFont.Bold))
        info_layout = QGridLayout(info_group)
        info_layout.setContentsMargins(15, 20, 15, 15)
        info_layout.setSpacing(10)

        # Create info rows
        info_items = [
            ("Total Notes:", f"{self.notebook_stats['total_entries']}"),
            ("Storage Used:", f"{self.notebook_stats['total_size_mb']} MB"),
            ("Type:", "Default Notebook" if self.notebook_name == "Default" else "Custom Notebook"),
            ("Status:", "Protected" if self.notebook_name == "Default" else "Editable")
        ]

        for i, (label_text, value_text) in enumerate(info_items):
            label = QLabel(label_text)
            label.setFont(QFont("Segoe UI", 10, QFont.Bold))
            label.setStyleSheet("color: #c7d2fe; background: transparent;")

            value = QLabel(value_text)
            value.setFont(QFont("Segoe UI", 10))
            value.setStyleSheet("color: #d1d5db; background: transparent;")

            info_layout.addWidget(label, i, 0)
            info_layout.addWidget(value, i, 1)

        content_layout.addWidget(info_group)
        layout.addWidget(content_frame, 1)

        # Action buttons - cleaner layout
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 15, 0, 0)
        buttons_layout.setSpacing(12)

        # Primary actions (left side)
        primary_layout = QHBoxLayout()
        primary_layout.setSpacing(8)

        self.save_btn = QPushButton("Save Changes")
        self.save_btn.setObjectName("primaryButton")
        self.save_btn.setMinimumHeight(42)
        self.save_btn.setMinimumWidth(120)
        self.save_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.save_btn.clicked.connect(self.save_changes)

        self.export_btn = QPushButton("Export")
        self.export_btn.setObjectName("secondaryButton")
        self.export_btn.setMinimumHeight(42)
        self.export_btn.setMinimumWidth(90)
        self.export_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.export_btn.clicked.connect(self.export_notebook)

        primary_layout.addWidget(self.save_btn)
        primary_layout.addWidget(self.export_btn)

        # Secondary actions (right side)
        secondary_layout = QHBoxLayout()
        secondary_layout.setSpacing(8)

        self.delete_btn = QPushButton("Delete")
        self.delete_btn.setObjectName("dangerButton")
        self.delete_btn.setMinimumHeight(42)
        self.delete_btn.setMinimumWidth(90)
        self.delete_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.delete_btn.clicked.connect(self.delete_notebook)
        if self.notebook_name == "Default":
            self.delete_btn.setEnabled(False)
            self.delete_btn.setToolTip("Default notebook cannot be deleted")

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("secondaryButton")
        self.cancel_btn.setMinimumHeight(42)
        self.cancel_btn.setMinimumWidth(90)
        self.cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cancel_btn.clicked.connect(self.reject)

        secondary_layout.addWidget(self.delete_btn)
        secondary_layout.addWidget(self.cancel_btn)

        buttons_layout.addLayout(primary_layout)
        buttons_layout.addStretch()
        buttons_layout.addLayout(secondary_layout)

        layout.addWidget(buttons_frame)

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
            virtual_folders = self.parent.entry_manager.secure_storage.list_virtual_folders()
            existing_notebooks = [
                folder.replace("notebooks/", "")
                for folder in virtual_folders
                if folder.startswith("notebooks/")
            ]
            if new_name in existing_notebooks:
                QMessageBox.warning(self, "Duplicate Name", f"A notebook named '{new_name}' already exists!")
                return
        except Exception:
            # If listing fails, proceed to let parent handle rename errors
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
            (
                f"Are you sure you want to delete notebook '{self.notebook_name}'?\n\n"
                f"This will permanently delete {self.notebook_stats['total_entries']} notes and cannot be undone!"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
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

            QFrame#headerFrame {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #6366f1, stop: 1 #4f46e5);
                border-radius: 12px;
                border: none;
            }

            QFrame#contentFrame {
                background-color: #252525;
                border: 1px solid #404040;
                border-radius: 8px;
                padding: 15px;
            }

            QGroupBox {
                background-color: transparent;
                border: 2px solid #404040;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
                color: #c7d2fe;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                background-color: #252525;
                color: #c7d2fe;
            }

            QLineEdit {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 2px solid #555555;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 12px;
            }

            QLineEdit:focus {
                border-color: #6366f1;
                background-color: #333333;
            }

            QPushButton#primaryButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #10b981, stop: 1 #059669);
                color: #ffffff;
                border: 2px solid #34d399;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton#primaryButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #34d399, stop: 1 #10b981);
                border: 2px solid #6ee7b7;
            }

            QPushButton#primaryButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #059669, stop: 1 #047857);
            }

            QPushButton#secondaryButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #404040, stop: 1 #2b2b2b);
                color: #e0e0e0;
                border: 2px solid #555555;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton#secondaryButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #505050, stop: 1 #3a3a3a);
                border: 2px solid #6366f1;
                color: #c7d2fe;
            }

            QPushButton#dangerButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #ef4444, stop: 1 #dc2626);
                color: #ffffff;
                border: 2px solid #f87171;
                border-radius: 8px;
                font-weight: bold;
            }

            QPushButton#dangerButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #f87171, stop: 1 #ef4444);
                border: 2px solid #fca5a5;
            }

            QPushButton#dangerButton:disabled {
                background-color: #2b2b2b;
                color: #666666;
                border: 2px solid #333333;
            }

            QLabel {
                background: transparent;
                border: none;
            }
        """)

    def get_result(self):
        return self.result_action
