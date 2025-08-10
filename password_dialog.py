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
        
        self.setWindowTitle("SecureJournal Pro - Authentication")
        self.setModal(True)
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Dialog | Qt.WindowTitleHint)
        
        self.setup_ui()
        self.apply_styles()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title and icon
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setAlignment(Qt.AlignCenter)
        
        # App title
        app_title = QLabel("🔒 SecureJournal Pro")
        app_title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        app_title.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(app_title)
        
        # Mode-specific subtitle
        if self.mode == "create":
            subtitle = QLabel("Set your master password")
            subtitle.setStyleSheet("color: #4a9eff; font-size: 14px;")
        else:
            subtitle = QLabel(f"Enter your password (Attempt {self.attempts}/3)")
            if self.attempts > 1:
                subtitle.setStyleSheet("color: #ff6b6b; font-size: 14px;")
            else:
                subtitle.setStyleSheet("color: #cccccc; font-size: 14px;")
        
        subtitle.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle)
        
        layout.addWidget(title_frame)
        
        # Password input section
        password_frame = QFrame()
        password_layout = QVBoxLayout(password_frame)
        
        if self.mode == "create":
            # Password field
            password_label = QLabel("Password:")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            password_layout.addWidget(password_label)
            
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(35)
            self.password_input.setPlaceholderText("Enter a secure password...")
            password_layout.addWidget(self.password_input)
            
            # Confirm password field
            confirm_label = QLabel("Confirm Password:")
            confirm_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            password_layout.addWidget(confirm_label)
            
            self.confirm_input = QLineEdit()
            self.confirm_input.setEchoMode(QLineEdit.Password)
            self.confirm_input.setMinimumHeight(35)
            self.confirm_input.setPlaceholderText("Confirm your password...")
            password_layout.addWidget(self.confirm_input)
            
        else:
            # Single password field for verification
            password_label = QLabel("Password:")
            password_label.setFont(QFont("Segoe UI", 11, QFont.Bold))
            password_layout.addWidget(password_label)
            
            self.password_input = QLineEdit()
            self.password_input.setEchoMode(QLineEdit.Password)
            self.password_input.setMinimumHeight(35)
            self.password_input.setPlaceholderText("Enter your password...")
            password_layout.addWidget(self.password_input)
        
        # Show password checkbox
        self.show_password_cb = QCheckBox("Show password")
        self.show_password_cb.stateChanged.connect(self.toggle_password_visibility)
        password_layout.addWidget(self.show_password_cb)
        
        layout.addWidget(password_frame)
        
        # Warning for verification mode
        if self.mode == "verify" and self.attempts > 1:
            warning_label = QLabel("⚠️ Warning: All data will be permanently deleted after 3 failed attempts!")
            warning_label.setStyleSheet("color: #ff6b6b; font-size: 10px; font-weight: bold;")
            warning_label.setAlignment(Qt.AlignCenter)
            warning_label.setWordWrap(True)
            layout.addWidget(warning_label)
        
        # Buttons
        button_frame = QFrame()
        button_layout = QHBoxLayout(button_frame)
        button_layout.setSpacing(15)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setMinimumSize(80, 35)
        self.cancel_btn.clicked.connect(self.reject)
        
        if self.mode == "create":
            self.ok_btn = QPushButton("Set Password")
        else:
            self.ok_btn = QPushButton("Login")
        
        self.ok_btn.setMinimumSize(100, 35)
        self.ok_btn.setDefault(True)
        self.ok_btn.clicked.connect(self.accept_password)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch()
        button_layout.addWidget(self.ok_btn)
        
        layout.addWidget(button_frame)
        
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
        QMessageBox.warning(self, "Invalid Input", message)
        self.password_input.setFocus()
        self.password_input.selectAll()
    
    def get_password(self):
        """Return the entered password"""
        return self.password
    
    def apply_styles(self):
        """Apply dark theme styles"""
        self.setStyleSheet("""
            QDialog {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            
            QLabel {
                color: #ffffff;
                background: transparent;
            }
            
            QLineEdit {
                background-color: #3a3a3a;
                color: #ffffff;
                border: 2px solid #555;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 12px;
            }
            
            QLineEdit:focus {
                border-color: #4a9eff;
                outline: none;
            }
            
            QPushButton {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #6b7280, stop: 1 #4b5563);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 11px;
            }
            
            QPushButton:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #7c8590, stop: 1 #5a6470);
            }
            
            QPushButton:pressed {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #4b5563, stop: 1 #374151);
            }
            
            QPushButton:default {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #4a9eff, stop: 1 #3b82f6);
            }
            
            QPushButton:default:hover {
                background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                           stop: 0 #5babff, stop: 1 #4c8df7);
            }
            
            QCheckBox {
                color: #cccccc;
                font-size: 10px;
            }
            
            QCheckBox::indicator {
                width: 15px;
                height: 15px;
            }
            
            QCheckBox::indicator:unchecked {
                background-color: #3a3a3a;
                border: 2px solid #555;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked {
                background-color: #4a9eff;
                border: 2px solid #4a9eff;
                border-radius: 3px;
            }
            
            QCheckBox::indicator:checked:hover {
                background-color: #5babff;
                border-color: #5babff;
            }
        """)