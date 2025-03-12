from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont

class SummaryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        # Page title
        title_label = QLabel("Summary")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")  # Light blue for the title
        layout.addWidget(title_label)

        # Cards layout
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(20)

        # Card 1: Total Scans
        total_scans_card = self.create_card("Total Scans", "ui/logos/total_scans.png", "150")
        cards_layout.addWidget(total_scans_card)

        # Card 2: Threats Detected
        threats_card = self.create_card("Threats Detected", "ui/logos/threats.png", "12")
        cards_layout.addWidget(threats_card)

        # Card 3: System Health
        system_health_card = self.create_card("System Health", "ui/logos/system_health.png", "95%")
        cards_layout.addWidget(system_health_card)

        layout.addLayout(cards_layout)

        # Recent Scans Section
        recent_scans_label = QLabel("Recent Scans")
        recent_scans_label.setFont(QFont("Arial", 18, QFont.Bold))
        recent_scans_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(recent_scans_label)

        # Recent Scans Table
        recent_scans_table = self.create_recent_scans_table()
        layout.addWidget(recent_scans_table)

    def create_card(self, title, icon_path, value):
        """Create a card with an icon, title, and value."""
        card = QFrame()
        card.setStyleSheet(
            """
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 20px;
            }
            """
        )
        card_layout = QVBoxLayout(card)
        card_layout.setAlignment(Qt.AlignCenter)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(icon_label)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")  # Light gray for text
        title_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setStyleSheet("color: #3498DB;")  # Light blue for value
        value_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(value_label)

        return card

    def create_recent_scans_table(self):
        """Create a table to display recent scans."""
        table = QFrame()
        table.setStyleSheet(
            """
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 20px;
            }
            """
        )
        table_layout = QVBoxLayout(table)

        # Table headers
        headers = ["Scan Type", "Date", "Files Scanned", "Threats Detected", "Status"]
        headers_layout = QHBoxLayout()
        for header in headers:
            header_label = QLabel(header)
            header_label.setFont(QFont("Arial", 14, QFont.Bold))
            header_label.setStyleSheet("color: #3498DB;")
            header_label.setAlignment(Qt.AlignCenter)
            headers_layout.addWidget(header_label)
        table_layout.addLayout(headers_layout)

        # Sample data
        recent_scans = [
            ["Quick Scan", "2023-10-01", "150", "0", "Completed"],
            ["Full Scan", "2023-10-02", "5000", "2", "Completed"],
            ["Custom Scan", "2023-10-03", "200", "1", "Completed"],
        ]

        # Add rows
        for scan in recent_scans:
            row_layout = QHBoxLayout()
            for item in scan:
                item_label = QLabel(item)
                item_label.setFont(QFont("Arial", 12))
                item_label.setStyleSheet("color: #ECF0F1;")
                item_label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(item_label)
            table_layout.addLayout(row_layout)

        return table