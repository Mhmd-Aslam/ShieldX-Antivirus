from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class TopThreatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Create a scroll area
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)  # Allow the widget to resize
        scroll_area.setStyleSheet(
            """
            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QScrollBar:vertical {
                background-color: #2C3E50;
                width: 12px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background-color: #091e36;
                min-height: 20px;
                border-radius: 6px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: none;
            }
            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: none;
            }
            """
        )

        # Create a container widget for the scroll area
        container = QWidget()
        scroll_area.setWidget(container)

        # Main layout for the container
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)  # Add margins
        layout.setSpacing(20)  # Add spacing between widgets

        # Page title
        title_label = QLabel("Top Threats")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #E74C3C;")  # Red for the title
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Most Critical Threats Detected")
        subtitle_label.setFont(QFont("Arial", 16))
        subtitle_label.setStyleSheet("color: #ECF0F1;")  # Light gray for text
        layout.addWidget(subtitle_label)

        # Threats layout
        threats_layout = QVBoxLayout()
        threats_layout.setSpacing(15)

        # Sample threats data
        threats = [
            {"name": "Trojan Horse", "severity": 90, "description": "A malicious program disguised as legitimate software."},
            {"name": "Ransomware", "severity": 85, "description": "Encrypts files and demands payment for decryption."},
            {"name": "Phishing Attack", "severity": 75, "description": "Attempts to steal sensitive information through fake emails."},
            {"name": "Spyware", "severity": 70, "description": "Secretly monitors user activity and collects data."},
            {"name": "Adware", "severity": 60, "description": "Displays unwanted advertisements and tracks user behavior."},
            {"name": "Worm", "severity": 80, "description": "Spreads across networks without user interaction."},
        ]

        # Add threat cards
        for threat in threats:
            threat_card = self.create_threat_card(threat["name"], threat["severity"], threat["description"])
            threats_layout.addWidget(threat_card)

        layout.addLayout(threats_layout)

        # Set the scroll area as the main layout of the page
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_threat_card(self, name, severity, description):
        """Create a card for a threat with a name, severity progress bar, and description."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 5px;
            }
            """
        )
        card_layout = QVBoxLayout(card)

        # Threat name
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 18, QFont.Bold))
        name_label.setStyleSheet("color: #E74C3C;")  # Red for threat name
        card_layout.addWidget(name_label)

        # Severity progress bar
        severity_bar = QProgressBar()
        severity_bar.setValue(severity)
        severity_bar.setTextVisible(False)
        severity_bar.setStyleSheet(
            """
            QProgressBar {
                background-color: #34495E;
                border-radius: 5px;
                height: 10px;
            }
            QProgressBar::chunk {
                background-color: #E74C3C;
                border-radius: 5px;
            }
            """
        )
        card_layout.addWidget(severity_bar)

        # Severity percentage
        severity_label = QLabel(f"Severity: {severity}%")
        severity_label.setFont(QFont("Arial", 12))
        severity_label.setStyleSheet("color: #ECF0F1;")  # Light gray for text
        card_layout.addWidget(severity_label)

        # Threat description
        description_label = QLabel(description)
        description_label.setFont(QFont("Arial", 12))
        description_label.setStyleSheet("color: #BDC3C7;")  # Light gray for description
        description_label.setWordWrap(True)
        card_layout.addWidget(description_label)

        return card