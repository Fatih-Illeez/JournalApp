import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QPalette, QColor
from journal_app import EncryptedJournal


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties
    app.setApplicationName("SecureJournal Pro")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("SecureApps")
    
    # Set dark palette for title bar
    palette = app.palette()
    palette.setColor(QPalette.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    app.setPalette(palette)
    
    journal = EncryptedJournal()
    journal.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()