from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QProgressBar, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QPushButton, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt, QTimer, QTime, Signal, QObject
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize
from scanner.scanner import Scanner, Directory
import threading
import os
import time


# Worker class to handle background scanning
class ScannerWorker(QObject):
    progress_updated = Signal(int, int, dict)
    scan_completed = Signal(list)
    scan_paused = Signal()
    scan_stopped = Signal()

    def __init__(self, scan_paths):
        super().__init__()
        self.scan_paths = scan_paths
        self.is_running = False
        self.is_paused = False

    def run_scan(self):
        # Only proceed if not already running
        if self.is_running:
            return

        self.is_running = True
        self.is_paused = False
        results = []
        total_files = 0
        processed_files = 0
        threats_found = 0

        self.scanner = Scanner()

        # Count total files to scan for progress calculation
        for path in self.scan_paths:
            if os.path.isfile(path):
                total_files += 1
            elif os.path.isdir(path):
                for root, _, files in os.walk(path):
                    total_files += len(files)

        # Perform the scan
        for path in self.scan_paths:
            if not self.is_running:
                break

            for result in self.scanner.full_scan(path):
                if not self.is_running:
                    break

                # Pause the scan if requested
                while self.is_paused:
                    time.sleep(0.1)
                    if not self.is_running:
                        break

                processed_files += 1

                # Check if malware was found
                is_malware = result.get('malware', False)
                if is_malware:
                    threats_found += 1

                # Calculate progress percentage
                progress_percent = min(int((processed_files / total_files) * 100), 100)

                # Prepare file info for UI update
                file_info = {
                    "path": result["path"],
                    "status": "Infected" if is_malware else "Clean",
                    "threat": "Malware Detected" if is_malware else "None"
                }

                # Emit signal to update UI
                self.progress_updated.emit(progress_percent, threats_found, file_info)

                # Add to results list
                results.append(result)

                # Small delay to prevent UI freezing
                time.sleep(0.01)

        # Complete the scan
        if self.is_running:
            self.scan_completed.emit(results)

        self.is_running = False

    def pause(self):
        """Pause the scan."""
        self.is_paused = True
        self.scan_paused.emit()

    def resume(self):
        """Resume the scan."""
        self.is_paused = False

    def stop(self):
        """Stop the scan."""
        self.is_running = False
        self.is_paused = False
        self.scan_stopped.emit()


