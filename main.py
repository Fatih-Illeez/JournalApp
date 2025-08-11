import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

# Import the updated journal app
from journal_app import EncryptedJournal


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("SecureJournal")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("SecureApps")
    
    # Set dark mode palette
    palette = app.palette()
    
    # Dark theme colors
    palette.setColor(QPalette.Window, QColor(26, 26, 26))           # Very dark gray background
    palette.setColor(QPalette.WindowText, QColor(224, 224, 224))    # Light gray text
    
    # Button colors
    palette.setColor(QPalette.Button, QColor(43, 43, 43))           # Dark gray buttons
    palette.setColor(QPalette.ButtonText, QColor(224, 224, 224))    # Light button text
    
    # Highlight colors (modern blue)
    palette.setColor(QPalette.Highlight, QColor(99, 102, 241))      # Indigo blue
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255)) # White highlighted text
    
    # Base colors for input fields
    palette.setColor(QPalette.Base, QColor(30, 30, 30))             # Dark input backgrounds
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 45))    # Slightly lighter alternate
    
    # Text colors
    palette.setColor(QPalette.Text, QColor(224, 224, 224))          # Light text
    palette.setColor(QPalette.BrightText, QColor(248, 113, 113))    # Light red for errors
    
    # Tooltip colors
    palette.setColor(QPalette.ToolTipBase, QColor(43, 43, 43))
    palette.setColor(QPalette.ToolTipText, QColor(224, 224, 224))
    
    app.setPalette(palette)
    
   # Set additional dark mode application styling
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1a1a1a;
        }
        QMenuBar {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border-bottom: 1px solid #404040;
            padding: 4px;
        }
        QMenuBar::item {
            background-color: transparent;
            padding: 4px 8px;
            border-radius: 4px;
        }
        QMenuBar::item:selected {
            background-color: #4a4a4a;
            color: #c7d2fe;
        }
        QMenuBar::item:pressed {
            background-color: #6366f1;
            color: #ffffff;
        }
        QMenu {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #404040;
            border-radius: 6px;
            padding: 4px;
        }
        QMenu::item {
            background-color: transparent;
            padding: 6px 12px;
            border-radius: 4px;
        }
        QMenu::item:selected {
            background-color: #4a4a4a;
            color: #c7d2fe;
        }
    """)
    
    try:
        journal = EncryptedJournal()
        
        # Check if authentication was successful
        if hasattr(journal, 'fernet') and journal.fernet is not None:
            journal.show()
            sys.exit(app.exec_())
        else:
            # Authentication failed or was cancelled
            sys.exit(0)
            
    except Exception as e:
        # Style the error message box too
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle("Startup Error")
        msg.setText(f"Failed to start SecureJournal:\n{str(e)}")
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #ffffff;
                color: #333333;
            }
            QMessageBox QLabel {
                color: #333333;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;pu
                color: #ffffff;
                border: none;
                border-radius: 4px;
                padding: 8px 20px;
                font-weight: bold;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        msg.exec_()
        sys.exit(1)


if __name__ == "__main__":
    main()