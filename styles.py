def get_app_stylesheet():
    """Return the main application stylesheet with enhanced dark theme"""
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
    
    /* Buttons */
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
    
    QPushButton:hover {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #505050, stop: 1 #3a3a3a);
        border: 2px solid #6366f1;
        color: #c7d2fe;
    }
    
    QPushButton:pressed {
        background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                   stop: 0 #6366f1, stop: 1 #4f46e5);
        color: #ffffff;
        border: 2px solid #4f46e5;
    }
    
    QPushButton:disabled {
        background-color: #2b2b2b;
        color: #666666;
        border: 2px solid #333333;
    }
    
    /* Tool Buttons */
    QToolButton {
        background-color: transparent;
        color: #e0e0e0;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 6px;
        margin: 1px;
    }
    
    QToolButton:hover {
        background-color: #404040;
        border: 1px solid #6366f1;
        color: #c7d2fe;
    }
    
    QToolButton:checked {
        background-color: #6366f1;
        color: white;
        border: 1px solid #4f46e5;
    }
    
    QToolButton:pressed {
        background-color: #4f46e5;
        color: white;
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
    }
    
    QListWidget::item:selected {
        background-color: #6366f1;
        color: white;
    }
    
    QListWidget::item:hover {
        background-color: #404040;
    }
    
    /* Frames */
    QFrame {
        background-color: #252525;
        border: 1px solid #404040;
        border-radius: 8px;
        color: #e0e0e0;
    }
    
    /* Labels */
    QLabel {
        background-color: transparent;
        color: #e0e0e0;
        border: none;
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
        border-color: #6366f1;
        background-color: #505050;
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
        border-color: #6366f1;
        background-color: #505050;
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
        background-color: #6366f1;
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
        background-color: #404040;
        color: #c7d2fe;
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
        background-color: #404040;
        color: #c7d2fe;
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
        background-color: #505050;
        border-color: #6366f1;
        color: #c7d2fe;
    }
    
    QMessageBox QPushButton:pressed {
        background-color: #6366f1;
        color: #ffffff;
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
        background-color: #505050;
        border-color: #6366f1;
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
        background: #8b5cf6;
    }
    
    QSlider::handle:horizontal:pressed {
        background: #4f46e5;
    }
    """


def get_notebook_item_stylesheet():
    """Return stylesheet for notebook list items"""
    return """
    QWidget {
        background-color: transparent;
        border-radius: 6px;
        padding: 8px;
    }
    QWidget:hover {
        background-color: #2a2a2a;
    }
    QLabel {
        background: transparent;
        border: none;
    }
    """