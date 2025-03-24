from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QTableWidget, QTableWidgetItem,
    QHeaderView, QLineEdit, QPushButton, QComboBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QShowEvent
from db.models import MiscDB  # Import MiscDB class
from datetime import datetime  # For date and time formatting


class ScanHistoryPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # Page title
        title_label = QLabel("Scan History")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")  # Light blue for the title
        layout.addWidget(title_label)

        # Search and filter bar
        search_filter_layout = QHBoxLayout()
        search_filter_layout.setSpacing(10)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search by file name or threat...")
        self.search_bar.setStyleSheet(
            """
            QLineEdit {
                padding: 10px;
                border: 2px solid #3498DB;
                border-radius: 10px;
                font-size: 14px;
                color: #ECF0F1;
                background-color: #2C3E50;
            }
            QLineEdit:focus {
                border-color: #1ABC9C;
            }
            """
        )
        search_filter_layout.addWidget(self.search_bar)

        # Filter by scan type
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["All", "Quick Scan", "Full Scan", "Custom Scan", "Removable Scan"])
        self.filter_combo.setStyleSheet(
            """
            QComboBox {
                padding: 10px;
                border: 2px solid #3498DB;
                border-radius: 10px;
                font-size: 14px;
                color: #ECF0F1;
                background-color: #2C3E50;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 30px;
                border-left: 1px solid #3498DB;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #3498DB;
                selection-background-color: #1ABC9C;
                font-size: 14px;
                color: #ECF0F1;
                background-color: #2C3E50;
            }
            """
        )
        search_filter_layout.addWidget(self.filter_combo)

        # Search button
        search_button = QPushButton("Search")
        search_button.setStyleSheet(
            """
            QPushButton {
                background-color: #3498DB;
                color: #ECF0F1;
                padding: 10px 20px;
                border-radius: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
            """
        )
        search_button.clicked.connect(self.filter_table)
        search_filter_layout.addWidget(search_button)

        layout.addLayout(search_filter_layout)

        # Scan history table
        self.scan_table = QTableWidget()
        self.scan_table.setColumnCount(5)
        self.scan_table.setHorizontalHeaderLabels(["Scan Type", "Date", "Files Scanned", "Threats Detected", "Status"])
        self.scan_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.scan_table.setStyleSheet(
            """
            QTableWidget {
                background-color: #34495E;
                border: 2px solid #3498DB;
                border-radius: 10px;
                font-size: 14px;
                color: #ECF0F1;
            }
            QHeaderView::section {
                background-color: #3498DB;
                color: #ECF0F1;
                padding: 10px;
                font-size: 16px;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 10px;
            }
            """
        )
        self.scan_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table non-editable
        layout.addWidget(self.scan_table)

        # Populate the table with initial data
        self.populate_table()

    def init_timer(self):
        """Initialize a QTimer to refresh the table periodically."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.populate_table)
        self.timer.start(5000)  # Refresh every 5 seconds

    def populate_table(self):
        """Populate the table with scan history data from the database."""
        # Get scan history from database
        db = MiscDB()
        scan_history = db.get_history()

        if not scan_history:
            # If no history is available, show empty table
            self.scan_table.setRowCount(0)
            return

        # Sort the scan history by date in descending order (newest first)
        scan_history.sort(key=lambda x: datetime.strptime(x[1], "%Y-%m-%d %H:%M:%S.%f"), reverse=True)

        # Set the number of rows in the table
        self.scan_table.setRowCount(len(scan_history))

        # Populate the table with data
        for row, record in enumerate(scan_history):
            # Map database fields to table columns
            # record format: (id, date, files, threats, type)
            scan_type = record[4]  # type
            date = self.format_date_time(record[1])  # Format date and time
            files = str(record[2])  # files
            threats = str(record[3])  # threats
            status = "Completed"  # Default status

            # Create table items
            data = [scan_type, date, files, threats, status]
            for col, value in enumerate(data):
                item = QTableWidgetItem(value)
                item.setTextAlignment(Qt.AlignCenter)
                self.scan_table.setItem(row, col, item)

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

    def filter_table(self):
        """Filter the table based on search text and scan type."""
        search_text = self.search_bar.text().lower()
        filter_type = self.filter_combo.currentText()

        for row in range(self.scan_table.rowCount()):
            match = True
            if filter_type != "All":
                scan_type = self.scan_table.item(row, 0).text()
                if scan_type != filter_type:
                    match = False

            if match and search_text:
                file_name = self.scan_table.item(row, 1).text().lower()
                threat = self.scan_table.item(row, 3).text().lower()
                if search_text not in file_name and search_text not in threat:
                    match = False

            self.scan_table.setRowHidden(row, not match)

    def showEvent(self, event: QShowEvent):
        """Override showEvent to refresh data when the page becomes visible."""
        super().showEvent(event)
        # Refresh the table data every time the page is shown
        self.populate_table()