class ScanningPage(QWidget):
    def __init__(self, scan_type, scan_paths, parent=None):
        super().__init__(parent)
        self.scan_type = scan_type  # Type of scan (e.g., "Custom Scan")
        self.scan_paths = scan_paths  # List of files/directories to scan
        self.start_time = QTime.currentTime()  # Track the start time of the scan
        self.result_label = None  # Add a class-level variable for the result label
        self.scan_thread = None
        self.scanner_worker = None
        self.files_processed = 0
        self.threats_detected = 0
        self.is_paused = False  # Track if the scan is paused
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)  # Add spacing between widgets

        # Top Bar Layout (Rescan Button + Header + Pause/Stop Buttons)
        top_bar_layout = QHBoxLayout()
        top_bar_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Rescan Button with Logo
        self.rescan_button = QPushButton()
        self.rescan_button.setIcon(QIcon("ui/logos/rescan.png"))  # Add rescan logo
        self.rescan_button.setIconSize(QSize(50, 50))  # Set icon size
        self.rescan_button.setFixedSize(50, 50)  # Set button size
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

        # Add a spacer to push the Pause and Stop buttons to the right
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        top_bar_layout.addSpacerItem(spacer)

        # Add Pause and Stop buttons to the top-right corner
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignRight)

        # Pause Button
        self.pause_button = QPushButton()
        self.pause_button.setIcon(QIcon("ui/logos/pause.png"))  # Add pause logo
        self.pause_button.setIconSize(QSize(25, 25))  # Smaller icon size
        self.pause_button.setFixedSize(50, 50)  # Same button size as rescan
        self.pause_button.setStyleSheet(
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
        self.pause_button.clicked.connect(self.toggle_pause)
        button_layout.addWidget(self.pause_button)

        # Stop Button
        self.stop_button = QPushButton()
        self.stop_button.setIcon(QIcon("ui/logos/stop.png"))  # Add stop logo
        self.stop_button.setIconSize(QSize(25, 25))  # Smaller icon size
        self.stop_button.setFixedSize(50, 50)  # Same button size as rescan
        self.stop_button.setStyleSheet(
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
        self.stop_button.clicked.connect(self.stop_scan)
        button_layout.addWidget(self.stop_button)

        top_bar_layout.addLayout(button_layout)
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
        # Prevent starting multiple scans
        if hasattr(self, 'scan_thread') and self.scan_thread and self.scan_thread.is_alive():
            print("Scan already in progress, not starting another one")
            return

        # Show the pause and stop buttons
        self.pause_button.show()
        self.stop_button.show()

        # Create a worker and thread for scanning
        self.scanner_worker = ScannerWorker(self.scan_paths)
        self.scanner_worker.progress_updated.connect(self.update_real_progress)
        self.scanner_worker.scan_completed.connect(self.on_scan_completed)
        self.scanner_worker.scan_paused.connect(self.on_scan_paused)
        self.scanner_worker.scan_stopped.connect(self.on_scan_stopped)

        # Create and start a thread for scanning
        self.scan_thread = threading.Thread(target=self.scanner_worker.run_scan)
        self.scan_thread.daemon = True
        self.scan_thread.start()

        # Start a timer just to update the elapsed time
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_elapsed_time)
        self.timer.start(1000)  # Update time every second

    def update_elapsed_time(self):
        # Update only the elapsed time
        elapsed_time = self.start_time.secsTo(QTime.currentTime())  # Calculate elapsed time in seconds
        self.elapsed_time_label.setText(f"Elapsed Time: {QTime(0, 0).addSecs(elapsed_time).toString('mm:ss')}")

    def update_real_progress(self, progress, threats, file_info):
        # Update UI with real scan progress
        self.progress_bar.setValue(progress)
        self.progress_percentage_label.setText(f"{progress}%")

        self.files_processed += 1
        self.files_scanned_label.setText(f"Files Scanned: {self.files_processed}")

        self.threats_detected = threats
        self.threats_detected_label.setText(f"Threats Detected: {self.threats_detected}")

        # Add result to table
        row_position = self.results_table.rowCount()
        self.results_table.insertRow(row_position)

        file_item = QTableWidgetItem(os.path.basename(file_info["path"]))
        status_item = QTableWidgetItem(file_info["status"])
        threat_item = QTableWidgetItem(file_info["threat"])

        # Make items non-editable
        file_item.setFlags(file_item.flags() & ~Qt.ItemIsEditable)
        status_item.setFlags(status_item.flags() & ~Qt.ItemIsEditable)
        threat_item.setFlags(threat_item.flags() & ~Qt.ItemIsEditable)

        # Set row colors based on status
        if file_info["status"] == "Infected":
            file_item.setBackground(Qt.red)
            status_item.setBackground(Qt.red)
            threat_item.setBackground(Qt.red)

        self.results_table.setItem(row_position, 0, file_item)
        self.results_table.setItem(row_position, 1, status_item)
        self.results_table.setItem(row_position, 2, threat_item)

    def on_scan_completed(self, results):
        # Called when scan is fully complete
        self.timer.stop()

        # Ensure progress bar is at 100%
        self.progress_bar.setValue(100)
        self.progress_percentage_label.setText("100%")

        # Update scan info label
        self.scan_info_label.setText(f"{self.scan_type} Complete")

        # Add or update the result label
        result_text = f"Scan Complete: {self.threats_detected} threats detected."
        text_color = "red" if self.threats_detected > 0 else "green"

        if self.result_label is None:
            self.result_label = QLabel(result_text)
            self.result_label.setStyleSheet(f"font-size: 18px; color: {text_color};")
            self.layout().addWidget(self.result_label)
        else:
            self.result_label.setText(result_text)
            self.result_label.setStyleSheet(f"font-size: 18px; color: {text_color};")

        # Hide the pause and stop buttons after scan completion
        self.pause_button.hide()
        self.stop_button.hide()

    def toggle_pause(self):
        """Toggle between pause and resume."""
        if self.scanner_worker:
            if self.is_paused:
                self.scanner_worker.resume()
                self.pause_button.setIcon(QIcon("ui/logos/pause.png"))
                self.scan_info_label.setText(f"{self.scan_type} in Progress...")
            else:
                self.scanner_worker.pause()
                self.pause_button.setIcon(QIcon("ui/logos/resume.png"))
                self.scan_info_label.setText(f"{self.scan_type} Paused")
            self.is_paused = not self.is_paused

    def stop_scan(self):
        """Stop the scan."""
        if self.scanner_worker:
            self.scanner_worker.stop()
            self.scan_info_label.setText(f"{self.scan_type} Stopped")
            self.timer.stop()

            # Hide the pause and stop buttons
            self.pause_button.hide()
            self.stop_button.hide()

    def on_scan_paused(self):
        """Handle scan paused event."""
        self.scan_info_label.setText(f"{self.scan_type} Paused")

    def on_scan_stopped(self):
        """Handle scan stopped event."""
        self.scan_info_label.setText(f"{self.scan_type} Stopped")
        self.timer.stop()

    def rescan(self):
        """Resets the scan and starts it again."""
        # Stop the current scan if it's running
        if self.scanner_worker and self.scan_thread and self.scan_thread.is_alive():
            self.scanner_worker.stop()
            self.scan_thread.join(timeout=1.0)

        # Reset progress bar and labels
        self.progress_bar.setValue(0)
        self.progress_percentage_label.setText("0%")
        self.files_scanned_label.setText("Files Scanned: 0")
        self.threats_detected_label.setText("Threats Detected: 0")
        self.elapsed_time_label.setText("Elapsed Time: 00:00")
        self.files_processed = 0
        self.threats_detected = 0

        # Clear the results table
        self.results_table.setRowCount(0)

        # Reset the start time
        self.start_time = QTime.currentTime()

        # Update scan info label
        self.scan_info_label.setText(f"{self.scan_type} in Progress...")

        # Show the pause and stop buttons
        self.pause_button.show()
        self.stop_button.show()

        # Start the scan again
        self.start_scan()