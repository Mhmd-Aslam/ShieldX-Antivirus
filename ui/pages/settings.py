# ui/pages/settings.py
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        label = QLabel("Settings Page")
        layout.addWidget(label)
        self.setLayout(layout)