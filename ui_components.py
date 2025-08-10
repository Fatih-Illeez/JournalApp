from datetime import datetime
from PyQt5.QtWidgets import (
    QTextEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QListWidget, QFrame, QStatusBar, QToolBar, QAction, QLineEdit, QProgressBar,
    QSplitter, QWidget, QComboBox, QSpinBox, QColorDialog, QListWidgetItem
)
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QIcon
from PyQt5.QtCore import Qt


class UIComponents:
    def __init__(self, parent):
        self.parent = parent

    def create_left_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMinimumWidth(350)
        panel.setMaximumWidth(500)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📔 SecureJournal Pro")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Create a splitter for notebooks and entries
        self.parent.left_splitter = QSplitter(Qt.Vertical)
        
        # Notebooks section
        notebooks_widget = QWidget()
        notebooks_layout = QVBoxLayout(notebooks_widget)
        notebooks_layout.setContentsMargins(0, 0, 0, 0)
        notebooks_layout.setSpacing(5)
        
        # Notebooks header
        notebooks_header = QFrame()
        notebooks_header_layout = QHBoxLayout(notebooks_header)
        notebooks_header_layout.setContentsMargins(0, 0, 0, 0)
        
        notebooks_label = QLabel("Notebooks")
        notebooks_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.parent.new_notebook_btn = QPushButton("+")
        self.parent.new_notebook_btn.setMaximumSize(25, 25)
        self.parent.new_notebook_btn.setMinimumSize(25, 25)
        self.parent.new_notebook_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.parent.new_notebook_btn.clicked.connect(self.parent.create_notebook)
        
        notebooks_header_layout.addWidget(notebooks_label)
        notebooks_header_layout.addStretch()
        notebooks_header_layout.addWidget(self.parent.new_notebook_btn)
        
        # Notebooks list
        self.parent.notebooks_list = QListWidget()
        self.parent.notebooks_list.setMinimumHeight(80)
        
        notebooks_layout.addWidget(notebooks_header)
        notebooks_layout.addWidget(self.parent.notebooks_list)
        
        # Entries section
        entries_widget = QWidget()
        entries_layout = QVBoxLayout(entries_widget)
        entries_layout.setContentsMargins(0, 0, 0, 0)
        entries_layout.setSpacing(5)
        
        # Entries header
        entries_header = QFrame()
        entries_header_layout = QHBoxLayout(entries_header)
        entries_header_layout.setContentsMargins(0, 0, 0, 0)
        
        entries_label = QLabel("Entries")
        entries_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        
        self.parent.new_entry_btn = QPushButton("+")
        self.parent.new_entry_btn.setMaximumSize(25, 25)
        self.parent.new_entry_btn.setMinimumSize(25, 25)
        self.parent.new_entry_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        entries_header_layout.addWidget(entries_label)
        entries_header_layout.addStretch()
        entries_header_layout.addWidget(self.parent.new_entry_btn)
        
        # Entry list
        self.parent.entry_list = QListWidget()
        self.parent.entry_list.setMinimumHeight(200)
        
        entries_layout.addWidget(entries_header)
        entries_layout.addWidget(self.parent.entry_list)
        
        # Add widgets to splitter
        self.parent.left_splitter.addWidget(notebooks_widget)
        self.parent.left_splitter.addWidget(entries_widget)
        
        # Set initial splitter proportions (notebooks smaller, entries larger)
        self.parent.left_splitter.setSizes([120, 400])
        self.parent.left_splitter.setCollapsible(0, False)
        self.parent.left_splitter.setCollapsible(1, False)
        
        layout.addWidget(self.parent.left_splitter)
        
        # Storage info section
        storage_frame = QFrame()
        storage_layout = QVBoxLayout(storage_frame)
        storage_layout.setContentsMargins(5, 5, 5, 5)
        
        storage_label = QLabel("🔒 Secure Storage")
        storage_label.setFont(QFont("Segoe UI", 10, QFont.Bold))
        storage_label.setAlignment(Qt.AlignCenter)
        
        self.parent.storage_info_label = QLabel("Files: 0 • Size: 0 MB")
        self.parent.storage_info_label.setFont(QFont("Segoe UI", 8))
        self.parent.storage_info_label.setAlignment(Qt.AlignCenter)
        self.parent.storage_info_label.setStyleSheet("color: #888;")
        
        storage_layout.addWidget(storage_label)
        storage_layout.addWidget(self.parent.storage_info_label)
        layout.addWidget(storage_frame)
        
        # Bottom lock button
        self.parent.lock_btn = QPushButton("🔒 Lock & Exit")
        self.parent.lock_btn.setMinimumHeight(40)
        self.parent.lock_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(self.parent.lock_btn)
        
        # Connect events
        self.parent.new_notebook_btn.clicked.connect(self.parent.create_notebook)
        self.parent.notebooks_list.itemClicked.connect(self.parent.select_notebook)
        self.parent.new_entry_btn.clicked.connect(self.parent.new_entry)
        self.parent.entry_list.itemClicked.connect(self.parent.load_selected_entry)
        self.parent.lock_btn.clicked.connect(self.parent.lock_and_exit)
        
        # Load notebooks
        self.parent.load_notebooks()
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(0)
        
        # Word-like formatting toolbar
        formatting_toolbar = self.create_formatting_toolbar()
        layout.addWidget(formatting_toolbar)
        
        # Single writing container for both title and editor
        writing_container = QFrame()
        writing_container.setObjectName("writingContainer")
        container_layout = QVBoxLayout(writing_container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(10)
        
        # Title section with toggle button
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        # Toggle button on the left
        self.parent.toggle_btn = QPushButton("◀")
        self.parent.toggle_btn.setMaximumSize(25, 25)
        self.parent.toggle_btn.setMinimumSize(25, 25)
        self.parent.toggle_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.parent.toggle_btn.clicked.connect(self.parent.toggle_left_panel)
        
        self.parent.entry_title = QLineEdit()
        self.parent.entry_title.setPlaceholderText("Enter your entry title...")
        self.parent.entry_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.parent.entry_title.setMinimumHeight(45)
        self.parent.entry_title.setObjectName("entryTitle")
        
        title_layout.addWidget(self.parent.toggle_btn)
        title_layout.addWidget(self.parent.entry_title, 1)
        
        # Action buttons
        buttons_frame = QFrame()
        buttons_layout = QHBoxLayout(buttons_frame)
        buttons_layout.setContentsMargins(0, 0, 0, 0)
        buttons_layout.setSpacing(15)
        
        self.parent.save_btn = QPushButton("💾 Save")
        self.parent.save_btn.setMinimumSize(80, 35)
        self.parent.save_btn.setToolTip("Save Entry")
        
        self.parent.delete_btn = QPushButton("🗑️ Delete")
        self.parent.delete_btn.setMinimumSize(80, 35)
        self.parent.delete_btn.setToolTip("Delete Entry")
        
        self.parent.date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
        self.parent.date_label.setFont(QFont("Segoe UI", 12))
        self.parent.date_label.setAlignment(Qt.AlignCenter)
        self.parent.date_label.setMinimumWidth(120)
        
        buttons_layout.addWidget(self.parent.date_label)
        buttons_layout.addWidget(self.parent.save_btn)
        buttons_layout.addWidget(self.parent.delete_btn)
        
        title_layout.addWidget(buttons_frame)
        container_layout.addWidget(title_frame)
        
        # Editor - Use QTextEdit for rich text support
        self.parent.editor = QTextEdit()
        self.parent.editor.setFont(QFont("Segoe UI", self.parent.config["font_size"]))
        self.parent.editor.setPlaceholderText("Start writing your thoughts here...")
        self.parent.editor.setLineWrapMode(QTextEdit.WidgetWidth if self.parent.config["word_wrap"] else QTextEdit.NoWrap)
        self.parent.editor.setObjectName("mainEditor")
        self.parent.editor.setAcceptRichText(True)  # Enable rich text support for images
        container_layout.addWidget(self.parent.editor, 1)
        
        layout.addWidget(writing_container, 1)
        
        # Bottom info bar
        info_frame = QFrame()
        info_layout = QHBoxLayout(info_frame)
        info_layout.setContentsMargins(10, 10, 10, 5)
        
        self.parent.word_count_label = QLabel("Words: 0")
        self.parent.char_count_label = QLabel("Characters: 0")
        
        # Center container for word/char counts
        center_frame = QFrame()
        center_layout = QHBoxLayout(center_frame)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(20)
        center_layout.addWidget(self.parent.word_count_label)
        center_layout.addWidget(self.parent.char_count_label)
        
        self.parent.last_saved_label = QLabel("Unsaved")
        
        info_layout.addStretch()
        info_layout.addWidget(center_frame)
        info_layout.addStretch()
        info_layout.addWidget(self.parent.last_saved_label)
        
        layout.addWidget(info_frame)
        
        # Connect editor events
        self.parent.editor.textChanged.connect(self.parent.on_text_changed)
        self.parent.entry_title.textChanged.connect(self.parent.on_title_changed)
        self.parent.save_btn.clicked.connect(self.parent.save_entry)
        self.parent.delete_btn.clicked.connect(self.parent.delete_entry)
        
        return panel
    
    def create_status_bar(self):
        self.parent.status_bar = QStatusBar()
        self.parent.setStatusBar(self.parent.status_bar)
        
        self.parent.status_bar.showMessage("Ready to write...")
        
        # Add progress bar for operations
        self.parent.progress_bar = QProgressBar()
        self.parent.progress_bar.setVisible(False)
        self.parent.progress_bar.setMaximumWidth(200)
        self.parent.status_bar.addPermanentWidget(self.parent.progress_bar)
    
    def create_toolbar(self):
        toolbar = QToolBar()
        self.parent.addToolBar(toolbar)
        
        # Font size actions with white text
        decrease_font = QAction("A-", self.parent)
        decrease_font.triggered.connect(self.parent.decrease_font_size)
        toolbar.addAction(decrease_font)
        
        increase_font = QAction("A+", self.parent)
        increase_font.triggered.connect(self.parent.increase_font_size)
        toolbar.addAction(increase_font)
        
        toolbar.addSeparator()
        
        # Word wrap toggle
        word_wrap = QAction("Word Wrap", self.parent)
        word_wrap.setCheckable(True)
        word_wrap.setChecked(self.parent.config["word_wrap"])
        word_wrap.triggered.connect(self.parent.toggle_word_wrap)
        toolbar.addAction(word_wrap)
        
        toolbar.addSeparator()
        
        # Storage management actions
        storage_stats = QAction("Storage Stats", self.parent)
        storage_stats.triggered.connect(self.parent.show_storage_stats)
        toolbar.addAction(storage_stats)
        
        cleanup_storage = QAction("Cleanup Storage", self.parent)
        cleanup_storage.triggered.connect(self.parent.cleanup_storage)
        toolbar.addAction(cleanup_storage)
        
        # Style the toolbar actions to have white text
        toolbar.setStyleSheet("""
            QToolBar {
                background-color: #2d2d2d;
                border: none;
                spacing: 3px;
                padding: 5px;
            }
            QToolBar QToolButton {
                color: #ffffff;
                background-color: #404040;
                border: 1px solid #555;
                border-radius: 4px;
                padding: 4px 8px;
                margin: 2px;
            }
            QToolBar QToolButton:hover {
                background-color: #4a4a4a;
                border-color: #6b7280;
            }
            QToolBar QToolButton:pressed {
                background-color: #333;
            }
            QToolBar QToolButton:checked {
                background-color: #6b7280;
                border-color: #7c8590;
            }
        """)

    def create_formatting_toolbar(self):
        toolbar = QFrame()
        toolbar.setObjectName("formattingToolbar")
        toolbar.setMinimumHeight(50)
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(5)
        
        # Undo/Redo
        self.parent.undo_btn = QPushButton("↶")
        self.parent.undo_btn.setMinimumSize(30, 30)
        self.parent.undo_btn.setToolTip("Undo")
        self.parent.undo_btn.clicked.connect(lambda: self.parent.editor.undo())
        
        self.parent.redo_btn = QPushButton("↷")
        self.parent.redo_btn.setMinimumSize(30, 30)
        self.parent.redo_btn.setToolTip("Redo")
        self.parent.redo_btn.clicked.connect(lambda: self.parent.editor.redo())
        
        layout.addWidget(self.parent.undo_btn)
        layout.addWidget(self.parent.redo_btn)
        layout.addWidget(self.create_separator())
        
        # Font family
        self.parent.font_combo = QComboBox()
        self.parent.font_combo.setMinimumWidth(120)
        self.parent.font_combo.addItems(["Segoe UI", "Arial", "Times New Roman", "Calibri", "Verdana", "Georgia"])
        self.parent.font_combo.currentTextChanged.connect(self.parent.change_font_family)
        layout.addWidget(self.parent.font_combo)
        
        # Font size
        self.parent.font_size_spin = QSpinBox()
        self.parent.font_size_spin.setRange(8, 72)
        self.parent.font_size_spin.setValue(12)
        self.parent.font_size_spin.setMinimumWidth(60)
        self.parent.font_size_spin.valueChanged.connect(self.parent.change_font_size)
        layout.addWidget(self.parent.font_size_spin)
        
        layout.addWidget(self.create_separator())
        
        # Bold, Italic, Underline
        self.parent.bold_btn = QPushButton("B")
        self.parent.bold_btn.setMinimumSize(30, 30)
        self.parent.bold_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        self.parent.bold_btn.setCheckable(True)
        self.parent.bold_btn.setToolTip("Bold")
        self.parent.bold_btn.clicked.connect(self.parent.toggle_bold)
        
        self.parent.italic_btn = QPushButton("I")
        self.parent.italic_btn.setMinimumSize(30, 30)
        self.parent.italic_btn.setFont(QFont("Segoe UI", 10, 75, True))  # Italic
        self.parent.italic_btn.setCheckable(True)
        self.parent.italic_btn.setToolTip("Italic")
        self.parent.italic_btn.clicked.connect(self.parent.toggle_italic)
        
        self.parent.underline_btn = QPushButton("U")
        self.parent.underline_btn.setMinimumSize(30, 30)
        self.parent.underline_btn.setFont(QFont("Segoe UI", 10))
        self.parent.underline_btn.setCheckable(True)
        self.parent.underline_btn.setToolTip("Underline")
        self.parent.underline_btn.clicked.connect(self.parent.toggle_underline)
        
        layout.addWidget(self.parent.bold_btn)
        layout.addWidget(self.parent.italic_btn)
        layout.addWidget(self.parent.underline_btn)
        
        layout.addWidget(self.create_separator())
        
        # Lists
        self.parent.bullet_btn = QPushButton("•")
        self.parent.bullet_btn.setMinimumSize(30, 30)
        self.parent.bullet_btn.setToolTip("Bullet List")
        self.parent.bullet_btn.clicked.connect(self.parent.insert_bullet_list)
        
        self.parent.number_btn = QPushButton("1.")
        self.parent.number_btn.setMinimumSize(30, 30)
        self.parent.number_btn.setToolTip("Numbered List")
        self.parent.number_btn.clicked.connect(self.parent.insert_numbered_list)
        
        layout.addWidget(self.parent.bullet_btn)
        layout.addWidget(self.parent.number_btn)
        
        layout.addWidget(self.create_separator())
        
        # Colors
        self.parent.text_color_btn = QPushButton("A")
        self.parent.text_color_btn.setMinimumSize(30, 30)
        self.parent.text_color_btn.setToolTip("Text Color")
        self.parent.text_color_btn.clicked.connect(self.parent.change_text_color)
        
        self.parent.bg_color_btn = QPushButton("⬛")
        self.parent.bg_color_btn.setMinimumSize(30, 30)
        self.parent.bg_color_btn.setToolTip("Background Color")
        self.parent.bg_color_btn.clicked.connect(self.parent.change_background_color)
        
        layout.addWidget(self.parent.text_color_btn)
        layout.addWidget(self.parent.bg_color_btn)
        
        layout.addWidget(self.create_separator())
        
        # Image insertion
        self.parent.insert_image_btn = QPushButton("🖼️")
        self.parent.insert_image_btn.setMinimumSize(35, 30)
        self.parent.insert_image_btn.setToolTip("Insert Image")
        self.parent.insert_image_btn.clicked.connect(self.parent.insert_image)
        layout.addWidget(self.parent.insert_image_btn)
        
        layout.addStretch()
        
        return toolbar
    
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setMaximumHeight(25)
        return separator
    
    def update_storage_info(self, stats):
        """Update the storage information display"""
        try:
            files = stats.get("virtual_files", 0)
            size_mb = stats.get("total_size_mb", 0.0)
            self.parent.storage_info_label.setText(f"Files: {files} • Size: {size_mb} MB")
        except Exception:
            self.parent.storage_info_label.setText("Files: - • Size: - MB")
    
    def update_notebooks_with_counts(self, notebooks_data):
        """Update the notebooks list with entry counts"""
        self.parent.notebooks_list.clear()
        
        for notebook_info in notebooks_data:
            item = QListWidgetItem()
            notebook_name = notebook_info['name']
            entry_count = notebook_info['count']
            
            # Main notebook name in larger font
            main_text = notebook_name
            # Count in smaller, muted font
            count_text = f"  ({entry_count} entries)" if entry_count != 1 else f"  ({entry_count} entry)"
            
            # Set the main text
            item.setText(main_text + count_text)
            
            # Style the item to show count in smaller font
            item.setData(Qt.UserRole, notebook_name)  # Store actual name for selection
            self.parent.notebooks_list.addItem(item)
        
        # Select current notebook
        for i in range(self.parent.notebooks_list.count()):
            item = self.parent.notebooks_list.item(i)
            if item.data(Qt.UserRole) == self.parent.current_notebook:
                self.parent.notebooks_list.setCurrentRow(i)
                break