from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton
)
from PySide6.QtCore import Qt, QTimer, QTime
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

class ScanningPage(QWidget):
    def __init__(self, scan_type, scan_paths, parent=None):
        super().__init__(parent)
        self.scan_type = scan_type  # Type of scan (e.g., "Custom Scan")
        self.scan_paths = scan_paths  # List of files/directories to scan
        self.start_time = QTime.currentTime()  # Track the start time of the scan
        self.result_label = None  # Add a class-level variable for the result label
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)  # Add spacing between widgets

        # Top Bar Layout (Rescan Button + Header)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Rescan Button with Logo
        self.rescan_button = QPushButton()
        self.rescan_button.setIcon(QIcon("ui/logos/rescan.png"))  # Add rescan logo
        icon_size = QSize(50, 50)
        self.rescan_button.setIconSize(icon_size)
        self.rescan_button.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #3B4A5A;
                border-radius: 5px;
            }
            """
        )
        self.rescan_button.clicked.connect(self.rescan)  # Connect to rescan method
        top_bar_layout.addWidget(self.rescan_button)

        # Header Section
        header_layout = QHBoxLayout()
        header_layout.setAlignment(Qt.AlignCenter)

        # Add a scan icon
        scan_icon = QLabel()
        scan_icon.setPixmap(QPixmap("ui/logos/scanning.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        scan_icon.setStyleSheet("background-color: transparent;")
        header_layout.addWidget(scan_icon)

        # Add scan type and status
        self.scan_info_label = QLabel(f"{self.scan_type} in Progress...")
        self.scan_info_label.setStyleSheet(
            "font-size: 24px; font-weight: bold; color: white; background-color: transparent;"
        )
        header_layout.addWidget(self.scan_info_label)

        top_bar_layout.addLayout(header_layout)
        layout.addLayout(top_bar_layout)

        # Progress Bar with Animation and Percentage
        progress_layout = QHBoxLayout()
        progress_layout.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)  # Hide default text
        self.progress_bar.setStyleSheet(
            """
            QProgressBar {
                border: 2px solid #444;
                border-radius: 10px;
                background-color: #1d2e4a;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(
                    x1: 0, y1: 0, x2: 1, y2: 0,
                    stop: 0 #00b4ff, stop: 1 #0066ff
                );
                border-radius: 8px;
            }
            """
        )
        progress_layout.addWidget(self.progress_bar)

        # Progress Percentage Label
        self.progress_percentage_label = QLabel("0%")
        self.progress_percentage_label.setStyleSheet("font-size: 16px; color: white;")
        progress_layout.addWidget(self.progress_percentage_label)

        layout.addLayout(progress_layout)

        # Scan Details Section
        details_layout = QHBoxLayout()
        details_layout.setAlignment(Qt.AlignCenter)

        # Files Scanned
        self.files_scanned_label = QLabel("Files Scanned: 0")
        self.files_scanned_label.setStyleSheet("font-size: 16px; color: white;")
        details_layout.addWidget(self.files_scanned_label)

        # Threats Detected
        self.threats_detected_label = QLabel("Threats Detected: 0")
        self.threats_detected_label.setStyleSheet("font-size: 16px; color: white;")
        details_layout.addWidget(self.threats_detected_label)

        # Elapsed Time
        self.elapsed_time_label = QLabel("Elapsed Time: 00:00")
        self.elapsed_time_label.setStyleSheet("font-size: 16px; color: white;")
        details_layout.addWidget(self.elapsed_time_label)

        layout.addLayout(details_layout)

        # Scan Results Table
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(3)
        self.results_table.setHorizontalHeaderLabels(["File", "Status", "Threat"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.results_table.setStyleSheet(
            """
            QTableWidget {
                background-color: #1d2e4a;
                color: white;
                border: 2px solid #444;
                border-radius: 10px;
            }
            QHeaderView::section {
                background-color: #2E3A48;
                color: white;
                font-size: 16px;
                padding: 5px;
            }
            QTableWidget::item {
                padding: 5px;
            }
            """
        )
        self.results_table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table non-editable
        layout.addWidget(self.results_table)

        # Start scanning automatically
        self.start_scan()

    def start_scan(self):
        # Simulate scanning progress using a QTimer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(100)  # Update progress every 100ms

    def update_progress(self):
        # Increment progress bar value
        current_value = self.progress_bar.value()
        if current_value < 100:
            self.progress_bar.setValue(current_value + 1)
            self.update_scan_details(current_value + 1)
        else:
            self.timer.stop()
            self.show_scan_results()

    def update_scan_details(self, progress):
        # Update files scanned, threats detected, elapsed time, and progress percentage
        files_scanned = int(progress * 1000 / 100)  # Simulate file count
        threats_detected = int(progress * 10 / 100)  # Simulate threat count
        elapsed_time = self.start_time.secsTo(QTime.currentTime())  # Calculate elapsed time in seconds

        self.files_scanned_label.setText(f"Files Scanned: {files_scanned}")
        self.threats_detected_label.setText(f"Threats Detected: {threats_detected}")
        self.elapsed_time_label.setText(f"Elapsed Time: {QTime(0, 0).addSecs(elapsed_time).toString('mm:ss')}")
        self.progress_percentage_label.setText(f"{progress}%")  # Update progress percentage

    def show_scan_results(self):
        # Display scan results in the table
        self.results_table.setRowCount(5)  # Simulate 5 results
        for i in range(5):
            file_item = QTableWidgetItem(f"File_{i + 1}.exe")
            status_item = QTableWidgetItem("Scanned")
            threat_item = QTableWidgetItem("No Threat")

            # Make items non-editable
            file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
            status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
            threat_item.setFlags(threat_item.flags() & ~Qt.ItemIsEditable)

            self.results_table.setItem(i, 0, file_item)
            self.results_table.setItem(i, 1, status_item)
            self.results_table.setItem(i, 2, threat_item)

        # Add or update the result label
        if self.result_label is None:
            self.result_label = QLabel("Scan Complete: No threats detected.")
            self.result_label.setStyleSheet("font-size: 18px; color: green;")
            self.layout().addWidget(self.result_label)
        else:
            self.result_label.setText("Scan Complete: No threats detected.")

    def rescan(self):
        """Resets the scan and starts it again."""
        # Reset progress bar and labels
        self.progress_bar.setValue(0)
        self.progress_percentage_label.setText("0%")
        self.files_scanned_label.setText("Files Scanned: 0")
        self.threats_detected_label.setText("Threats Detected: 0")
        self.elapsed_time_label.setText("Elapsed Time: 00:00")

        # Clear the results table
        self.results_table.setRowCount(0)

        # Reset the start time
        self.start_time = QTime.currentTime()

        # Start the scan again
        self.start_scan()