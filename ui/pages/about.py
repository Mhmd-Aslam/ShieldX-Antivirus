# ui/pages/about.py
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap

class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        # Logo or Icon
        logo_label = QLabel()
        logo_pixmap = QPixmap("ui/logos/logo.png")  # Update path to logo
        logo_label.setPixmap(logo_pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Application Name
        app_name_label = QLabel("ShieldX Antivirus")
        app_name_label.setStyleSheet("font-size: 32px; font-weight: bold; color: #4CAF50;")
        layout.addWidget(app_name_label, alignment=Qt.AlignCenter)

        # Version
        version_label = QLabel("Version 1.0.0")
        version_label.setStyleSheet("font-size: 18px; color: #888;")
        layout.addWidget(version_label, alignment=Qt.AlignCenter)

        # About Our Antivirus
        about_antivirus_label = QLabel(
            "About Our Antivirus\n\n"
            "Our antivirus integrates Large Language Models (LLMs), vector embeddings, and AI-driven reasoning with static, dynamic, and memory-based analysis to detect and prevent even the most evasive malware—going beyond traditional signature-based security."
        )
        about_antivirus_label.setStyleSheet("font-size: 16px; color: #ccc;")
        about_antivirus_label.setAlignment(Qt.AlignCenter)
        about_antivirus_label.setWordWrap(True)
        layout.addWidget(about_antivirus_label)

        # What Makes Us Different?
        what_makes_different_label = QLabel("What Makes Us Different?")
        what_makes_different_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #4CAF50;")
        what_makes_different_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(what_makes_different_label)

        # Points
        points = [
            "✔ AI-Powered Threat Intelligence – Uses LLMs to break down file intent and detect sophisticated attacks.",
            "✔ Vector Embedding Technology – Identifies malware variants by analyzing deep structural similarities.",
            "✔ Memory & Behavior Analysis – Tracks real-time execution to detect stealthy, fileless threats.",
            "✔ Adaptive Heuristics – Learns from new threats, improving detection without constant updates.",
            "✔ Smart Quarantine & Forensics – Isolates threats instantly and provides AI-generated risk reports."
        ]
        for point in points:
            point_label = QLabel(point)
            point_label.setStyleSheet("font-size: 14px; color: #ccc;")
            point_label.setAlignment(Qt.AlignLeft)
            point_label.setWordWrap(False)  # Disable word wrap to keep text on one line
            layout.addWidget(point_label)

        # Closing Statement
        closing_label = QLabel(
            "With multi-layered, AI-driven security, our antivirus offers faster, smarter, and more proactive protection—without unnecessary system slowdowns."
        )
        closing_label.setStyleSheet("font-size: 16px; color: #ccc;")
        closing_label.setAlignment(Qt.AlignCenter)
        closing_label.setWordWrap(True)
        layout.addWidget(closing_label)

        # Developer Information
        developer_label = QLabel("Developed by ShieldX Technologies")
        developer_label.setStyleSheet("font-size: 14px; color: #888;")
        layout.addWidget(developer_label, alignment=Qt.AlignCenter)

        # Contact Information
        contact_label = QLabel("Contact: support@shieldx.com | Website: www.shieldx.com")
        contact_label.setStyleSheet("font-size: 14px; color: #888;")
        layout.addWidget(contact_label, alignment=Qt.AlignCenter)

        # Spacer
        layout.addStretch()

        self.setLayout(layout)