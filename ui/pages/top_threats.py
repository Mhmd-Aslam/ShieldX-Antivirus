from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from db.models import MiscDB

class TopThreatsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.threats_layout = None  # Store layout reference
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
        self.container = QWidget()
        scroll_area.setWidget(self.container)

        # Main layout for the container
        layout = QVBoxLayout(self.container)
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

        # Threats layout - store as class variable
        self.threats_layout = QVBoxLayout()
        self.threats_layout.setSpacing(15)
        layout.addLayout(self.threats_layout)

        # Set the scroll area as the main layout of the page
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)
        
        # Initial update
        self.update_threats()

    def update_threats(self):
        """Update threats from database and refresh the UI"""
        # Clear existing threat cards
        self.clear_threats()
        
        # Get threats from database
        db = MiscDB()
        threat_records = db.get_threats()
        
        # Format threat data from the database
        # threat_records format: (id, type, severity, description)
        threats = []
        for record in threat_records:
            threats.append({
                "name": record[1],  # type column
                "severity": record[2],  # severity column
                "description": record[3]  # description column
            })

        # Add threat cards
        for threat in threats:
            threat_card = self.create_threat_card(threat["name"], threat["severity"], threat["description"])
            self.threats_layout.addWidget(threat_card)
    
    def clear_threats(self):
        """Clear all threat cards from the layout"""
        if self.threats_layout:
            while self.threats_layout.count():
                item = self.threats_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
    
    def showEvent(self, event):
        """Override showEvent to update threats whenever page is shown"""
        self.update_threats()
        super().showEvent(event)

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