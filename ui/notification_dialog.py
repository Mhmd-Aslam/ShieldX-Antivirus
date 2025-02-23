# notification_dialog.py
from PySide6.QtWidgets import QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QLabel
from PySide6.QtCore import Qt

class NotificationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove title bar
        self.setFixedSize(300, 400)  # Small vertical rectangular size
        self.setStyleSheet(
            """
            QDialog {
                background-color: #2E3A48;
                border-radius: 20px;
                border: 1px solid #888;
            }
            QLabel {
                font-size: 14px;
                color: white;
            }
            QScrollArea {
                border: none;
            }
            QScrollBar:vertical {
                background: #1d2e4a;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4CAF50;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background: none;
            }
            """
        )

        # Layout for the notification dialog
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Close button at the top
        close_button = QPushButton("×")  # Close logo (X)
        close_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 40px;
                font-weight: bold;
                border: none;
                padding: -10px;
            }
            QPushButton:hover {
                color: #ff5555;
            }
            """
        )
        close_button.setFixedSize(30, 35)
        close_button.clicked.connect(self.close)

        # Add close button to the top-right corner
        close_button_layout = QHBoxLayout()
        close_button_layout.addStretch()
        close_button_layout.addWidget(close_button)
        layout.addLayout(close_button_layout)

        # Scrollable area for notifications
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        scroll_layout.setAlignment(Qt.AlignTop)

        # Add sample notifications
        notifications = [
            "No new threats detected.",
            "System scan completed successfully.",
            "Database updated to the latest version.",
            "Real-time protection is active.",
            "Threat detected: Malware 'Trojan.XYZ' quarantined.",
            "Scheduled scan started.",
            "System optimization completed.",
            "New update available for installation.",
        ]

        for notification in notifications:
            label = QLabel(notification)
            label.setStyleSheet("font-size: 14px; color: white; padding: 5px;")
            label.setWordWrap(True)
            scroll_layout.addWidget(label)

        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)