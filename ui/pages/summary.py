from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap, QFont, QShowEvent
from db.models import MiscDB
from datetime import datetime


class SummaryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_refresh_timer()
        self.init_ui()

    def setup_refresh_timer(self):
        """Initialize and configure the refresh timer"""
        self.refresh_timer = QTimer(self)
        self.refresh_timer.timeout.connect(self.refresh_page)
        self.refresh_timer.setInterval(5000)  # 5 second refresh interval

    def init_ui(self):
        """Initialize the user interface"""
        self.setup_main_layout()
        self.setup_title()
        self.setup_cards_section()
        self.setup_recent_scans_section()
        self.refresh_timer.start()

    def setup_main_layout(self):
        """Configure the main layout of the page"""
        if self.layout():
            self.clear_layout(self.layout())
        
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

    def setup_title(self):
        """Create and add the page title"""
        self.title_label = QLabel("Summary")
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        self.title_label.setStyleSheet("color: #ECF0F1;")
        self.main_layout.addWidget(self.title_label)

    def setup_cards_section(self):
        """Create the summary cards section"""
        self.cards_layout = QHBoxLayout()
        self.cards_layout.setSpacing(20)
        self.update_cards()
        self.main_layout.addLayout(self.cards_layout)

    def setup_recent_scans_section(self):
        """Create the recent scans section"""
        self.recent_scans_label = QLabel("Recent Scans")
        self.recent_scans_label.setFont(QFont("Arial", 18, QFont.Bold))
        self.recent_scans_label.setStyleSheet("color: #ECF0F1;")
        self.main_layout.addWidget(self.recent_scans_label)

        self.recent_scans_table_frame = QFrame()
        self.recent_scans_table_frame.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        self.table_layout = QVBoxLayout(self.recent_scans_table_frame)
        self.update_recent_scans_table()
        self.main_layout.addWidget(self.recent_scans_table_frame)

    def update_cards(self):
        """Update the summary cards with fresh data"""
        self.clear_layout(self.cards_layout)
        stats = self.get_summary_stats()

        cards_data = [
            ("Total Scans", "ui/logos/total_scans.png", str(stats['total_scans'])),
            ("Threats Detected", "ui/logos/threats.png", str(stats['total_threats'])),
            ("System Health", "ui/logos/system_health.png", f"{stats['system_health']}%")
        ]

        for title, icon_path, value in cards_data:
            card = self.create_card(title, icon_path, value)
            self.cards_layout.addWidget(card)

    def create_card(self, title, icon_path, value):
        """Create an individual summary card"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setAlignment(Qt.AlignCenter)

        # Icon
        icon = QLabel()
        icon.setPixmap(QPixmap(icon_path).scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        icon.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Value
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 20, QFont.Bold))
        value_label.setStyleSheet("color: #3498DB;")
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        return card

    def update_recent_scans_table(self):
        """Update the recent scans table with fresh data"""
        self.clear_layout(self.table_layout)
        
        # Headers
        headers = ["Scan Type", "Date", "Files Scanned", "Threats Detected", "Status"]
        headers_layout = QHBoxLayout()
        
        for header in headers:
            header_label = QLabel(header)
            header_label.setFont(QFont("Arial", 14, QFont.Bold))
            header_label.setStyleSheet("color: #3498DB;")
            header_label.setAlignment(Qt.AlignCenter)
            headers_layout.addWidget(header_label)
        
        self.table_layout.addLayout(headers_layout)

        # Data Rows
        db = MiscDB()
        scan_history = db.get_history()
        recent_scans = sorted(
            scan_history, 
            key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S.%f"), 
            reverse=True
        )[:3] if scan_history else []

        for scan in recent_scans:
            row_layout = QHBoxLayout()
            scan_data = [
                scan[4],  # Scan Type
                self.format_date_time(scan[1]),  # Date
                str(scan[2]),  # Files Scanned
                str(scan[3]),  # Threats Detected
                "Completed"  # Status
            ]
            
            for item in scan_data:
                item_label = QLabel(item)
                item_label.setFont(QFont("Arial", 12))
                item_label.setStyleSheet("color: #ECF0F1;")
                item_label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(item_label)
            
            self.table_layout.addLayout(row_layout)

        if not recent_scans:
            no_data_label = QLabel("No scan history available")
            no_data_label.setFont(QFont("Arial", 12))
            no_data_label.setStyleSheet("color: #ECF0F1;")
            no_data_label.setAlignment(Qt.AlignCenter)
            self.table_layout.addWidget(no_data_label)

    def get_summary_stats(self):
        """Calculate summary statistics from database"""
        db = MiscDB()
        scan_history = db.get_history()
        
        total_scans = len(scan_history)
        total_threats = sum(scan[3] for scan in scan_history)
        
        system_health = 100
        if total_scans > 0 and total_threats > 0:
            threat_ratio = total_threats / total_scans
            system_health = max(0, int(100 - (threat_ratio * 100)))
        
        return {
            'total_scans': total_scans,
            'total_threats': total_threats,
            'system_health': system_health
        }

    def format_date_time(self, timestamp):
        """Format timestamp for display"""
        try:
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            return dt.strftime("%d/%m/%Y %I:%M %p")
        except Exception as e:
            print(f"Error formatting date: {e}")
            return timestamp

    def clear_layout(self, layout):
        """Clear all widgets from a layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            elif item.layout():
                self.clear_layout(item.layout())

    def refresh_page(self):
        """Refresh all page content"""
        self.update_cards()
        self.update_recent_scans_table()

    def showEvent(self, event):
        """Handle page visibility"""
        super().showEvent(event)
        self.refresh_timer.start()
        self.refresh_page()

    def hideEvent(self, event):
        """Handle page hiding"""
        super().hideEvent(event)
        self.refresh_timer.stop()

    def closeEvent(self, event):
        """Handle window closing"""
        self.refresh_timer.stop()
        super().closeEvent(event)