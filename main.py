import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from journal_app import EncryptedJournal


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("SecureJournal Pro")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("SecureApps")
    
    # Set dark palette for title bar and entire application
    palette = app.palette()
    
    # Window colors (affects title bar)
    palette.setColor(QPalette.Window, QColor(0, 0, 0))  # Black background
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))  # White text
    
    # Button colors (affects title bar buttons)
    palette.setColor(QPalette.Button, QColor(30, 30, 30))  # Dark gray buttons
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))  # White button text
    
    # Highlight colors
    palette.setColor(QPalette.Highlight, QColor(107, 114, 128))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    
    # Base colors for input fields
    palette.setColor(QPalette.Base, QColor(58, 58, 58))
    palette.setColor(QPalette.AlternateBase, QColor(66, 66, 66))
    
    # Text colors
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
    
    # Tooltip colors
    palette.setColor(QPalette.ToolTipBase, QColor(0, 0, 0))
    palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
    
    app.setPalette(palette)
    
    # Set additional style for better dark theme support
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1e1e1e;
        }
        QMenuBar {
            background-color: #000000;
            color: #ffffff;
            border: none;
        }
        QMenuBar::item:selected {
            background-color: #333333;
        }
    """)
    
    journal = EncryptedJournal()
    journal.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()