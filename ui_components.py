from datetime import datetime
from PyQt5.QtWidgets import (
    QTextEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QListWidget, QFrame, QStatusBar, QToolBar, QAction, QLineEdit, QProgressBar,
    QSplitter, QWidget, QComboBox, QSpinBox, QColorDialog, QListWidgetItem, QShortcut
)
from PyQt5.QtGui import QFont, QTextCharFormat, QColor, QIcon, QKeySequence
from PyQt5.QtCore import Qt


class UIComponents:
    def __init__(self, parent):
        self.parent = parent

    def create_left_panel(self):
        panel = QFrame()
        panel.setObjectName("leftPanel")
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setMinimumWidth(300)
        panel.setMaximumWidth(450)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Header section
        header_section = QFrame()
        header_section.setStyleSheet("background-color: #6366f1; border: none; border-radius: 0;")
        header_section.setFixedHeight(80)
        
        header_layout = QVBoxLayout(header_section)
        header_layout.setContentsMargins(20, 15, 20, 15)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # App title with Evernote-style elephant icon representation
        title = QLabel("🐘 SecureJournal")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #ffffff; background: transparent;")
        
        subtitle = QLabel("Your thoughts, secured")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: rgba(255, 255, 255, 0.8); background: transparent;")
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        layout.addWidget(header_section)
        
        # Main content area - Dark background
        content_area = QFrame()
        content_area.setStyleSheet("background-color: #252525; border: none;")
        content_layout = QVBoxLayout(content_area)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(20)
        
        # Create vertical splitter for notebooks and entries with enhanced functionality
        self.parent.left_splitter = QSplitter(Qt.Vertical)
        self.parent.left_splitter.setHandleWidth(8)  # Make handle more visible
        self.parent.left_splitter.setChildrenCollapsible(False)  # Prevent complete collapse
        
        # Notebooks section
        notebooks_widget = QWidget()
        notebooks_widget.setStyleSheet("background-color: #2b2b2b; border-radius: 8px;")
        notebooks_layout = QVBoxLayout(notebooks_widget)
        notebooks_layout.setContentsMargins(15, 15, 15, 15)
        notebooks_layout.setSpacing(8)
        
        # Notebooks header
        notebooks_header = QFrame()
        notebooks_header.setStyleSheet("background: transparent; border: none;")
        notebooks_header_layout = QHBoxLayout(notebooks_header)
        notebooks_header_layout.setContentsMargins(0, 0, 0, 10)
        
        notebooks_label = QLabel("NOTEBOOKS")
        notebooks_label.setObjectName("sectionHeader")
        notebooks_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        notebooks_label.setStyleSheet("color: #c7d2fe; background: transparent;")
        
        self.parent.new_notebook_btn = QPushButton("+")
        self.parent.new_notebook_btn.setObjectName("roundButton")
        self.parent.new_notebook_btn.setMaximumSize(28, 28)
        self.parent.new_notebook_btn.setMinimumSize(28, 28)
        self.parent.new_notebook_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        notebooks_header_layout.addWidget(notebooks_label)
        notebooks_header_layout.addStretch()
        notebooks_header_layout.addWidget(self.parent.new_notebook_btn)
        
        # Notebooks list
        self.parent.notebooks_list = QListWidget()
        self.parent.notebooks_list.setObjectName("notebooksList")
        self.parent.notebooks_list.setMinimumHeight(100)
        
        notebooks_layout.addWidget(notebooks_header)
        notebooks_layout.addWidget(self.parent.notebooks_list)
        
        # Entries section
        entries_widget = QWidget()
        entries_widget.setStyleSheet("background-color: #2b2b2b; border-radius: 8px;")
        entries_layout = QVBoxLayout(entries_widget)
        entries_layout.setContentsMargins(15, 15, 15, 15)
        entries_layout.setSpacing(8)
        
        # Entries header
        entries_header = QFrame()
        entries_header.setStyleSheet("background: transparent; border: none;")
        entries_header_layout = QHBoxLayout(entries_header)
        entries_header_layout.setContentsMargins(0, 0, 0, 10)
        
        entries_label = QLabel("NOTES")
        entries_label.setObjectName("sectionHeader")
        entries_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        entries_label.setStyleSheet("color: #c7d2fe; background: transparent;")
        
        self.parent.new_entry_btn = QPushButton("+")
        self.parent.new_entry_btn.setObjectName("roundButton")
        self.parent.new_entry_btn.setMaximumSize(28, 28)
        self.parent.new_entry_btn.setMinimumSize(28, 28)
        self.parent.new_entry_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        
        entries_header_layout.addWidget(entries_label)
        entries_header_layout.addStretch()
        entries_header_layout.addWidget(self.parent.new_entry_btn)
        
        # Entry list
        self.parent.entry_list = QListWidget()
        self.parent.entry_list.setObjectName("entriesList")
        self.parent.entry_list.setMinimumHeight(200)
        
        entries_layout.addWidget(entries_header)
        entries_layout.addWidget(self.parent.entry_list)
        
        # Add widgets to splitter with proper sizing
        self.parent.left_splitter.addWidget(notebooks_widget)
        self.parent.left_splitter.addWidget(entries_widget)
        
        # Configure splitter behavior - Fixed to work properly
        # Set minimum sizes to prevent complete collapse
        notebooks_widget.setMinimumHeight(150)
        entries_widget.setMinimumHeight(200)
        
        # Set initial sizes - notebooks smaller, entries larger
        self.parent.left_splitter.setSizes([180, 320])
        
        # Set stretch factors - notebooks don't stretch, entries do
        self.parent.left_splitter.setStretchFactor(0, 0)
        self.parent.left_splitter.setStretchFactor(1, 1)
        
        # Allow resizing but prevent complete collapse
        self.parent.left_splitter.setCollapsible(0, False)
        self.parent.left_splitter.setCollapsible(1, False)
        
        content_layout.addWidget(self.parent.left_splitter)
        
        # Storage info section
        storage_frame = QFrame()
        storage_frame.setObjectName("storageSection")
        storage_layout = QVBoxLayout(storage_frame)
        storage_layout.setContentsMargins(12, 10, 12, 10)
        storage_layout.setSpacing(4)
        
        storage_label = QLabel("SECURE STORAGE")
        storage_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
        storage_label.setStyleSheet("color: #9ca3af; background: transparent;")
        storage_label.setAlignment(Qt.AlignCenter)
        
        self.parent.storage_info_label = QLabel("0 files • 0 MB")
        self.parent.storage_info_label.setObjectName("storageInfo")
        self.parent.storage_info_label.setFont(QFont("Segoe UI", 9))
        self.parent.storage_info_label.setAlignment(Qt.AlignCenter)
        
        storage_layout.addWidget(storage_label)
        storage_layout.addWidget(self.parent.storage_info_label)
        content_layout.addWidget(storage_frame)
        
        # Bottom action button
        self.parent.lock_btn = QPushButton("🔒 Lock & Exit")
        self.parent.lock_btn.setObjectName("lockButton")
        self.parent.lock_btn.setMinimumHeight(45)
        self.parent.lock_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        content_layout.addWidget(self.parent.lock_btn)
        
        layout.addWidget(content_area, 1)
        
        # Connect events
        self.parent.new_notebook_btn.clicked.connect(self.parent.create_notebook)
        self.parent.notebooks_list.itemClicked.connect(self.parent.select_notebook)
        self.parent.new_entry_btn.clicked.connect(self.parent.new_entry)
        self.parent.entry_list.itemClicked.connect(self.parent.load_selected_entry)
        self.parent.lock_btn.clicked.connect(self.parent.lock_and_exit)
        
        return panel
    
    def create_right_panel(self):
        panel = QFrame()
        panel.setFrameStyle(QFrame.StyledPanel)
        panel.setStyleSheet("background-color: #1a1a1a; border: none;")
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Evernote-style formatting toolbar
        formatting_toolbar = self.create_formatting_toolbar()
        layout.addWidget(formatting_toolbar)
        
        # Main writing area
        writing_container = QFrame()
        writing_container.setObjectName("writingContainer")
        container_layout = QVBoxLayout(writing_container)
        container_layout.setContentsMargins(20, 20, 20, 15)
        container_layout.setSpacing(15)
        
        # Title and actions bar
        title_section = QFrame()
        title_section.setStyleSheet("background: transparent; border: none;")
        title_layout = QHBoxLayout(title_section)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(15)
        
        # Toggle button
        self.parent.toggle_btn = QPushButton("‹")
        self.parent.toggle_btn.setObjectName("toggleButton")
        self.parent.toggle_btn.setMaximumSize(32, 32)
        self.parent.toggle_btn.setMinimumSize(32, 32)
        self.parent.toggle_btn.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.parent.toggle_btn.clicked.connect(self.parent.toggle_left_panel)
        
        # Title input
        self.parent.entry_title = QLineEdit()
        self.parent.entry_title.setObjectName("entryTitle")
        self.parent.entry_title.setPlaceholderText("Untitled")
        self.parent.entry_title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        self.parent.entry_title.setMinimumHeight(50)
        
        # Action buttons section
        actions_section = QFrame()
        actions_section.setStyleSheet("background: transparent; border: none;")
        actions_layout = QHBoxLayout(actions_section)
        actions_layout.setContentsMargins(0, 0, 0, 0)
        actions_layout.setSpacing(10)
        
        # Date label
        self.parent.date_label = QLabel(datetime.now().strftime("%B %d, %Y"))
        self.parent.date_label.setObjectName("dateLabel")
        self.parent.date_label.setFont(QFont("Segoe UI", 11))
        
        # Action buttons
        self.parent.save_btn = QPushButton("Save")
        self.parent.save_btn.setMinimumSize(80, 36)
        self.parent.save_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        self.parent.delete_btn = QPushButton("Delete")
        self.parent.delete_btn.setObjectName("deleteButton")
        self.parent.delete_btn.setMinimumSize(80, 36)
        self.parent.delete_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        
        actions_layout.addWidget(self.parent.date_label)
        actions_layout.addStretch()
        actions_layout.addWidget(self.parent.save_btn)
        actions_layout.addWidget(self.parent.delete_btn)
        
        title_layout.addWidget(self.parent.toggle_btn)
        title_layout.addWidget(self.parent.entry_title, 1)
        title_layout.addWidget(actions_section)
        
        container_layout.addWidget(title_section)
        
        # Editor
        self.parent.editor = QTextEdit()
        self.parent.editor.setObjectName("mainEditor")
        self.parent.editor.setFont(QFont("Segoe UI", self.parent.config["font_size"]))
        self.parent.editor.setPlaceholderText("Start writing...")
        self.parent.editor.setLineWrapMode(QTextEdit.WidgetWidth if self.parent.config["word_wrap"] else QTextEdit.NoWrap)
        self.parent.editor.setAcceptRichText(True)
        
        # Add keyboard shortcut for image resizing
        resize_shortcut = QShortcut(QKeySequence("Ctrl+T"), self.parent.editor)
        resize_shortcut.activated.connect(self.parent.entry_manager.resize_selected_image)
        
        container_layout.addWidget(self.parent.editor, 1)
        layout.addWidget(writing_container, 1)
        
        # Bottom status bar - Dark theme
        status_section = QFrame()
        status_section.setStyleSheet("background-color: #2b2b2b; border-top: 1px solid #404040; border-radius: 0;")
        status_layout = QHBoxLayout(status_section)
        status_layout.setContentsMargins(20, 8, 20, 8)
        status_layout.setSpacing(20)
        
        # Word and character counts
        self.parent.word_count_label = QLabel("0 words")
        self.parent.word_count_label.setObjectName("countLabel")
        self.parent.word_count_label.setFont(QFont("Segoe UI", 10))
        
        self.parent.char_count_label = QLabel("0 characters")
        self.parent.char_count_label.setObjectName("countLabel")
        self.parent.char_count_label.setFont(QFont("Segoe UI", 10))
        
        # Save status
        self.parent.last_saved_label = QLabel("Not saved")
        self.parent.last_saved_label.setObjectName("saveStatus")
        self.parent.last_saved_label.setFont(QFont("Segoe UI", 10))
        
        # Image resize tip
        resize_tip_label = QLabel("Ctrl+T: Resize Image")
        resize_tip_label.setFont(QFont("Segoe UI", 9))
        resize_tip_label.setStyleSheet("color: #888888;")
        
        status_layout.addWidget(self.parent.word_count_label)
        status_layout.addWidget(self.parent.char_count_label)
        status_layout.addWidget(resize_tip_label)
        status_layout.addStretch()
        status_layout.addWidget(self.parent.last_saved_label)
        
        layout.addWidget(status_section)
        
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
        
        # Font size actions
        decrease_font = QAction("A−", self.parent)
        decrease_font.setToolTip("Decrease Font Size")
        decrease_font.triggered.connect(self.parent.decrease_font_size)
        toolbar.addAction(decrease_font)
        
        increase_font = QAction("A+", self.parent)
        increase_font.setToolTip("Increase Font Size")
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
        storage_stats = QAction("Storage Info", self.parent)
        storage_stats.setToolTip("View Storage Statistics")
        storage_stats.triggered.connect(self.parent.show_storage_stats)
        toolbar.addAction(storage_stats)
        
        cleanup_storage = QAction("Cleanup", self.parent)
        cleanup_storage.setToolTip("Cleanup Unused Files")
        cleanup_storage.triggered.connect(self.parent.cleanup_storage)
        toolbar.addAction(cleanup_storage)

    def create_formatting_toolbar(self):
        toolbar = QFrame()
        toolbar.setObjectName("formattingToolbar")
        toolbar.setFixedHeight(55)
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Undo/Redo - Enhanced visibility
        self.parent.undo_btn = QPushButton("⟲")
        self.parent.undo_btn.setProperty("class", "formatting")
        self.parent.undo_btn.setMinimumSize(36, 36)
        self.parent.undo_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.parent.undo_btn.setToolTip("Undo")
        self.parent.undo_btn.clicked.connect(lambda: self.parent.editor.undo())
        
        self.parent.redo_btn = QPushButton("⟳")
        self.parent.redo_btn.setProperty("class", "formatting")
        self.parent.redo_btn.setMinimumSize(36, 36)
        self.parent.redo_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.parent.redo_btn.setToolTip("Redo")
        self.parent.redo_btn.clicked.connect(lambda: self.parent.editor.redo())
        
        layout.addWidget(self.parent.undo_btn)
        layout.addWidget(self.parent.redo_btn)
        layout.addWidget(self.create_separator())
        
        # Font family dropdown
        self.parent.font_combo = QComboBox()
        self.parent.font_combo.setMinimumWidth(140)
        self.parent.font_combo.setMaximumWidth(140)
        self.parent.font_combo.addItems([
            "Segoe UI", "Arial", "Times New Roman", "Calibri", 
            "Verdana", "Georgia", "Helvetica Neue"
        ])
        self.parent.font_combo.currentTextChanged.connect(self.parent.change_font_family)
        layout.addWidget(self.parent.font_combo)
        
        # Font size spinner
        self.parent.font_size_spin = QSpinBox()
        self.parent.font_size_spin.setRange(8, 48)
        self.parent.font_size_spin.setValue(14)
        self.parent.font_size_spin.setMinimumWidth(60)
        self.parent.font_size_spin.setMaximumWidth(60)
        self.parent.font_size_spin.valueChanged.connect(self.parent.change_font_size)
        layout.addWidget(self.parent.font_size_spin)
        
        layout.addWidget(self.create_separator())
        
        # Text formatting buttons - Enhanced
        self.parent.bold_btn = QPushButton("B")
        self.parent.bold_btn.setProperty("class", "formatting")
        self.parent.bold_btn.setMinimumSize(36, 36)
        self.parent.bold_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.parent.bold_btn.setCheckable(True)
        self.parent.bold_btn.setToolTip("Bold")
        self.parent.bold_btn.clicked.connect(self.parent.toggle_bold)
        
        self.parent.italic_btn = QPushButton("I")
        self.parent.italic_btn.setProperty("class", "formatting")
        self.parent.italic_btn.setMinimumSize(36, 36)
        self.parent.italic_btn.setFont(QFont("Segoe UI", 14, QFont.Normal, True))
        self.parent.italic_btn.setCheckable(True)
        self.parent.italic_btn.setToolTip("Italic")
        self.parent.italic_btn.clicked.connect(self.parent.toggle_italic)
        
        self.parent.underline_btn = QPushButton("U")
        self.parent.underline_btn.setProperty("class", "formatting")
        self.parent.underline_btn.setMinimumSize(36, 36)
        self.parent.underline_btn.setFont(QFont("Segoe UI", 14, QFont.Normal))
        self.parent.underline_btn.setCheckable(True)
        self.parent.underline_btn.setToolTip("Underline")
        self.parent.underline_btn.clicked.connect(self.parent.toggle_underline)
        
        layout.addWidget(self.parent.bold_btn)
        layout.addWidget(self.parent.italic_btn)
        layout.addWidget(self.parent.underline_btn)
        
        layout.addWidget(self.create_separator())
        
        # List buttons - Enhanced
        self.parent.bullet_btn = QPushButton("• ‥")
        self.parent.bullet_btn.setProperty("class", "formatting")
        self.parent.bullet_btn.setMinimumSize(45, 36)
        self.parent.bullet_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.parent.bullet_btn.setToolTip("Bullet List")
        self.parent.bullet_btn.clicked.connect(self.parent.insert_bullet_list)
        
        self.parent.number_btn = QPushButton("1. 2.")
        self.parent.number_btn.setProperty("class", "formatting")
        self.parent.number_btn.setMinimumSize(45, 36)
        self.parent.number_btn.setFont(QFont("Segoe UI", 11, QFont.Bold))
        self.parent.number_btn.setToolTip("Numbered List")
        self.parent.number_btn.clicked.connect(self.parent.insert_numbered_list)
        
        layout.addWidget(self.parent.bullet_btn)
        layout.addWidget(self.parent.number_btn)
        
        layout.addWidget(self.create_separator())
        
        # Color buttons - Enhanced
        self.parent.text_color_btn = QPushButton("A")
        self.parent.text_color_btn.setProperty("class", "formatting")
        self.parent.text_color_btn.setMinimumSize(36, 36)
        self.parent.text_color_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.parent.text_color_btn.setToolTip("Text Color")
        self.parent.text_color_btn.clicked.connect(self.parent.change_text_color)
        
        self.parent.bg_color_btn = QPushButton("⬛")
        self.parent.bg_color_btn.setProperty("class", "formatting")
        self.parent.bg_color_btn.setMinimumSize(36, 36)
        self.parent.bg_color_btn.setFont(QFont("Segoe UI", 12))
        self.parent.bg_color_btn.setToolTip("Highlight Color")
        self.parent.bg_color_btn.clicked.connect(self.parent.change_background_color)
        
        layout.addWidget(self.parent.text_color_btn)
        layout.addWidget(self.parent.bg_color_btn)
        
        layout.addWidget(self.create_separator())
        
        # Media insertion - Enhanced
        self.parent.insert_image_btn = QPushButton("🖼")
        self.parent.insert_image_btn.setProperty("class", "formatting")
        self.parent.insert_image_btn.setMinimumSize(42, 36)
        self.parent.insert_image_btn.setFont(QFont("Segoe UI", 14))
        self.parent.insert_image_btn.setToolTip("Insert Image")
        self.parent.insert_image_btn.clicked.connect(self.parent.insert_image)
        layout.addWidget(self.parent.insert_image_btn)
        
        # Image resize button - NEW
        self.parent.resize_image_btn = QPushButton("📐")
        self.parent.resize_image_btn.setProperty("class", "formatting")
        self.parent.resize_image_btn.setMinimumSize(42, 36)
        self.parent.resize_image_btn.setFont(QFont("Segoe UI", 14))
        self.parent.resize_image_btn.setToolTip("Resize Selected Image (Ctrl+T)")
        self.parent.resize_image_btn.clicked.connect(self.parent.entry_manager.resize_selected_image)
        layout.addWidget(self.parent.resize_image_btn)
        
        # Spacer to push everything to the left
        layout.addStretch()
        
        return toolbar
    
    def create_separator(self):
        separator = QFrame()
        separator.setFrameShape(QFrame.VLine)
        separator.setFrameShadow(QFrame.Sunken)
        separator.setMaximumHeight(32)
        separator.setStyleSheet("color: #6b7280; background-color: #6b7280; margin: 4px;")
        return separator
    
    def update_storage_info(self, stats):
        """Update the storage information display"""
        try:
            files = stats.get("virtual_files", 0)
            size_mb = stats.get("total_size_mb", 0.0)
            
            # Format the display text
            if files == 0:
                display_text = "No files stored"
            elif files == 1:
                display_text = f"1 file • {size_mb} MB"
            else:
                display_text = f"{files} files • {size_mb} MB"
            
            self.parent.storage_info_label.setText(display_text)
        except Exception:
            self.parent.storage_info_label.setText("Storage info unavailable")
    
    def update_notebooks_with_counts(self, notebooks_data):
        """Update the notebooks list with entry counts"""
        self.parent.notebooks_list.clear()
        
        for notebook_info in notebooks_data:
            item = QListWidgetItem()
            notebook_name = notebook_info['name']
            entry_count = notebook_info['count']
            
            # Format the display text
            if entry_count == 0:
                display_text = f"{notebook_name}"
                subtitle = "Empty"
            elif entry_count == 1:
                display_text = f"{notebook_name}"
                subtitle = "1 note"
            else:
                display_text = f"{notebook_name}"
                subtitle = f"{entry_count} notes"
            
            # Create a rich text format for the item
            item_text = f"{display_text}\n{subtitle}"
            item.setText(item_text)
            
            # Store the actual notebook name for selection logic
            item.setData(Qt.UserRole, notebook_name)
            
            # Add special styling for the default notebook
            if notebook_name == "Default":
                item.setFont(QFont("Segoe UI", 11, QFont.Bold))
            else:
                item.setFont(QFont("Segoe UI", 11))
            
            self.parent.notebooks_list.addItem(item)
        
        # Select current notebook
        for i in range(self.parent.notebooks_list.count()):
            item = self.parent.notebooks_list.item(i)
            if item.data(Qt.UserRole) == self.parent.current_notebook:
                self.parent.notebooks_list.setCurrentRow(i)
                break