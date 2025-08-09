from PyQt5.QtCore import QThread, pyqtSignal


class AutoSaveThread(QThread):
    save_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.running = False
        
    def run(self):
        self.running = True
        while self.running:
            self.msleep(30000)  # Auto-save every 30 seconds
            if self.running:
                self.save_signal.emit()
    
    def stop(self):
        self.running = False
        self.quit()