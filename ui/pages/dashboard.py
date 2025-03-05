from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QSizePolicy, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from ui.notification_dialog import NotificationDialog
from ui.scan_button import ScanButton


class DashboardPage(QWidget):
    def __init__(self, main_window):  # Accept main_window as an argument
        super().__init__()
        self.main_window = main_window  # Store the reference to MainWindow
        self.notifications_button = None  # Store the notification button reference
        self.notification_dialog = None  # Store the notification dialog reference
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # Remove margins around the main layout
        layout.setSpacing(10)  # Reduce spacing between widgets in the main layout

        # Notifications button
        self.notifications_button = QPushButton("🔔 Notifications")
        self.notifications_button.setStyleSheet(self.notifications_button_style())
        self.notifications_button.setFixedWidth(160)
        self.notifications_button.setFixedHeight(40)
        self.notifications_button.setContentsMargins(0, 0, 0, 0)
        self.notifications_button.clicked.connect(self.show_notification_dialog)  # Connect to local method
        layout.addWidget(self.notifications_button, alignment=Qt.AlignRight)

        # Header section with a gradient background
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: transparent;")
        header_frame.setFixedHeight(150)  # Adjust height as needed
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)  # Minimal spacing between logo and label
        header_layout.setContentsMargins(20, 10, 20, 10)  # Tight margins
        header_frame.setLayout(header_layout)

        # Add a secure logo (e.g., a checkmark or shield)
        secure_logo = QLabel()
        secure_logo.setPixmap(QPixmap("ui/logos/secure_logo.png").scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        secure_logo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  # Prevent unnecessary stretching
        secure_logo.setAlignment(Qt.AlignVCenter)  # Align logo vertically
        header_layout.addWidget(secure_logo)

        # Add "System is Secure" text with stylish font
        header_label = QLabel("System is Secure")
        header_label.setAlignment(Qt.AlignVCenter)  # Align text vertically
        header_label.setStyleSheet(
            "font-size: 32px;"
            "font-weight: bold;"
            "color: white;"
            "font-family: 'Arial';"
            "margin-left: 10px;"  # Add a small margin to separate logo and label
        )
        header_layout.addWidget(header_label)

        # Add the header frame to the main layout
        layout.addWidget(header_frame, alignment=Qt.AlignTop)  # Align header to the top

        # Add a stretch to push the scan buttons higher
        layout.addStretch(1)  # Adjust the stretch factor to control the spacing

        # Scan options
        scan_layout = QHBoxLayout()
        scan_layout.setSpacing(20)  # Spacing between scan buttons
        scan_layout.setContentsMargins(20, 20, 20, 20)  # Margins around the scan buttons

        # Quick Scan button
        self.quick_scan_button = ScanButton("ui/logos/Quick_Scan.png", "Quick Scan")
        self.quick_scan_button.clicked.connect(lambda: print("Quick Scan started!"))
        scan_layout.addWidget(self.quick_scan_button)

        # Full Scan button
        self.full_scan_button = ScanButton("ui/logos/Full_Scan.png", "Full Scan")
        self.full_scan_button.clicked.connect(lambda: print("Full Scan started!"))
        scan_layout.addWidget(self.full_scan_button)

        # Removable Scan button
        self.removable_scan_button = ScanButton("ui/logos/Removable_Scan.png", "Removable Scan")
        self.removable_scan_button.clicked.connect(lambda: print("Removable Scan started!"))
        scan_layout.addWidget(self.removable_scan_button)

        # Custom Scan button
        self.custom_scan_button = ScanButton("ui/logos/Custom_Scan.png", "Custom Scan")
        self.custom_scan_button.clicked.connect(self.open_custom_scan_dialog)  # Connect to handler
        scan_layout.addWidget(self.custom_scan_button)

        layout.addLayout(scan_layout)

        # Initialize the notification dialog
        self.notification_dialog = NotificationDialog(self.main_window)
        self.notification_dialog.hide()  # Initially hidden

    def show_notification_dialog(self):
        print("Notification button clicked!")  # Debug print
        if not self.notification_dialog:
            print("Dialog not initialized!")  # Debug print
            return

        # Calculate the position relative to the right side of the window
        window_width = self.main_window.width()
        dialog_width = self.notification_dialog.width()
        dialog_x = window_width - dialog_width - 18  # 20px margin from the right edge
        dialog_y = 18  # Fixed vertical position (adjust as needed)

        # Move the dialog to the calculated position
        self.notification_dialog.move(dialog_x, dialog_y)

        # Ensure the dialog is raised to the top
        self.notification_dialog.raise_()
        self.notification_dialog.activateWindow()

        # Show the dialog
        self.notification_dialog.show()

    def open_custom_scan_dialog(self):
        #Handle Custom Scan button click.
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder for Custom Scan")
        if folder_path:
            # Trigger scan via MainWindow
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