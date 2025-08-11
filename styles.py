def get_app_stylesheet():
    """Dark mode stylesheet with modern design and improved button hover effects"""
    return """
        /* Main Window */
        QMainWindow {
            background-color: #1a1a1a;
            color: #e0e0e0;
        }
        
        /* Generic Frame Styling */
        QFrame {
            background-color: #2b2b2b;
            border: 1px solid #404040;
            border-radius: 8px;
            color: #e0e0e0;
        }
        
        /* Left Panel Specific */
        QFrame#leftPanel {
            background-color: #252525;
            border: 1px solid #404040;
            border-radius: 8px;
        }
        
        /* Formatting Toolbar */
        QFrame#formattingToolbar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #3a3a3a, stop: 1 #2b2b2b);
            border: none;
            border-bottom: 1px solid #404040;
            border-radius: 0;
        }
        
        /* Writing Container */
        QFrame#writingContainer {
            background-color: #1e1e1e;
            border: 1px solid #404040;
            border-radius: 8px;
        }
        
        /* Storage Section */
        QFrame#storageSection {
            background-color: #2a2a2a;
            border: 1px solid #404040;
            border-radius: 6px;
        }
        
        /* Labels */
        QLabel {
            color: #e0e0e0;
            background: transparent;
            border: none;
        }
        
        QLabel#sectionHeader {
            color: #c7d2fe;
            font-weight: bold;
            font-size: 14px;
            background: transparent;
        }
        
        QLabel#dateLabel {
            color: #9ca3af;
            background: transparent;
        }
        
        QLabel#countLabel {
            color: #9ca3af;
            background: transparent;
        }
        
        QLabel#saveStatus {
            background: transparent;
        }
        
        QLabel#saveStatus[saved="true"] {
            color: #4ade80;
            font-weight: bold;
        }
        
        QLabel#saveStatus[saved="false"] {
            color: #f87171;
            font-weight: bold;
        }
        
        QLabel#storageInfo {
            color: #888888;
            background: transparent;
            font-size: 9px;
        }
        
        /* Buttons - Enhanced with better hover effects */
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #404040, stop: 1 #2b2b2b);
            color: #e0e0e0;
            border: 2px solid #555555;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            font-size: 11px;
        }
        
        QPushButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #505050, stop: 1 #3a3a3a);
            border: 2px solid #6366f1;
            color: #c7d2fe;
            transform: translateY(-1px);
        }
        
        QPushButton:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #6366f1, stop: 1 #4f46e5);
            color: #ffffff;
            border: 2px solid #4f46e5;
            transform: translateY(1px);
        }
        
        /* Save Button - Green with better hover */
        QPushButton[text="Save"] {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #10b981, stop: 1 #059669);
            color: #ffffff;
            border: 2px solid #059669;
            border-radius: 6px;
            font-weight: bold;
        }
        
        QPushButton[text="Save"]:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #34d399, stop: 1 #10b981);
            border: 2px solid #10b981;
            color: #ffffff;
            transform: translateY(-1px);
        }
        
        QPushButton[text="Save"]:pressed {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #059669, stop: 1 #047857);
            border: 2px solid #047857;
            transform: translateY(1px);
        }
        
        /* Special Button Styles */
        QPushButton#roundButton {
            background-color: #6366f1;
            color: #ffffff;
            border: 2px solid #6366f1;
            border-radius: 11px;
            padding: 0;
            font-weight: bold;
        }
        
        QPushButton#roundButton:hover {
            background-color: #5b21b6;
            border: 2px solid #5b21b6;
            transform: scale(1.05);
        }
        
        QPushButton#roundButton:pressed {
            background-color: #4c1d95;
            border: 2px solid #4c1d95;
            transform: scale(0.95);
        }
        
        QPushButton#toggleButton {
            background-color: #3a3a3a;
            color: #b0b0b0;
            border: 2px solid #555555;
            border-radius: 14px;
            padding: 0;
        }
        
        QPushButton#toggleButton:hover {
            background-color: #4a4a4a;
            color: #e0e0e0;
            border: 2px solid #6366f1;
            transform: scale(1.05);
        }
        
        QPushButton#lockButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #ef4444, stop: 1 #dc2626);
            color: #ffffff;
            border: 2px solid #dc2626;
            border-radius: 6px;
            font-weight: bold;
        }
        
        QPushButton#lockButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #dc2626, stop: 1 #b91c1c);
            border: 2px solid #b91c1c;
            transform: translateY(-1px);
        }
        
        QPushButton#deleteButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #f87171, stop: 1 #ef4444);
            color: #ffffff;
            border: 2px solid #ef4444;
        }
        
        QPushButton#deleteButton:hover {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #ef4444, stop: 1 #dc2626);
            border: 2px solid #dc2626;
            transform: translateY(-1px);
        }
        
        /* Formatting Toolbar Buttons - Enhanced */
        QPushButton[class="formatting"] {
            background-color: #3a3a3a;
            color: #e0e0e0;
            border: 2px solid #555555;
            border-radius: 4px;
            padding: 6px;
            margin: 1px;
        }
        
        QPushButton[class="formatting"]:hover {
            background-color: #4a4a4a;
            border: 2px solid #6366f1;
            color: #c7d2fe;
            transform: translateY(-1px);
        }
        
        QPushButton[class="formatting"]:checked {
            background-color: #6366f1;
            color: #ffffff;
            border: 2px solid #6366f1;
            transform: translateY(-1px);
        }
        
        QPushButton[class="formatting"]:pressed {
            background-color: #4f46e5;
            color: #ffffff;
            border: 2px solid #4f46e5;
            transform: translateY(1px);
        }
        
        /* Line Edits */
        QLineEdit {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #555555;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
        }
        
        QLineEdit:focus {
            border-color: #6366f1;
            outline: none;
            background-color: #333333;
        }
        
        QLineEdit#entryTitle {
            background-color: transparent;
            border: none;
            border-bottom: 2px solid #555555;
            border-radius: 0;
            padding: 8px 0;
            font-size: 18px;
            font-weight: bold;
            color: #f3f4f6;
        }
        
        QLineEdit#entryTitle:focus {
            border-bottom: 2px solid #6366f1;
            background-color: transparent;
        }
        
        QLineEdit::placeholder {
            color: #6b7280;
        }
        
        /* Text Edit */
        QTextEdit {
            background-color: #1e1e1e;
            color: #e0e0e0;
            border: none;
            padding: 10px;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.5;
            selection-background-color: #4f46e5;
            selection-color: #ffffff;
        }
        
        QTextEdit:focus {
            border: none;
            outline: none;
            background-color: #1e1e1e;
        }
        
        QTextEdit#mainEditor {
            background-color: #1e1e1e;
            border: none;
            color: #e0e0e0;
        }
        
        /* List Widgets */
        QListWidget {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #404040;
            border-radius: 8px;
            padding: 8px;
            outline: none;
        }
        
        QListWidget::item {
            background-color: #2b2b2b;
            border: none;
            border-bottom: 1px solid #404040;
            border-radius: 0;
            margin: 0;
            padding: 12px 16px;
            font-size: 11px;
            outline: none;
            color: #e0e0e0;
        }
        
        QListWidget::item:hover {
            background-color: #333333;
            border-left: 3px solid #6366f1;
            color: #f3f4f6;
        }
        
        QListWidget::item:selected {
            background-color: #374151;
            border-left: 4px solid #6366f1;
            color: #f9fafb;
            font-weight: 500;
            outline: none;
        }
        
        QListWidget::item:focus {
            outline: none;
            border-color: #6366f1;
        }
        
        /* Notebook List Specific */
        QListWidget#notebooksList::item {
            background-color: transparent;
            border: none;
            border-radius: 6px;
            padding: 10px 16px;
            margin: 2px 0;
            color: #d1d5db;
        }
        
        QListWidget#notebooksList::item:hover {
            background-color: rgba(99, 102, 241, 0.1);
            color: #c7d2fe;
            border-left: none;
        }
        
        QListWidget#notebooksList::item:selected {
            background-color: #6366f1;
            color: #ffffff;
            font-weight: bold;
            border-left: none;
        }
        
        /* Entry List Specific */
        QListWidget#entriesList::item {
            border: none;
            border-bottom: 1px solid #404040;
            padding: 16px 20px;
            margin: 0;
            background-color: #2b2b2b;
            color: #e0e0e0;
        }
        
        QListWidget#entriesList::item:hover {
            background-color: #333333;
            border-left: 3px solid #6366f1;
        }
        
        QListWidget#entriesList::item:selected {
            background-color: #374151;
            border-left: 4px solid #6366f1;
            color: #f9fafb;
            font-weight: 500;
        }
        
        /* Combo Boxes */
        QComboBox {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px 8px;
            min-height: 22px;
        }
        
        QComboBox:hover {
            border-color: #6366f1;
            background-color: #333333;
        }
        
        QComboBox:focus {
            border-color: #6366f1;
            background-color: #2b2b2b;
        }
        
        QComboBox::drop-down {
            border: none;
            background: transparent;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #9ca3af;
            margin-right: 4px;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #555555;
            selection-background-color: #6366f1;
            selection-color: #ffffff;
            outline: none;
        }
        
        /* Spin Boxes */
        QSpinBox {
            background-color: #2b2b2b;
            color: #e0e0e0;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px;
            min-height: 22px;
        }
        
        QSpinBox:hover {
            border-color: #6366f1;
            background-color: #333333;
        }
        
        QSpinBox:focus {
            border-color: #6366f1;
            background-color: #2b2b2b;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            background-color: #3a3a3a;
            border: 1px solid #555555;
            width: 16px;
            color: #e0e0e0;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background-color: #4a4a4a;
            border-color: #6366f1;
        }
        
        QSpinBox::up-arrow, QSpinBox::down-arrow {
            color: #9ca3af;
        }
        
        /* Scroll Bars */
        QScrollBar:vertical {
            background: #2b2b2b;
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555555;
            border-radius: 6px;
            min-height: 20px;
            margin: 2px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #6366f1;
        }
        
        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            border: none;
            background: none;
            height: 0;
        }
        
        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
        }
        
        QScrollBar:horizontal {
            background: #2b2b2b;
            height: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:horizontal {
            background-color: #555555;
            border-radius: 6px;
            min-width: 20px;
            margin: 2px;
        }
        
        QScrollBar::handle:horizontal:hover {
            background-color: #6366f1;
        }
        
        /* Splitters */
        QSplitter::handle {
            background-color: #404040;
        }
        
        QSplitter::handle:hover {
            background-color: #555555;
        }
        
        QSplitter::handle:vertical {
            height: 3px;
        }
        
        QSplitter::handle:horizontal {
            width: 3px;
        }
        
        /* Status Bar */
        QStatusBar {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #3a3a3a, stop: 1 #2b2b2b);
            border-top: 1px solid #404040;
            color: #9ca3af;
            font-size: 11px;
        }
        
        /* Tool Bar */
        QToolBar {
            background-color: #2b2b2b;
            border: none;
            spacing: 3px;
            padding: 5px;
            color: #e0e0e0;
        }
        
        QToolBar QToolButton {
            background-color: #3a3a3a;
            color: #e0e0e0;
            border: 1px solid #555555;
            border-radius: 4px;
            padding: 4px 8px;
        }
        
        QToolBar QToolButton:hover {
            background-color: #4a4a4a;
            border-color: #6366f1;
            color: #c7d2fe;
        }
        
        /* Progress Bar */
        QProgressBar {
            border: 2px solid #555555;
            border-radius: 5px;
            text-align: center;
            background-color: #2b2b2b;
            color: #e0e0e0;
        }
        
        QProgressBar::chunk {
            background-color: #6366f1;
            border-radius: 3px;
        }
        
        /* Separators */
        QFrame[frameShape="4"], QFrame[frameShape="5"] { 
            color: #555555;
            background-color: #555555;
            border: none;
        }
        
        /* Menu Styling */
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
            color: #e0e0e0;
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
            color: #e0e0e0;
        }
        
        QMenu::item:selected {
            background-color: #4a4a4a;
            color: #c7d2fe;
        }
    """