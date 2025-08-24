def get_app_stylesheet():
    """Return the main application stylesheet with enhanced dark theme and full-width layout (Qt-safe)"""
    return """
    /* Main Application Styling */
    QMainWindow {
        background-color: #0d0d0d;
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
    
    /* Toggle Button */
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
    }
    
    QPushButton#toggleButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        border: 3px solid #7c3aed;
        color: #f3f4f6;
        font-size: 15px;     /* enlarge */
    }
    
    QPushButton#toggleButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 3px solid #5b21b6;
        font-size: 14px;
    }
    
    /* General Buttons */
    QPushButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #404040, stop: 1 #2b2b2b);
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        min-height: 20px;
    }
    
    /*Save Button (hover dark purple per request)  */
    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-size: 15px;       /* enlarge */
        padding: 10px 18px;    /* enlarge */
        font-weight: 900;
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b); /* very dark indigo/purple */
        color: #ffffff;
        border: 2px solid #5b21b6;
        font-size: 14px;       /* slight shrink from hover */
        padding: 8px 16px;
    }
    
    QPushButton:disabled {
        background-color: #2b2b2b;
        color: #666666;
        border: 2px solid #333333;
    }
    
    /* Round Buttons for + actions */
    QPushButton#roundButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #10b981, stop: 1 #059669);
        color: #34d399;
        border: 2px solid #34d399;
        border-radius: 14px;
        font-size: 14px;
        font-weight: bold;
        padding: 0px 10px;
    }
    
    QPushButton#roundButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-size: 15px;
        padding: 2px 12px;
    }
    
    QPushButton#roundButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 2px solid #5b21b6;
        font-size: 14px;
        padding: 0px 10px;
    }
    
    /* Delete Button Styling (hover now dark purple per request) */
    QPushButton#deleteButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #ef4444, stop: 1 #dc2626);
        border: 2px solid #f87171;
        color: #ffffff;
    }
    
    QPushButton#deleteButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-size: 15px;
        padding: 10px 18px;
        font-weight: 900;
    }
    
    QPushButton#deleteButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 2px solid #5b21b6;
        font-size: 14px;
        padding: 8px 16px;
    }
    
    /* Lock Button (hover dark purple per request) */
    QPushButton#lockButton {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #dc2626, stop: 1 #991b1b);
        color: #ffffff;
        border: 2px solid #ef4444;
    }
    
    QPushButton#lockButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-size: 15px;
        padding: 10px 18px;
        font-weight: 900;
    }
    
    QPushButton#lockButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        border: 2px solid #5b21b6;
        font-size: 14px;
        padding: 8px 16px;
    }
    
    /* Tool Buttons (bold, italic, etc.) */
    QToolButton {
        background-color: transparent;
        color: #e0e0e0;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        margin: 1px;
    }
    
    QToolButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-weight: 700;
        padding: 8px; /* slightly larger on hover */
    }
    
    QToolButton:checked {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4338ca, stop: 1 #3730a3);
        color: white;
        border: 2px solid #4338ca;
    }
    
    QToolButton:checked:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        border: 2px solid #7c3aed;
        padding: 8px;
    }
    
    QToolButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        color: white;
        padding: 6px; /* revert to base size */
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
    
    /* Main Editor (optional id) */
    QTextEdit#mainEditor {
        background-color: #0a0a0a;
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
    
    /* List Widgets - Full Width with improved formatting */
    QListWidget#notebooksList, QListWidget#entriesList {
        background-color: #2b2b2b;
        border: none;
        border-radius: 0;
        outline: none;
        selection-background-color: #6366f1;
        selection-color: #ffffff;
        padding: 0px;
        margin: 0px;
        font-size: 12px;
    }
    
    QListWidget#notebooksList::item, QListWidget#entriesList::item {
        background-color: transparent;
        border: none;
        padding: 12px 15px;
        margin: 0px;
        border-radius: 0px;
        color: #e0e0e0;
        border-bottom: 1px solid #333333;
        min-height: 60px;
    }
    
    QListWidget#notebooksList::item:selected, QListWidget#entriesList::item:selected {
        background-color: #6366f1;
        color: white;
        font-weight: bold;
        border-bottom: 1px solid #4f46e5;
    }
    
    QListWidget#notebooksList::item:hover, QListWidget#entriesList::item:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #374151, stop: 1 #1f2937);
        color: #f9fafb;
        border-bottom: 1px solid #4c1d95;
    }
    
    QListWidget#notebooksList::item:last {
        border-bottom: none;
    }
    
    QListWidget#entriesList::item:last {
        border-bottom: none;
    }
    
    /* Generic List Widgets */
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
        background-color: #0d0d0d;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }
    
    /* Formatting Toolbar */
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
        padding: 6px 10px;
        font-weight: bold;
    }
    
    QPushButton[class="formatting"]:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        font-weight: 900;
        font-size: 15px;     /* enlarge */
        padding: 8px 12px;   /* enlarge */
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
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        border: 2px solid #7c3aed;
        font-size: 15px;
        padding: 8px 12px;
    }
    
    QPushButton[class="formatting"]:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #312e81, stop: 1 #1e1b4b);
        color: #ffffff;
        font-size: 14px;
        padding: 6px 10px;
    }
    
    /* Storage Section - Full Width */
    QFrame#storageSection {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #1f2937, stop: 1 #111827);
        border: none;
        border-top: 1px solid #374151;
        border-radius: 0;
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
    
    /* Combo Boxes */
    QComboBox {
        background-color: #404040;
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 6px 12px;
        min-width: 100px;
    }
    
    QComboBox:hover {
        border: 2px solid #7c3aed;  /* purple border on hover */
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        color: #ffffff;
        padding: 8px 14px; /* enlarge slightly */
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
    
    /* Spin Boxes */
    QSpinBox {
        background-color: #404040;
        color: #e0e0e0;
        border: 2px solid #555555;
        border-radius: 6px;
        padding: 6px;
        min-width: 60px;
    }
    
    QSpinBox:hover {
        border: 2px solid #7c3aed;
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764);
        color: #ffffff;
        padding: 8px;  /* enlarge */
    }
    
    QSpinBox:focus {
        border-color: #6366f1;
        background-color: #505050;
    }
    
    QSpinBox::up-button, QSpinBox::down-button {
        background-color: #555555;
        border: none;
        width: 16px;
    }
    
    QSpinBox::up-button:hover, QSpinBox::down-button:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* purple on hover */
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
    }
    
    QMenu::item:selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        color: #ffffff;
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
    }
    
    QMessageBox QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple hover */
        border: 2px solid #7c3aed;
        color: #ffffff;
        padding: 10px 22px; /* enlarge */
    }
    
    QMessageBox QPushButton:pressed {
        background-color: #312e81;
        color: #ffffff;
        padding: 8px 20px;
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
    }
    
    QTabBar::tab:selected {
        background-color: #6366f1;
        color: #ffffff;
        border-color: #4f46e5;
    }
    
    QTabBar::tab:hover:!selected {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        border: 2px solid #7c3aed;
        color: #ffffff;
        padding: 10px 18px; /* enlarge */
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
    }
    
    QSlider::handle:horizontal:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #4c1d95, stop: 1 #3b0764); /* dark purple */
        border: 1px solid #7c3aed;
        width: 20px;  /* subtle enlarge */
        margin: -8px 0;
    }
    
    QSlider::handle:horizontal:pressed {
        background: #4f46e5;
        width: 18px;
        margin: -7px 0;
    }
    """