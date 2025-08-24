
# SecureJournal

SecureJournal is a privacy-first, fully encrypted journaling application built with PyQt5 and cryptography. It is designed for users who demand maximum security, local-only storage, and advanced organization features for their notes and images.

---

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

---

## Features

- **End-to-End Encryption**  
   All your notes and images are encrypted using the industry-standard Fernet (AES-128) encryption. Your data is never stored in plain text, and only you have access to the encryption key.

- **Self-Destruct Feature**  
   For maximum privacy, SecureJournal includes a self-destruct option. When triggered, this feature securely deletes all your encrypted data and keys, making recovery impossible. This is ideal for users who require absolute confidentiality.

- **Local-Only Storage**  
   All data is stored exclusively on your machine. Nothing is ever uploaded or synced to the cloud, ensuring your journal remains private and under your control.

- **Multiple Notebooks & Notes**  
   Organize your thoughts with unlimited notebooks. Each notebook can contain multiple notes, allowing for flexible categorization and easy retrieval.

- **Rich Text & Image Support**  
   Write with a full-featured rich text editor supporting bold, italic, underline, font size, color, and more. You can also insert images into your notes.

- **Image Rescale Support**  
   Easily resize images within your notes to fit your layout and preferences.

- **Export Functionality**  
   Export your entire journal, individual notebooks, or single notes to plain text or HTML for backup or sharing. Exports are always decrypted and readable.

- **Auto-Save**  
   Your work is automatically saved every 30 seconds, so you never lose progress.

- **Calendar & Date Organization**  
   Browse and organize entries by date using the built-in calendar view.

- **Word/Character Count**  
   Real-time statistics help you track your writing progress.

- **Modern Dark Theme**  
   Enjoy a beautiful, distraction-free dark UI.

---

## Security & Encryption

- **Encryption Details**:  
   SecureJournal uses Fernet symmetric encryption (AES-128 in CBC mode with HMAC authentication). Each note and image is encrypted before being written to disk. The encryption key is generated on first use and never leaves your device.

- **Key Storage**:  
   The master key is stored in your user directory in a protected file. Without this key, your data is cryptographically inaccessible.

- **Self-Destruct**:  
   The self-destruct feature securely deletes all encrypted data and the master key. This process is irreversible, ensuring that no one (not even you) can recover your journal after destruction.

- **No Cloud, No Tracking**:  
   SecureJournal does not connect to the internet, does not sync, and does not collect any analytics or telemetry.

---

## Data Storage

- **Location**:  
   All data is stored in a dedicated folder in your user directory (e.g., `~/.secure_journal/`).

- **Structure**:  
   - `master.key` — Your encryption key (do not lose this!)
   - `config.json` — Application settings
   - `notebooks/` — All your notebooks and notes, encrypted
   - `images/` — Encrypted images
   - `exports/` — Your exported, decrypted notes (if you use export)

---

## How to Use

1. **First Launch**:  
    The app generates a unique encryption key and sets up your secure environment.

2. **Creating Notebooks & Notes**:  
    Add new notebooks and notes using the intuitive sidebar and toolbar.

3. **Writing & Formatting**:  
    Use the rich text editor to write, format, and insert images.

4. **Image Handling**:  
    Drag and drop images or use the insert image button. Resize images as needed.

5. **Exporting**:  
    Use the export feature to save your notes or entire notebooks as plain text or HTML.

6. **Self-Destruct**:  
    Trigger the self-destruct from the settings menu if you need to permanently erase all data.

7. **Lock & Exit**:  
    Use the lock button to securely close the app and protect your data.

---

## Keyboard Shortcuts

- **Ctrl+N**: New note
- **Ctrl+S**: Save note
- **Ctrl+B/I/U**: Bold, Italic, Underline
- **Ctrl+E**: Export
- **Ctrl+L**: Lock & Exit

---

## Security Best Practices

- **Backup Your Key**:  
   The `master.key` file is essential. Back it up in a secure location.

- **No Recovery Without Key**:  
   If you lose your key, your data cannot be recovered.

- **Local Backups**:  
   Regularly export or backup your data folder for extra safety.

---

## Troubleshooting

- **Dependencies**:  
   Ensure all Python dependencies are installed (`pip install -r requirements.txt`).

- **Permissions**:  
   Make sure you have write access to your user directory.

- **Lost Key**:  
   Without your `master.key`, your data is unrecoverable.

---

## Contributing

Suggestions and bug reports are welcome! Please open an issue or pull request.

---

## License

This project is for personal use. All rights reserved. Respect user privacy and security.
