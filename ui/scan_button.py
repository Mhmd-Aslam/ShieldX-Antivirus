# scan_button.py
from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QSizePolicy  # Add QSizePolicy here
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

class ScanButton(QPushButton):
    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.name = name
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(180, 130)  # Keep the button size as per your requirement
        self.setStyleSheet(self.default_style())

        # Create a layout for the button
        button_layout = QVBoxLayout(self)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins to give more space
        button_layout.setSpacing(5)  # Add some spacing between the icon and the label

        # Add the icon
        self.icon_label = QLabel()
        icon_pixmap = QPixmap(self.icon_path).scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background-color: transparent;")  # Remove background color
        self.icon_label.setFixedSize(100, 100)  # Ensure the label has enough space for the icon
        button_layout.addWidget(self.icon_label)

        # Add the label
        self.text_label = QLabel(self.name)
        self.text_label.setStyleSheet("font-size: 16px; color: white; background-color: transparent;")  # Remove background color
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)  # Enable word wrapping for long text
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Allow the label to expand
        button_layout.addWidget(self.text_label)

    def default_style(self):
        return (
            "QPushButton {"
            "    border: 2px solid #888;"
            "    border-radius: 20px;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "    padding: 10px;"
            "    margin: 2px;"
            "}"
        )

    def enterEvent(self, event):
        self.setStyleSheet(
            "QPushButton {"
            "    background-color: #3B4A5A;"
            "    border: 2px solid #888;"
            "    border-radius: 20px;"
            "}"
        )
        self.icon_label.setStyleSheet("background-color: #3B4A5A;")
        self.text_label.setStyleSheet("font-size: 18px; color: white; background-color: #3B4A5A;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style())
        self.icon_label.setStyleSheet("background-color: #2E3A48;")
        self.text_label.setStyleSheet("font-size: 16px; color: white; background-color: #2E3A48;")
        super().leaveEvent(event)