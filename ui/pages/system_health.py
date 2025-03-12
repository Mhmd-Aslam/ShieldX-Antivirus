from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap

class SystemHealthPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)  # Add margins
        main_layout.setSpacing(20)  # Add spacing between widgets

        # Page title
        title_label = QLabel("System Health")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")  # Light gray for the title
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Overview of System Performance and Health Metrics")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #BDC3C7;")  # Light gray for subtitle
        main_layout.addWidget(subtitle_label)

        # Health metrics layout
        metrics_layout = QHBoxLayout()
        metrics_layout.setSpacing(20)

        # CPU Usage Card
        cpu_card = self.create_metric_card(
            "CPU Usage", "ui/logos/cpu_icon.png", 65, "#3498DB"
        )
        metrics_layout.addWidget(cpu_card)

        # Memory Usage Card
        memory_card = self.create_metric_card(
            "Memory Usage", "ui/logos/memory_icon.png", 45, "#E74C3C"
        )
        metrics_layout.addWidget(memory_card)

        # Disk Usage Card
        disk_card = self.create_metric_card(
            "Disk Usage", "ui/logos/disk_icon.png", 80, "#2ECC71"
        )
        metrics_layout.addWidget(disk_card)

        main_layout.addLayout(metrics_layout)

        # System Status Section
        status_label = QLabel("System Status")
        status_label.setFont(QFont("Arial", 18, QFont.Bold))
        status_label.setStyleSheet("color: #ECF0F1;")
        main_layout.addWidget(status_label)

        # Status cards
        status_layout = QHBoxLayout()
        status_layout.setSpacing(20)

        # Temperature Status
        temp_card = self.create_status_card(
            "Temperature", "ui/logos/temp_icon.png", "Normal", "#F1C40F"
        )
        status_layout.addWidget(temp_card)

        # Network Status
        network_card = self.create_status_card(
            "Network", "ui/logos/network_icon.png", "Stable", "#3498DB"
        )
        status_layout.addWidget(network_card)

        # Power Status
        power_card = self.create_status_card(
            "Power", "ui/logos/power_icon.png", "Optimal", "#2ECC71"
        )
        status_layout.addWidget(power_card)

        main_layout.addLayout(status_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def create_metric_card(self, title, icon_path, value, color):
        """Create a card for displaying a system metric."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #34495E;
                border-radius: 10px;
                padding: 15px;
            }}
            """
        )
        card_layout = QVBoxLayout(card)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio))
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setValue(value)
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: #2C3E50;
                border-radius: 5px;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
            """
        )
        card_layout.addWidget(progress_bar)

        # Value
        value_label = QLabel(f"{value}%")
        value_label.setFont(QFont("Arial", 12))
        value_label.setStyleSheet("color: #BDC3C7;")  # Light gray for text
        card_layout.addWidget(value_label, alignment=Qt.AlignCenter)

        return card

    def create_status_card(self, title, icon_path, status, color):
        """Create a card for displaying system status."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #34495E;
                border-radius: 10px;
                padding: 15px;
            }}
            """
        )
        card_layout = QVBoxLayout(card)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio))
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Status
        status_label = QLabel(status)
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(status_label, alignment=Qt.AlignCenter)

        return card