from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class PasswordDialog(QDialog):
    def __init__(self, parent=None, mode="verify", attempts=1):
        super().__init__(parent)
        self.mode = mode  # "create" or "verify"
        self.attempts = attempts
        self.password = ""
        
        self.setWindowTitle("SecureJournal - Authentication")
        self.setModal(True)
        self.setFixedSize(450, 450)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header section with Evernote green
        header = QFrame()
        header.setObjectName("header")
        header.setFixedHeight(100)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(30, 20, 30, 20)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # App icon and title
        app_title = QLabel("🐘 SecureJournal")
        app_title.setObjectName("appTitle")
        app_title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter)
        
        # Subtitle based on mode
        if self.mode == "create":
            subtitle = QLabel("Create your master password")
            subtitle.setObjectName("subtitle")
        else:
            if self.attempts > 1:
                subtitle = QLabel(f"Incorrect password. Attempt {self.attempts} of 3")
                subtitle.setObjectName("subtitleError")
            else:
                subtitle = QLabel("Enter your master password")
                subtitle.setObjectName("subtitle")
        
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        
        header_layout.addWidget(app_title)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header)
        
        # Content section
        content = QFrame()
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(40, 30, 40, 30)
        content_layout.setSpacing(20)
        
        if self.mode == "create":
            # Password creation fields
            password_section = QFrame()
            password_layout = QVBoxLayout(password_section)
            password_layout.setSpacing(15)
            
            # Password field
            password_label = QLabel("Password")
            password_label.setObjectName("fieldLabel")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.password_input = QLineEdit()
            self.password_input.setObjectName("passwordInput")
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(40)
            self.password_input.setPlaceholderText("Enter a secure password...")
            self.password_input.setFont(QFont("Segoe UI", 12))
            
            # Confirm password field
            confirm_label = QLabel("Confirm Password")
            confirm_label.setObjectName("fieldLabel")
            confirm_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.confirm_input = QLineEdit()
            self.confirm_input.setObjectName("passwordInput")
            self.confirm_input.setEchoMode(QLineEdit.Password)
            self.confirm_input.setMinimumHeight(40)
            self.confirm_input.setPlaceholderText("Confirm your password...")
            self.confirm_input.setFont(QFont("Segoe UI", 12))
            
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_input)
            password_layout.addWidget(confirm_label)
            password_layout.addWidget(self.confirm_input)
            
        else:
            # Single password field for verification
            password_section = QFrame()
            password_layout = QVBoxLayout(password_section)
            password_layout.setSpacing(15)
            
            password_label = QLabel("Password")
            password_label.setObjectName("fieldLabel")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            
            self.password_input = QLineEdit()
            self.password_input.setObjectName("passwordInput")
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(40)
            self.password_input.setPlaceholderText("Enter your password...")
            self.password_input.setFont(QFont("Segoe UI", 12))
            
            password_layout.addWidget(password_label)
            password_layout.addWidget(self.password_input)
        
        # Show password checkbox
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.setObjectName("showPassword")
        self.show_password_cb.setFont(QFont("Segoe UI", 10))
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_cb)
        
        content_layout.addWidget(password_section)
        
        # Warning for verification mode
        if self.mode == "verify" and self.attempts > 1:
            warning = QLabel("⚠️ All data will be permanently deleted after 3 failed attempts!")
            warning.setObjectName("warningLabel")
            warning.setFont(QFont("Segoe UI", 10, QFont.Bold))
            warning.setAlignment(Qt.AlignCenter)
            warning.setWordWrap(True)
            content_layout.addWidget(warning)
        
        layout.addWidget(content, 1)
        
        # Button section
        button_section = QFrame()
        button_section.setObjectName("buttonSection")
        button_section.setFixedHeight(70)
        button_layout = QHBoxLayout(button_section)
        button_layout.setContentsMargins(40, 15, 40, 15)
        button_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setObjectName("cancelButton")
        self.cancel_btn.setMinimumSize(100, 40)
        self.cancel_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.cancel_btn.clicked.connect(self.reject)
        
        if self.mode == "create":
            self.ok_btn = QPushButton("Create Password")
        else:
            self.ok_btn = QPushButton("Sign In")
        
        self.ok_btn.setObjectName("okButton")
        self.ok_btn.setMinimumSize(140, 40)
        self.ok_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.ok_btn.setDefault(True)
        self.ok_btn.clicked.connect(self.accept_password)
        
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)
        
        layout.addWidget(button_section)
        
        # Set focus and enter key handling
        self.password_input.returnPressed.connect(self.accept_password)
        if self.mode == "create":
            self.confirm_input.returnPressed.connect(self.accept_password)
        self.password_input.setFocus()
    
    def toggle_password_visibility(self, state):
        """Toggle password visibility"""
        if state == Qt.Checked:
            self.password_input.setEchoMode(QLineEdit.Normal)
            if self.mode == "create":
                self.confirm_input.setEchoMode(QLineEdit.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            if self.mode == "create":
                self.confirm_input.setEchoMode(QLineEdit.Password)
    
    def accept_password(self):
        """Validate and accept password"""
        password = self.password_input.text().strip()
        
        if not password:
            self.show_error("Please enter a password.")
            return
        
        if self.mode == "create":
            # Validate password creation
            confirm_password = self.confirm_input.text().strip()
            
            if len(password) < 4:
                self.show_error("Password must be at least 4 characters long.")
                return
            
            if password != confirm_password:
                self.show_error("Passwords do not match.")
                return
        
        self.password = password
        self.accept()
    
    def show_error(self, message):
        """Show error message"""
        from PyQt5.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Invalid Input")
        msg_box.setText(message)
        msg_box.setStyleSheet(self.get_message_box_style())
        msg_box.exec_()
        
        self.password_input.setFocus()
        self.password_input.selectAll()
    
    def get_password(self):
        """Return the entered password"""
        return self.password
    
    def get_message_box_style(self):
        return """
            QMessageBox {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: #6366f1;
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #5b21b6;
            }
        """
    
    def apply_styles(self):
        """Apply dark mode theme"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1a1a1a;
                color: #e0e0e0;
            }
            
            QFrame#header {
                background-color: #6366f1;
                border: none;
                border-radius: 0;
            }
            
            QLabel#appTitle {
                color: #ffffff;
                background: transparent;
            }
            
            QLabel#subtitle {
                color: rgba(255, 255, 255, 0.9);
                background: transparent;
            }
            
            QLabel#subtitleError {
                color: #fef2f2;
                background: #ef4444;
                font-weight: bold;
                padding: 4px 8px;
                border-radius: 4px;
            }
            
            QFrame#content {
                background-color: #1a1a1a;
                border: none;
            }
            
            QLabel#fieldLabel {
                color: #e0e0e0;
                background: transparent;
            }
            
            QLineEdit#passwordInput {
                background-color: #2b2b2b;
                color: #e0e0e0;
                border: 2px solid #404040;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 12px;
            }
            
            QLineEdit#passwordInput:focus {
                border-color: #6366f1;
                background-color: #333333;
                outline: none;
            }
            
            QLineEdit#passwordInput::placeholder {
                color: #6b7280;
            }
            
            QCheckBox#showPassword {
                color: #d1d5db;
                font-size: 10px;
                spacing: 8px;
            }
            
            QCheckBox#showPassword::indicator {
                width: 16px;
                height: 16px;
            }
            
            QCheckBox#showPassword::indicator:unchecked {
                background-color: #2b2b2b;
                border: 2px solid #555555;
                border-radius: 3px;
            }
            
            QCheckBox#showPassword::indicator:checked {
                background-color: #6366f1;
                border: 2px solid #6366f1;
                border-radius: 3px;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTAiIGhlaWdodD0iMTAiIHZpZXdCb3g9IjAgMCAxMCAxMCIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTguNSAzTDQgNy41TDEuNSA1IiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjIiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIgc3Ryb2tlLWxpbmVqb2luPSJyb3VuZCIvPgo8L3N2Zz4K);
            }
            
            QCheckBox#showPassword::indicator:checked:hover {
                background-color: #5b21b6;
                border-color: #5b21b6;
            }
            
            QLabel#warningLabel {
                color: #fef2f2;
                background-color: #7f1d1d;
                border: 1px solid #dc2626;
                border-radius: 6px;
                padding: 10px;
                margin: 10px 0;
            }
            
            QFrame#buttonSection {
                background-color: #2b2b2b;
                border-top: 1px solid #404040;
                border-radius: 0;
            }
            
            QPushButton#okButton {
                background-color: #6366f1;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            
            QPushButton#okButton:hover {
                background-color: #5b21b6;
            }
            
            QPushButton#okButton:pressed {
                background-color: #4c1d95;
            }
            
            QPushButton#cancelButton {
                background-color: #3a3a3a;
                color: #e0e0e0;
                border: 1px solid #555555;
                border-radius: 6px;
                font-weight: bold;
            }
            
            QPushButton#cancelButton:hover {
                background-color: #4a4a4a;
                border-color: #6b7280;
            }
            
            QPushButton#cancelButton:pressed {
                background-color: #555555;
            }
        """)