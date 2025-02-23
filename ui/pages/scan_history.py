# ui/pages/scan_history.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class ScanHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Scan History Page")
        layout.addWidget(label)
        self.setLayout(layout)