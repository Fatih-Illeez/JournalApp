# SecureJournal Pro

A secure, encrypted personal journaling application built with PyQt5 and cryptography.

## Features

- **End-to-End Encryption**: All entries are encrypted using Fernet (AES 128) encryption
- **Rich Text Editor**: Full formatting support with toolbar (bold, italic, underline, colors, fonts)
- **Multiple Notebooks**: Organize entries into separate notebooks
- **Auto-Save**: Automatic saving every 30 seconds
- **Date Organization**: Entries are organized by date folders
- **Export Functionality**: Export your journal to plain text
- **Dark Theme**: Modern dark UI with professional styling
- **Word/Character Count**: Real-time statistics
- **Calendar View**: Browse entries by date

## Installation

1. **Prerequisites**: Make sure you have Python 3.6+ installed

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python main.py
   ```

## File Structure

```
encrypted-journal/
├── main.py                 # Entry point
├── journal_app.py          # Main application class
├── auto_save_thread.py     # Auto-save background thread
├── calendar_dialog.py      # Calendar picker dialog
├── entry_manager.py        # Entry CRUD operations
├── journal_entry.py        # Entry data model
├── notebook_manager.py     # Notebook management
├── security_manager.py     # Encryption & security
├── settings_manager.py     # App configuration
├── styles.py              # UI styling
├── ui_components.py        # UI component creation
└── requirements.txt        # Python dependencies
```

## Security

- **Master Key**: A master encryption key is generated on first run and stored in `~/.encrypted_journal_pro/master.key`
- **Encrypted Storage**: All journal entries are encrypted before being saved to disk
- **No Plain Text**: Your entries are never stored in plain text
- **Secure Lock**: Use "Lock & Exit" to securely close the application

## Data Storage

Journal data is stored in your home directory:

- **Location**: `~/.encrypted_journal_pro/`
- **Structure**:
  - `master.key` - Encryption key (keep safe!)
  - `config.json` - Application settings
  - `notebooks/` - Custom notebooks
  - `YYYY-MM-DD/` - Daily entry folders

## Usage

1. **First Run**: The app will create encryption keys automatically
2. **Create Entry**: Click the "+" button next to Entries
3. **Write**: Use the rich text editor with formatting toolbar
4. **Save**: Entries auto-save or use Ctrl+S
5. **Organize**: Create notebooks to categorize entries
6. **Export**: Use the export function to backup your journal

## Keyboard Shortcuts

- **Ctrl+N**: New entry
- **Ctrl+S**: Save entry
- **Ctrl+Z**: Undo
- **Ctrl+Y**: Redo
- **Ctrl+B**: Bold
- **Ctrl+I**: Italic
- **Ctrl+U**: Underline

## Security Best Practices

1. **Backup your key**: The `master.key` file is crucial - back it up safely
2. **Use Lock & Exit**: Always use the lock button to close securely
3. **Keep software updated**: Regularly update dependencies
4. **Secure your system**: Use full disk encryption and strong passwords

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure all dependencies are installed
2. **Permission errors**: Check write permissions in home directory
3. **Corruption**: If entries won't load, check `~/.encrypted_journal_pro/` permissions

### Recovery

If you lose your encryption key, your entries cannot be recovered. Always backup:

- The entire `~/.encrypted_journal_pro/` folder
- Especially the `master.key` file

## Contributing

This is a personal project, but suggestions and bug reports are welcome!

## License

This project is for personal use. Please respect the privacy and security features.
