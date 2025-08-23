def get_app_stylesheet():
    """Return the main application stylesheet with enhanced dark theme and improved hover effects"""
    return """
    /* Main Application Styling */
    QMainWindow {
        background-color: #1a1a1a;
        color: #e0e0e0;
        border: none;
    }
    
    /* Title Bar Styling (where supported) */
    QMainWindow::title {
        background-color: #000000;
        color: #ffffff;
        padding: 5px;
    }
    
    /* Central Widget */
    QWidget {
        background-color: #1a1a1a;
        color: #e0e0e0;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
    }
    
    /* Toggle Button - FIXED */
    QPushButton#toggleButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #6366f1, stop: 1 #4f46e5);
        color: #ffffff;
        border: 2px solid #4f46e5;
        border-radius: 16px;
        font-size: 14px;
        font-weight: bold;
        padding: 0px;
        margin: 0px;
        transition: all 0.2s ease;
    }
    
    QPushButton#toggleButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border: 3px solid #374151;
        color: #f3f4f6;
        font-size: 15px;
    }
    
    QPushButton#toggleButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #111827, stop: 1 #030712);
        border: 3px solid #111827;
        font-size: 13px;
    }
    
    /* General Buttons - Enhanced hover with darker colors */
    QPushButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #404040, stop: 1 #2b2b2b);
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        min-height: 20px;
        transition: all 0.2s ease;
    }
    
    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border: 3px solid #374151;
        color: #f9fafb;
        transform: scale(1.02);
        font-weight: 900;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #111827, stop: 1 #030712);
        color: #ffffff;
        border: 3px solid #111827;
        transform: scale(0.98);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    QPushButton:disabled {
        background-color: #2b2b2b;
        color: #666666;
        border: 2px solid #333333;
        transform: none;
        box-shadow: none;
    }
    
    /* Round Buttons for + actions - Enhanced */
    QPushButton#roundButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #10b981, stop: 1 #059669);
        color: #ffffff;
        border: 2px solid #34d399;
        border-radius: 14px;
        font-size: 14px;
        font-weight: bold;
        padding: 0px;
        transition: all 0.2s ease;
    }
    
    QPushButton#roundButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #166534, stop: 1 #14532d);
        border: 3px solid #166534;
        color: #f0fdf4;
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        font-size: 15px;
    }
    
    QPushButton#roundButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #052e16, stop: 1 #022c22);
        border: 3px solid #052e16;
        transform: scale(1.05);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Delete Button Styling - Enhanced */
    QPushButton#deleteButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #ef4444, stop: 1 #dc2626);
        border: 2px solid #f87171;
        color: #ffffff;
        transition: all 0.2s ease;
    }
    
    QPushButton#deleteButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #7f1d1d, stop: 1 #450a0a);
        border: 3px solid #7f1d1d;
        color: #fef2f2;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
        font-weight: 900;
    }
    
    QPushButton#deleteButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #450a0a, stop: 1 #1c0000);
        border: 3px solid #450a0a;
        transform: scale(0.98);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    /* Lock Button - Enhanced */
    QPushButton#lockButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #dc2626, stop: 1 #991b1b);
        color: #ffffff;
        border: 2px solid #ef4444;
        transition: all 0.2s ease;
    }
    
    QPushButton#lockButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #7f1d1d, stop: 1 #450a0a);
        border: 3px solid #7f1d1d;
        color: #fef2f2;
        transform: scale(1.02);
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        font-weight: 900;
    }
    
    QPushButton#lockButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #450a0a, stop: 1 #1c0000);
        border: 3px solid #450a0a;
        transform: scale(0.98);
    }
    
    /* Tool Buttons - Enhanced hover */
    QToolButton {
        background-color: transparent;
        color: #e0e0e0;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        margin: 1px;
        transition: all 0.2s ease;
    }
    
    QToolButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border: 2px solid #374151;
        color: #f9fafb;
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    QToolButton:checked {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4338ca, stop: 1 #3730a3);
        color: white;
        border: 2px solid #4338ca;
    }
    
    QToolButton:checked:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 2px solid #312e81;
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(67, 56, 202, 0.4);
    }
    
    QToolButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #111827, stop: 1 #030712);
        color: white;
        transform: scale(0.95);
    }
    
    /* Entry Title */
    QLineEdit#entryTitle {
        background-color: #252525;
        color: #ffffff;
        border: 2px solid transparent;
        border-radius: 8px;
        padding: 12px 16px;
        font-size: 18px;
        font-weight: bold;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
    }
    
    QLineEdit#entryTitle:focus {
        border-color: #6366f1;
        background-color: #2a2a2a;
    }
    
    QLineEdit#entryTitle::placeholder {
        color: #888888;
        font-style: italic;
    }
    
    /* Line Edits */
    QLineEdit {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 8px 12px;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
    }
    
    QLineEdit:focus {
        border-color: #6366f1;
        background-color: #252525;
    }
    
    QLineEdit::placeholder {
        color: #666666;
    }
    
    /* Main Editor */
    QTextEdit#mainEditor {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 20px;
        selection-background-color: #dbeafe;
        selection-color: #1f2937;
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
    }
    
    QTextEdit#mainEditor:focus {
        border-color: #6366f1;
        background-color: #ffffff;
    }
    
    /* Text Edits */
    QTextEdit {
        background-color: #1e1e1e;
        color: #e0e0e0;
        border: 2px solid #404040;
        border-radius: 8px;
        padding: 15px;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
    }
    
    QTextEdit:focus {
        border-color: #6366f1;
        background-color: #252525;
    }
    
    QTextEdit::placeholder {
        color: #666666;
    }
    
    /* List Widgets - Notebooks and Entries */
    QListWidget#notebooksList, QListWidget#entriesList {
        background-color: #1e1e1e;
        border: 1px solid #333333;
        border-radius: 6px;
        outline: none;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
        padding: 8px;
    }
    
    QListWidget#notebooksList::item, QListWidget#entriesList::item {
        background-color: transparent;
        border: none;
        padding: 12px 8px;
        margin: 2px 0px;
        border-radius: 6px;
        color: #e0e0e0;
        border-left: 3px solid transparent;
        transition: all 0.2s ease;
    }
    
    QListWidget#notebooksList::item:selected, QListWidget#entriesList::item:selected {
        background-color: #6366f1;
        color: white;
        border-left: 3px solid #ffffff;
        font-weight: bold;
    }
    
    QListWidget#notebooksList::item:hover, QListWidget#entriesList::item:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border-left: 3px solid #374151;
        color: #f9fafb;
        transform: translateX(2px);
    }
    
    /* List Widgets */
    QListWidget {
        background-color: #252525;
        border: 1px solid #404040;
        border-radius: 8px;
        outline: none;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
    }
    
    QListWidget::item {
        background-color: transparent;
        border: none;
        padding: 12px;
        margin: 2px;
        border-radius: 6px;
        color: #e0e0e0;
        transition: all 0.2s ease;
    }
    
    QListWidget::item:selected {
        background-color: #6366f1;
        color: white;
        font-weight: bold;
    }
    
    QListWidget::item:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
    }
    
    /* Frames */
    QFrame {
        background-color: #252525;
        border: 1px solid #404040;
        border-radius: 8px;
        color: #e0e0e0;
    }
    
    /* Writing Container */
    QFrame#writingContainer {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    /* Formatting Toolbar - Enhanced */
    QFrame#formattingToolbar {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #2b2b2b);
        border: 1px solid #4b5563;
        border-radius: 8px;
        color: #e0e0e0;
    }
    
    QPushButton[class="formatting"] {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4b5563, stop: 1 #374151);
        color: #e0e0e0;
        border: 1px solid #6b7280;
        border-radius: 6px;
        padding: 6px;
        font-weight: bold;
        transition: all 0.2s ease;
    }
    
    QPushButton[class="formatting"]:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #1f2937, stop: 1 #111827);
        border: 2px solid #1f2937;
        color: #f9fafb;
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        font-weight: 900;
    }
    
    QPushButton[class="formatting"]:checked {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4338ca, stop: 1 #3730a3);
        color: #ffffff;
        border: 2px solid #4338ca;
        font-weight: bold;
    }
    
    QPushButton[class="formatting"]:checked:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 2px solid #312e81;
        transform: scale(1.05);
        box-shadow: 0 2px 8px rgba(67, 56, 202, 0.4);
    }
    
    QPushButton[class="formatting"]:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #111827, stop: 1 #030712);
        color: #ffffff;
        transform: scale(0.95);
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    /* Storage Section */
    QFrame#storageSection {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #1f2937, stop: 1 #111827);
        border: 1px solid #374151;
        border-radius: 6px;
    }
    
    QLabel#storageInfo {
        color: #d1d5db;
        font-weight: bold;
        background: transparent;
        border: none;
    }
    
    /* Labels */
    QLabel {
        background-color: transparent;
        color: #e0e0e0;
        border: none;
    }
    
    QLabel#sectionHeader {
        color: #c7d2fe;
        font-weight: bold;
        background: transparent;
        border: none;
    }
    
    QLabel#dateLabel {
        color: #6b7280;
        background: transparent;
        border: none;
    }
    
    QLabel#countLabel {
        color: #9ca3af;
        background: transparent;
        border: none;
    }
    
    QLabel#saveStatus {
        background: transparent;
        border: none;
    }
    
    QLabel#saveStatus[saved="true"] {
        color: #10b981;
        font-weight: bold;
    }
    
    QLabel#saveStatus[saved="false"] {
        color: #ef4444;
        font-weight: bold;
    }
    
    /* Splitters */
    QSplitter::handle {
        background-color: #404040;
        width: 2px;
        height: 2px;
    }
    
    QSplitter::handle:hover {
        background-color: #6366f1;
    }
    
    QSplitter::handle:pressed {
        background-color: #4f46e5;
    }
    
    /* Scroll Bars */
    QScrollBar:vertical {
        background: #2b2b2b;
        width: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    
    QScrollBar::handle:vertical {
        background: #555555;
        border-radius: 6px;
        min-height: 20px;
        margin: 2px;
    }
    
    QScrollBar::handle:vertical:hover {
        background: #666666;
    }
    
    QScrollBar::handle:vertical:pressed {
        background: #6366f1;
    }
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    
    QScrollBar:horizontal {
        background: #2b2b2b;
        height: 12px;
        border-radius: 6px;
        margin: 0px;
    }
    
    QScrollBar::handle:horizontal {
        background: #555555;
        border-radius: 6px;
        min-width: 20px;
        margin: 2px;
    }
    
    QScrollBar::handle:horizontal:hover {
        background: #666666;
    }
    
    QScrollBar::handle:horizontal:pressed {
        background: #6366f1;
    }
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        border: none;
        background: none;
        width: 0px;
    }
    
    /* Combo Boxes - Enhanced hover */
    QComboBox {
        background-color: #404040;
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 100px;
        transition: all 0.2s ease;
    }
    
    QComboBox:hover {
        border: 3px solid #374151;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
        transform: scale(1.02);
    }
    
    QComboBox:focus {
        border-color: #6366f1;
        background-color: #505050;
    }
    
    QComboBox::drop-down {
        border: none;
        width: 20px;
    }
    
    QComboBox::down-arrow {
        image: none;
        border-left: 5px solid transparent;
        border-right: 5px solid transparent;
        border-top: 5px solid #e0e0e0;
    }
    
    QComboBox QAbstractItemView {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: 1px solid #404040;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
        outline: none;
    }
    
    /* Spin Boxes - Enhanced hover */
    QSpinBox {
        background-color: #404040;
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 6px;
        min-width: 60px;
        transition: all 0.2s ease;
    }
    
    QSpinBox:hover {
        border: 3px solid #374151;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
        transform: scale(1.02);
    }
    
    QSpinBox:focus {
        border-color: #6366f1;
        background-color: #505050;
    }
    
    QSpinBox::up-button, QSpinBox::down-button {
        background-color: #555555;
        border: none;
        width: 16px;
        transition: all 0.2s ease;
    }
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        transform: scale(1.1);
    }
    
    QSpinBox::up-arrow {
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-bottom: 4px solid #e0e0e0;
    }
    
    QSpinBox::down-arrow {
        border-left: 4px solid transparent;
        border-right: 4px solid transparent;
        border-top: 4px solid #e0e0e0;
    }
    
    /* Tool Bars */
    QToolBar {
        background-color: #2b2b2b;
        border: 1px solid #404040;
        border-radius: 6px;
        spacing: 3px;
        padding: 5px;
        color: #e0e0e0;
    }
    
    QToolBar::separator {
        background-color: #555555;
        width: 1px;
        height: 20px;
        margin: 0 5px;
    }
    
    /* Status Bar */
    QStatusBar {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border-top: 1px solid #404040;
        padding: 4px;
    }
    
    QStatusBar::item {
        border: none;
        padding: 0 5px;
    }
    
    /* Menu Bar */
    QMenuBar {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border-bottom: 1px solid #404040;
        padding: 4px;
    }
    
    QMenuBar::item {
        background-color: transparent;
        padding: 6px 12px;
        border-radius: 4px;
        transition: all 0.2s ease;
    }
    
    QMenuBar::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
    }
    
    QMenuBar::item:pressed {
        background-color: #6366f1;
        color: #ffffff;
    }
    
    /* Menus */
    QMenu {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 6px;
        padding: 4px;
    }
    
    QMenu::item {
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 4px;
        margin: 1px;
        transition: all 0.2s ease;
    }
    
    QMenu::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
    }
    
    QMenu::item:pressed {
        background-color: #6366f1;
        color: #ffffff;
    }
    
    QMenu::separator {
        height: 1px;
        background-color: #555555;
        margin: 4px 8px;
    }
    
    /* Dialog Styling */
    QDialog {
        background-color: #1a1a1a;
        color: #e0e0e0;
        border: 1px solid #404040;
    }
    
    /* Message Box Styling */
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
        transition: all 0.2s ease;
    }
    
    QMessageBox QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border: 2px solid #374151;
        color: #f9fafb;
        transform: scale(1.02);
    }
    
    QMessageBox QPushButton:pressed {
        background-color: #6366f1;
        color: #ffffff;
        transform: scale(0.98);
    }
    
    /* Input Dialog Styling */
    QInputDialog {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    
    /* File Dialog Styling */
    QFileDialog {
        background-color: #2b2b2b;
        color: #e0e0e0;
    }
    
    /* Tooltip Styling */
    QToolTip {
        background-color: #2b2b2b;
        color: #e0e0e0;
        border: 1px solid #404040;
        border-radius: 4px;
        padding: 6px;
        font-size: 11px;
    }
    
    /* Tab Widget (if used) */
    QTabWidget::pane {
        background-color: #252525;
        border: 1px solid #404040;
        border-radius: 6px;
    }
    
    QTabBar::tab {
        background-color: #404040;
        color: #e0e0e0;
        border: 1px solid #555555;
        border-bottom: none;
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        margin: 0 2px;
        transition: all 0.2s ease;
    }
    
    QTabBar::tab:selected {
        background-color: #6366f1;
        color: #ffffff;
        border-color: #4f46e5;
    }
    
    QTabBar::tab:hover:!selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        border: 2px solid #374151;
        color: #f9fafb;
        transform: scale(1.02);
    }
    
    /* Progress Bar (if used) */
    QProgressBar {
        background-color: #2b2b2b;
        border: 1px solid #404040;
        border-radius: 6px;
        text-align: center;
        color: #e0e0e0;
    }
    
    QProgressBar::chunk {
        background-color: #6366f1;
        border-radius: 5px;
    }
    
    /* Slider (if used) */
    QSlider::groove:horizontal {
        border: 1px solid #555;
        height: 4px;
        background: #2b2b2b;
        border-radius: 2px;
    }
    
    QSlider::handle:horizontal {
        background: #6366f1;
        border: 1px solid #4f46e5;
        width: 18px;
        margin: -7px 0;
        border-radius: 9px;
        transition: all 0.2s ease;
    }
    
    QSlider::handle:horizontal:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        transform: scale(1.1);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    }
    
    QSlider::handle:horizontal:pressed {
        background: #4f46e5;
        transform: scale(0.9);
    }
    """