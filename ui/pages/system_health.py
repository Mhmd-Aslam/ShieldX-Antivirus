# ui/pages/system_health.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SystemHealthPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("System Health Page")
        layout.addWidget(label)
        self.setLayout(layout)