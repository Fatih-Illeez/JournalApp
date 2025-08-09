from datetime import datetime
from PyQt5.QtWidgets import (
    QTextEdit, QPushButton, QLabel, QHBoxLayout, QVBoxLayout,
    QListWidget, QFrame, QStatusBar, QToolBar, QAction, QLineEdit, QProgressBar
)
from PyQt5.QtGui import QFont
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
        
        # Title with toggle button
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        self.parent.toggle_btn = QPushButton("◀")
        self.parent.toggle_btn.setMaximumSize(25, 25)
        self.parent.toggle_btn.setMinimumSize(25, 25)
        self.parent.toggle_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        
        title = QLabel("📔 SecureJournal Pro")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        
        title_layout.addWidget(self.parent.toggle_btn)
        title_layout.addWidget(title, 1)
        layout.addWidget(title_frame)
        
        # Notebooks section with integrated header
        notebooks_frame = QFrame()
        notebooks_layout = QVBoxLayout(notebooks_frame)
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
        self.parent.notebooks_list.setMaximumHeight(120)
        
        notebooks_layout.addWidget(notebooks_header)
        notebooks_layout.addWidget(self.parent.notebooks_list)
        layout.addWidget(notebooks_frame)
        
        # Entries section with integrated header
        entries_frame = QFrame()
        entries_layout = QVBoxLayout(entries_frame)
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
        self.parent.entry_list.setMinimumHeight(300)
        
        entries_layout.addWidget(entries_header)
        entries_layout.addWidget(self.parent.entry_list)
        layout.addWidget(entries_frame)
        
        # Bottom lock button
        self.parent.lock_btn = QPushButton("🔒 Lock & Exit")
        self.parent.lock_btn.setMinimumHeight(40)
        self.parent.lock_btn.setFont(QFont("Segoe UI", 10, QFont.Bold))
        layout.addWidget(self.parent.lock_btn)
        
        # Connect events
        self.parent.toggle_btn.clicked.connect(self.parent.toggle_left_panel)
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
        
        # Single writing container for both title and editor
        writing_container = QFrame()
        writing_container.setObjectName("writingContainer")
        container_layout = QVBoxLayout(writing_container)
        container_layout.setContentsMargins(15, 15, 15, 15)
        container_layout.setSpacing(10)
        
        # Title section
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        self.parent.entry_title = QLineEdit()
        self.parent.entry_title.setPlaceholderText("Enter your entry title...")
        self.parent.entry_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        self.parent.entry_title.setMinimumHeight(45)
        self.parent.entry_title.setObjectName("entryTitle")
        
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
        
        title_layout.addWidget(self.parent.entry_title, 1)
        title_layout.addWidget(buttons_frame)
        container_layout.addWidget(title_frame)
        
        # Editor
        self.parent.editor = QTextEdit()
        self.parent.editor.setFont(QFont("Segoe UI", self.parent.config["font_size"]))
        self.parent.editor.setPlaceholderText("Start writing your thoughts here...")
        self.parent.editor.setLineWrapMode(QTextEdit.WidgetWidth if self.parent.config["word_wrap"] else QTextEdit.NoWrap)
        self.parent.editor.setObjectName("mainEditor")
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
        
        # Font size actions
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