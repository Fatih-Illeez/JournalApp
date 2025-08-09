def get_app_stylesheet():
    return """
        QMainWindow {
            background-color: #1e1e1e;
            color: #ffffff;
        }
        
        QFrame {
            background-color: #2d2d2d;
            border: 1px solid #3e3e3e;
            border-radius: 8px;
        }
        
        QLabel {
            color: #ffffff;
            background: transparent;
            border: none;
        }
        
        QPushButton {
            background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,
                                       stop: 0 #6b7280, stop: 1 #4b5563);
            color: #ffffff;
            border: none;
            border-radius: 6px;
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
        
        QLineEdit {
            background-color: #3a3a3a;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 12px;
        }
        
        QLineEdit:focus {
            border-color: #6b7280;
            outline: none;
        }
        
        QLineEdit#entryTitle {
            background-color: #3a3a3a;
            border: none;
            border-bottom: 2px solid #555;
            border-radius: 0;
            padding: 8px 0;
        }
        
        QLineEdit#entryTitle:focus {
            border-bottom: 2px solid #6b7280;
        }
        
        QTextEdit {
            background-color: transparent;
            color: #ffffff;
            border: none;
            padding: 10px 0;
            font-family: 'Segoe UI', Arial, sans-serif;
            line-height: 1.5;
        }
        
        QTextEdit:focus {
            border: none;
            outline: none;
        }
        
        QTextEdit#mainEditor {
            background-color: transparent;
            border: none;
        }
        
        QFrame#writingContainer {
            background-color: #2a2a2a;
            border: 1px solid #444;
            border-radius: 8px;
        }
        
        QListWidget {
            background-color: #333;
            color: #ffffff;
            border: 1px solid #555;
            border-radius: 8px;
            padding: 8px;
        }
        
        QListWidget::item {
            background-color: #404040;
            border: 1px solid #555;
            border-radius: 6px;
            margin: 3px 0;
            padding: 12px;
            font-size: 11px;
        }
        
        QListWidget::item:hover {
            background-color: #4a4a4a;
            border-color: #6b7280;
        }
        
        QListWidget::item:selected {
            background-color: #6b7280;
            border-color: #7c8590;
        }
        
        QScrollBar:vertical {
            background-color: #2d2d2d;
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }
        
        QScrollBar::handle:vertical {
            background-color: #555;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #6b7280;
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
        
        QStatusBar {
            background-color: #252525;
            color: #cccccc;
            border-top: 1px solid #3e3e3e;
        }
        
        QToolBar {
            background-color: #2d2d2d;
            border: none;
            spacing: 3px;
            padding: 5px;
        }
        
        QProgressBar {
            border: 2px solid #555;
            border-radius: 5px;
            text-align: center;
            background-color: #333;
        }
        
        QProgressBar::chunk {
            background-color: #4a9eff;
            border-radius: 3px;
        }
    """