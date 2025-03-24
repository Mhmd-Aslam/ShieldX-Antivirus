from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QFont, QShowEvent
from db.models import MiscDB  # Import MiscDB class
from datetime import datetime  # For date and time formatting


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

        # Get summary stats from database
        stats = self.get_summary_stats()

        # Card 1: Total Scans
        total_scans_card = self.create_card("Total Scans", "ui/logos/total_scans.png", str(stats['total_scans']))
        cards_layout.addWidget(total_scans_card)

        # Card 2: Threats Detected
        threats_card = self.create_card("Threats Detected", "ui/logos/threats.png", str(stats['total_threats']))
        cards_layout.addWidget(threats_card)

        # Card 3: System Health
        system_health_card = self.create_card("System Health", "ui/logos/system_health.png", 
                                             f"{stats['system_health']}%")
        cards_layout.addWidget(system_health_card)

        layout.addLayout(cards_layout)

        # Recent Scans Section
        recent_scans_label = QLabel("Recent Scans")
        recent_scans_label.setFont(QFont("Arial", 18, QFont.Bold))
        recent_scans_label.setStyleSheet("color: #ECF0F1;")
        layout.addWidget(recent_scans_label)

        # Recent Scans Table
        self.recent_scans_table_frame = self.create_recent_scans_table()
        layout.addWidget(self.recent_scans_table_frame)
    
    def get_summary_stats(self):
        """Calculate summary statistics from the database"""
        db = MiscDB()
        scan_history = db.get_history()
        
        # Calculate statistics
        total_scans = len(scan_history)
        
        total_threats = 0
        for scan in scan_history:
            # Threats are in index 3 of the record
            total_threats += scan[3]
        
        # Simple system health calculation (just an example)
        # Higher is better, max 100%
        system_health = 100
        if total_scans > 0 and total_threats > 0:
            # Reduce health based on threat ratio
            threat_ratio = total_threats / total_scans
            system_health = max(0, int(100 - (threat_ratio * 100)))
        
        return {
            'total_scans': total_scans,
            'total_threats': total_threats,
            'system_health': system_health
        }

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

    def format_date_time(self, timestamp):
        """Format the timestamp into 'dd/mm/yyyy hr/min AM/PM' format."""
        try:
            # Parse the timestamp including microseconds
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
            # Format it as 'dd/mm/yyyy hr/min AM/PM'
            formatted_date = dt.strftime("%d/%m/%Y %I:%M %p")
            return formatted_date
        except Exception as e:
            print(f"Error formatting date: {e}")
            return timestamp  # Return the original timestamp if formatting fails

    def create_recent_scans_table(self):
        """Create a table to display recent scans."""
        table_frame = QFrame()
        table_frame.setStyleSheet(
            """
            QFrame {
                background-color: #2C3E50;
                border-radius: 10px;
                padding: 20px;
            }
            """
        )
        table_layout = QVBoxLayout(table_frame)

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

        # Get recent scans from database
        db = MiscDB()
        scan_history = db.get_history()
        
        # Limit to most recent 3 scans
        recent_scans = []
        if scan_history:
            recent_scans = sorted(scan_history, key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S.%f"), reverse=True)[:3]
        
        # Add rows
        for scan in recent_scans:
            row_layout = QHBoxLayout()
            
            # Format scan data for display
            scan_type = scan[4]  # type
            date = self.format_date_time(scan[1])  # Format date and time
            files = str(scan[2])  # files
            threats = str(scan[3])  # threats
            status = "Completed"  # Default status
            
            scan_data = [scan_type, date, files, threats, status]
            
            for item in scan_data:
                item_label = QLabel(item)
                item_label.setFont(QFont("Arial", 12))
                item_label.setStyleSheet("color: #ECF0F1;")
                item_label.setAlignment(Qt.AlignCenter)
                row_layout.addWidget(item_label)
            table_layout.addLayout(row_layout)
        
        # If no scans available, show message
        if not recent_scans:
            no_data_label = QLabel("No scan history available")
            no_data_label.setFont(QFont("Arial", 12))
            no_data_label.setStyleSheet("color: #ECF0F1;")
            no_data_label.setAlignment(Qt.AlignCenter)
            table_layout.addWidget(no_data_label)

        return table_frame
    
    def showEvent(self, event: QShowEvent):
        """Override showEvent to refresh data when the page becomes visible"""
        super().showEvent(event)
        # Refresh the page with latest data
        self.refresh_page()
        
    def refresh_page(self):
        """Refresh the page with latest data from database"""
        # Remove existing widgets
        layout = self.layout()
        
        # Reinitialize UI with fresh data
        self.init_ui()