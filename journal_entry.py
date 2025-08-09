from datetime import datetime


class JournalEntry:
    def __init__(self, title, content, date, file_path=None):
        self.title = title
        self.content = content
        self.date = date
        self.file_path = file_path
        self.word_count = len(content.split()) if content else 0
        self.created_time = datetime.now().strftime("%H:%M")