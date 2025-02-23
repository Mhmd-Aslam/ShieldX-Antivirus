# ui/pages/summary.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SummaryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Summary Page")
        layout.addWidget(label)
        self.setLayout(layout)