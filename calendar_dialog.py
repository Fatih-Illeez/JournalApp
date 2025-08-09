from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCalendarWidget, QDialogButtonBox


class CalendarDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Date")
        self.setModal(True)
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                border: 1px solid #555;
            }
            QCalendarWidget QTableView {
                selection-background-color: #4a9eff;
                background-color: #333;
                color: #fff;
            }
        """)
        layout.addWidget(self.calendar)
        
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_selected_date(self):
        return self.calendar.selectedDate().toString("yyyy-MM-dd")