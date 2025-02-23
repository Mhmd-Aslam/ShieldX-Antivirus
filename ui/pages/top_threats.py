# ui/pages/top_threats.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class TopThreatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Top Threats Page")
        layout.addWidget(label)
        self.setLayout(layout)