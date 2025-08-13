import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QPalette, QColor, QIcon, QPixmap, QPainter, QPen, QRadialGradient
from PyQt5.QtCore import Qt, QRect


from PyQt5.QtCore import Qt

# Import the updated journal app
from journal_app import EncryptedJournal


def create_elephant_icon():
    """Create a professional elephant icon for the application"""
    # Create multiple sizes for better Windows integration
    sizes = [16, 24, 32, 48, 64, 128, 256]
    icon = QIcon()
    
    for size in sizes:
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        
        # Calculate scaling factors
        scale = size / 64.0
        
        # Draw background circle with gradient
        gradient = QRadialGradient(size/2, size/2, size/2)
        gradient.setColorAt(0, QColor(99, 102, 241))  # Indigo
        gradient.setColorAt(0.8, QColor(67, 56, 202))  # Darker indigo
        gradient.setColorAt(1, QColor(55, 48, 163))    # Even darker
        
        painter.setPen(Qt.NoPen)
        painter.setBrush(gradient)
        painter.drawEllipse(int(2*scale), int(2*scale), 
                          int((size-4)*scale), int((size-4)*scale))
        
        # Add subtle border
        painter.setPen(QPen(QColor(45, 55, 135), max(1, int(2*scale))))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(int(2*scale), int(2*scale), 
                          int((size-4)*scale), int((size-4)*scale))
        
        # Draw elephant emoji with proper scaling
        painter.setPen(QColor(255, 255, 255))
        font = painter.font()
        font.setPointSize(max(8, int(28*scale)))
        font.setFamily("Segoe UI Emoji")
        painter.setFont(font)
        
        # Center the emoji
        rect = QRect(0, 0, size, size)
        painter.drawText(rect, Qt.AlignCenter, "🐘")
        
        # Add shine effect for larger sizes
        if size >= 32:
            shine_gradient = QRadialGradient(size*0.3, size*0.3, size*0.4)
            shine_gradient.setColorAt(0, QColor(255, 255, 255, 40))
            shine_gradient.setColorAt(1, QColor(255, 255, 255, 0))
            painter.setBrush(shine_gradient)
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(size*0.1), int(size*0.1), 
                              int(size*0.5), int(size*0.5))
        
        painter.end()
        icon.addPixmap(pixmap, QIcon.Normal, QIcon.Off)
    
    return icon


def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Modern look
    
    # Set application properties with elephant icon
    app.setApplicationName("SecureJournal")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("SecureApps")
    app.setApplicationDisplayName("SecureJournal")
    
    # Create and set the elephant icon
    elephant_icon = create_elephant_icon()
    app.setWindowIcon(elephant_icon)
    
    # Also set app icon for taskbar (Windows)
    if sys.platform == "win32":
        try:
            import ctypes
            # Set the app user model ID for proper Windows taskbar grouping
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("SecureApps.SecureJournal.2.0")
        except:
            pas
    
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
    
    # Set additional dark mode application styling with black title bar
    app.setStyleSheet("""
        QMainWindow {
            background-color: #1a1a1a;
        }
        
        /* Black title bar styling for Windows */
        QMainWindow::title {
            background-color: #000000;
            color: #ffffff;
            padding: 5px;
        }
        
        /* Title bar button styling */
        QMainWindow::close-button, QMainWindow::minimize-button, QMainWindow::maximize-button {
            background-color: #000000;
            color: #ffffff;
        }
        
        QMainWindow::close-button:hover {
            background-color: #e74c3c;
        }
        
        QMainWindow::minimize-button:hover, QMainWindow::maximize-button:hover {
            background-color: #333333;
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
        
        /* Dialog styling to match the dark theme */
        QDialog {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        QMessageBox {
            background-color: #2b2b2b;
            color: #e0e0e0;
        }
        QMessageBox QLabel {
            color: #e0e0e0;
            font-size: 12px;
        }
        QMessageBox QPushButton {
            background-color: #404040;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px 20px;
            font-weight: bold;
            min-width: 80px;
        }
        QMessageBox QPushButton:hover {
            background-color: #505050;
            border-color: #6366f1;
            color: #c7d2fe;
        }
        QMessageBox QPushButton:pressed {
            background-color: #6366f1;
            color: #ffffff;
        }
        
        /* Input dialog styling */
        QInputDialog {
            background-color: #2b2b2b;
            color: #e0e0e0;
        }
        QInputDialog QLineEdit {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: 2px solid #555555;
            border-radius: 6px;
            padding: 8px;
        }
        QInputDialog QLineEdit:focus {
            border-color: #6366f1;
        }
        QInputDialog QPushButton {
            background-color: #404040;
            color: #e0e0e0;
            border: 1px solid #555;
            border-radius: 4px;
            padding: 8px 20px;
            min-width: 80px;
        }
        QInputDialog QPushButton:hover {
            background-color: #505050;
            border-color: #6366f1;
        }
        
        /* File dialog styling */
        QFileDialog {
            background-color: #2b2b2b;
            color: #e0e0e0;
        }
        
        /* Tooltip styling */
        QToolTip {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #404040;
            border-radius: 4px;
            padding: 6px;
        }
    """)
    
    # Set platform-specific window flags for proper title bar theming
    if sys.platform == "win32":
        # For Windows - try to use custom title bar handling
        try:
            import ctypes
            from ctypes import wintypes
            # This might help with title bar theming on Windows
            ctypes.windll.dwmapi.DwmSetWindowAttribute.argtypes = [wintypes.HWND, wintypes.DWORD, ctypes.POINTER(ctypes.c_int), wintypes.DWORD]
        except:
            pass  # Fallback if ctypes not available
    
    try:
        journal = EncryptedJournal()
        
        # Set the elephant icon for the main window as well
        journal.setWindowIcon(elephant_icon)
        
        # Additional window styling for title bar
        journal.setStyleSheet(journal.styleSheet() + """
            QMainWindow {
                border: 1px solid #000000;
            }
        """)
        
        # Check if authentication was successful
        if hasattr(journal, 'fernet') and journal.fernet is not None:
            journal.show()
            
            # Try to set window attributes for better title bar theming
            if sys.platform == "win32":
                try:
                    import ctypes
                    from ctypes import wintypes
                    
                    hwnd = journal.winId()
                    # DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                    # This enables dark mode for the title bar on Windows 10/11
                    value = ctypes.c_int(1)
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        int(hwnd), 
                        20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                        ctypes.byref(value),
                        ctypes.sizeof(value)
                    )
                    
                     # Set window icon in multiple sizes for Windows
                    icon_sizes = [16, 32, 48]
                    for size in icon_sizes:
                        pixmap = elephant_icon.pixmap(size, size)
                        # Windows will automatically use the best size

                except Exception as e:
                    print(f"Could not set dark title bar: {e}")
            
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
        msg.setWindowIcon(elephant_icon)  # Add icon to error dialog too
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QMessageBox QLabel {
                color: #e0e0e0;
                font-size: 12px;
            }
            QMessageBox QPushButton {
                background-color: #e74c3c;
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