from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from ui.notification_dialog import NotificationDialog
from ui.scan_button import ScanButton
import os

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.notifications_button = None
        self.notification_dialog = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # Notifications button
        self.notifications_button = QPushButton("🔔 Notifications")
        self.notifications_button.setStyleSheet(self.notifications_button_style())
        self.notifications_button.setFixedWidth(160)
        self.notifications_button.setFixedHeight(40)
        self.notifications_button.setContentsMargins(0, 0, 0, 0)
        self.notifications_button.clicked.connect(self.show_notification_dialog)
        layout.addWidget(self.notifications_button, alignment=Qt.AlignRight)

        # Header section
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_frame.setFixedHeight(150)
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        header_layout.setContentsMargins(20, 10, 20, 10)
        header_frame.setLayout(header_layout)

        # Secure logo
        secure_logo = QLabel()
        secure_logo.setPixmap(QPixmap("ui/logos/secure_logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        secure_logo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        secure_logo.setAlignment(Qt.AlignVCenter)
        header_layout.addWidget(secure_logo)

        # Header label
        header_label = QLabel("System is Secure")
        header_label.setAlignment(Qt.AlignVCenter)
        header_label.setStyleSheet(
            "font-size: 32px;"
            "font-weight: bold;"
            "color: white;"
            "font-family: 'Arial';"
            "margin-left: 10px;"
        )
        header_layout.addWidget(header_label)

        layout.addWidget(header_frame, alignment=Qt.AlignTop)
        layout.addStretch(1)

        # Scan options
        scan_layout = QHBoxLayout()
        scan_layout.setSpacing(20)
        scan_layout.setContentsMargins(20, 20, 20, 20)

        # Quick Scan button
        self.quick_scan_button = ScanButton("ui/logos/Quick_Scan.png", "Quick Scan")
        self.quick_scan_button.start_scan_signal.connect(self.handle_quick_scan)
        scan_layout.addWidget(self.quick_scan_button)

        # Full Scan button
        self.full_scan_button = ScanButton("ui/logos/Full_Scan.png", "Full Scan")
        self.full_scan_button.start_scan_signal.connect(self.main_window.start_scan)
        scan_layout.addWidget(self.full_scan_button)

        # Removable Scan button
        self.removable_scan_button = ScanButton("ui/logos/Removable_Scan.png", "Removable Scan")
        self.removable_scan_button.start_scan_signal.connect(self.main_window.start_scan)
        scan_layout.addWidget(self.removable_scan_button)

        # Custom Scan button
        self.custom_scan_button = ScanButton("ui/logos/Custom_Scan.png", "Custom Scan")
        self.custom_scan_button.clicked.connect(self.open_custom_scan_dialog)
        scan_layout.addWidget(self.custom_scan_button)

        layout.addLayout(scan_layout)

        # Initialize notification dialog
        self.notification_dialog = NotificationDialog(self.main_window)
        self.notification_dialog.hide()

    def handle_quick_scan(self, scan_type, scan_paths):
        """Handle quick scan by scanning common system locations"""
        # Define common system locations to scan
        quick_scan_paths = [
            os.path.expanduser("~/.local/share"),
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            "/tmp"
        ]
        
        # Filter to only existing paths
        existing_paths = [path for path in quick_scan_paths if os.path.exists(path)]
        
        # Start the scan with the filtered paths
        self.main_window.start_scan(scan_type, existing_paths)

    def show_notification_dialog(self):
        if not self.notification_dialog:
            return

        window_width = self.main_window.width()
        dialog_width = self.notification_dialog.width()
        dialog_x = window_width - dialog_width - 18
        dialog_y = 18

        self.notification_dialog.move(dialog_x, dialog_y)
        self.notification_dialog.raise_()
        self.notification_dialog.activateWindow()
        self.notification_dialog.show()

    def open_custom_scan_dialog(self):
        """Handle Custom Scan button click (for folders)"""
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder for Custom Scan")
        if folder_path:
            self.main_window.start_scan("Custom Scan", [folder_path])

    def notifications_button_style(self):
        return (
            "QPushButton {"
            "    border: none;"
            "    text-align: center;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "    padding: 8px 15px;"
            "    border-radius: 10px;"
            "    background-color: transparent;"
            "} "
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "    border-top-left-radius: 0px; "
            "    border-bottom-left-radius: 20px; "
            "    border-top-right-radius: 20px; "
            "    border-bottom-right-radius: 0px; "
            "} "
        )