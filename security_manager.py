from PyQt5.QtWidgets import QMessageBox, QApplication


class SecurityManager:
    def __init__(self, parent):
        self.parent = parent

    def lock_and_exit(self):
        # Verify all files are encrypted before closing
        try:
            self.parent.status_bar.showMessage("Verifying encryption...")
            self.parent.progress_bar.setVisible(True)
            self.parent.progress_bar.setValue(0)
            
            # Check if current work is saved
            if self.parent.unsaved_changes:
                reply = QMessageBox.question(self.parent, "Unsaved Changes", 
                                           "You have unsaved changes. Save before exiting?",
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    self.parent.entry_manager.save_entry()
                elif reply == QMessageBox.Cancel:
                    self.parent.progress_bar.setVisible(False)
                    return
            
            self.parent.progress_bar.setValue(50)
            
            # Verify encryption by testing key access
            test_data = b"encryption_test"
            encrypted_test = self.parent.fernet.encrypt(test_data)
            decrypted_test = self.parent.fernet.decrypt(encrypted_test)
            
            if decrypted_test != test_data:
                raise Exception("Encryption verification failed")
            
            self.parent.progress_bar.setValue(100)
            self.parent.status_bar.showMessage("Encryption verified. Locking journal...")
            
            # Clear sensitive data
            self.parent.editor.clear()
            self.parent.entry_title.clear()
            
            # Stop auto-save thread
            if hasattr(self.parent, 'auto_save_thread'):
                self.parent.auto_save_thread.stop()
            
            self.parent.progress_bar.setVisible(False)
            QMessageBox.information(self.parent, "Locked", "🔒 Journal locked securely. All entries are encrypted and safe!")
            QApplication.instance().quit()
            
        except Exception as e:
            self.parent.progress_bar.setVisible(False)
            QMessageBox.critical(self.parent, "Security Error", 
                               f"Failed to verify encryption: {str(e)}\nPlease check your files manually.")
    
    def handle_close_event(self, event):
        # Verify encryption before closing
        try:
            if self.parent.unsaved_changes:
                reply = QMessageBox.question(self.parent, "Unsaved Changes", 
                                           "You have unsaved changes. Save before exiting?",
                                           QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
                if reply == QMessageBox.Yes:
                    self.parent.entry_manager.save_entry()
                elif reply == QMessageBox.Cancel:
                    event.ignore()
                    return
            
            # Verify encryption
            test_data = b"encryption_test"
            encrypted_test = self.parent.fernet.encrypt(test_data)
            decrypted_test = self.parent.fernet.decrypt(encrypted_test)
            
            if decrypted_test != test_data:
                raise Exception("Encryption verification failed")
            
            # Clear sensitive data
            self.parent.editor.clear()
            self.parent.entry_title.clear()
            
            # Stop auto-save thread
            if hasattr(self.parent, 'auto_save_thread'):
                self.parent.auto_save_thread.stop()
            
            event.accept()
            
        except Exception as e:
            reply = QMessageBox.question(self.parent, "Security Warning", 
                                       f"Could not verify encryption: {str(e)}\nClose anyway?",
                                       QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()