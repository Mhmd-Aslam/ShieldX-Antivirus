from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame, QStackedWidget, QSizePolicy
from PySide6.QtCore import Qt, QPoint  # Import QPoint
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
# Absolute imports
from ui.notification_dialog import NotificationDialog
from ui.scan_button import ScanButton

# Import pages
from ui.pages.scan_history import ScanHistoryPage
from ui.pages.summary import SummaryPage
from ui.pages.top_threats import TopThreatsPage
from ui.pages.system_health import SystemHealthPage
from ui.pages.graph import GraphPage
from ui.pages.settings import SettingsPage
from ui.pages.about import AboutPage


class DashboardPage(QWidget):
    def __init__(self, main_window):  # Accept main_window as an argument
        super().__init__()
        self.main_window = main_window  # Store the reference to MainWindow
        self.notifications_button = None  # Store the notification button reference
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Notifications button
        self.notifications_button = QPushButton("🔔 Notifications")
        self.notifications_button.setStyleSheet(self.notifications_button_style())
        self.notifications_button.setFixedWidth(160)
        self.notifications_button.setFixedHeight(40)
        self.notifications_button.setContentsMargins(0, 0, 0, 0)
        self.notifications_button.clicked.connect(self.main_window.show_notification_dialog)  # Connect to MainWindow's method
        layout.addWidget(self.notifications_button, alignment=Qt.AlignRight)

        # Header section
        header_label = QLabel("✔️ System is Secure")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        layout.addWidget(header_label)
        layout.addStretch()

        # Scan options
        scan_layout = QHBoxLayout()
        for name, icon_path in [("Quick Scan", "ui/logos/Quick_Scan.png"),
                                ("Full Scan", "ui/logos/Full_Scan.png"),
                                ("Removable Scan", "ui/logos/Removable_Scan.png"),
                                ("Custom Scan", "ui/logos/Custom_Scan.png")]:
            button = ScanButton(icon_path, name)
            scan_layout.addWidget(button)

        layout.addLayout(scan_layout)
        self.setLayout(layout)

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


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fytra Antivirus")
        self.setWindowIcon(QIcon("ui/logos/app_logo.png"))
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #091e36; color: white;")

        # Track the currently active button
        self.active_button = None

        # Main layout (Vertical layout)
        main_layout = QVBoxLayout()

        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(
            "background-color:rgb(42, 87, 111);"
            "border-top-left-radius: 20px;"
            "border-bottom-left-radius: 20px;"
            "padding: 20px 0px 20px 0px;"
        )
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        # Add app logo and name to the sidebar
        app_logo = QLabel()
        app_logo.setPixmap(QPixmap("ui/logos/app_logo.png").scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        app_name = QLabel("Fytra Antivirus")
        app_name.setStyleSheet("font-size: 20px; font-weight: bold; color: white;")

        # Create a horizontal layout for the logo and app name
        app_info_layout = QHBoxLayout()
        app_info_layout.addWidget(app_logo)
        app_info_layout.addWidget(app_name)
        app_info_layout.setAlignment(Qt.AlignCenter)

        # Add vertical spacing above the app info layout
        sidebar_layout.addSpacing(-25)

        # Add the app info layout to the sidebar
        sidebar_layout.addLayout(app_info_layout)

        # Create a QStackedWidget to hold the different pages
        self.stacked_widget = QStackedWidget()

        # Add pages to the stacked widget
        self.pages = {
            "Dashboard": DashboardPage(self),  # Pass self (MainWindow) to DashboardPage
            "Scan History": ScanHistoryPage(),
            "Summary": SummaryPage(),
            "Top Threats": TopThreatsPage(),
            "System Health": SystemHealthPage(),
            "Graph": GraphPage(),
            "Settings": SettingsPage(),
            "About": AboutPage(),
        }

        for name, page in self.pages.items():
            self.stacked_widget.addWidget(page)

        # Add User Button
        add_user_button = QPushButton("➕ Add User")
        add_user_button.setStyleSheet(self.sidebar_button_style())
        sidebar_layout.addWidget(add_user_button)

        # Dashboard Button
        dashboard_button = QPushButton("Dashboard")
        dashboard_button.setStyleSheet(self.sidebar_button_style())
        dashboard_button.clicked.connect(lambda: self.set_active_page("Dashboard", dashboard_button))
        sidebar_layout.addWidget(dashboard_button)

        # Other buttons
        buttons = ["Scan History", "Summary", "Top Threats", "System Health", "Graph", "Settings"]
        self.page_buttons = {}  # Dictionary to store page buttons
        for label in buttons:
            button = QPushButton(label)
            button.setStyleSheet(self.sidebar_button_style())
            button.clicked.connect(lambda _, name=label: self.set_active_page(name, self.page_buttons[name]))
            self.page_buttons[label] = button
            sidebar_layout.addWidget(button)

        # About Button
        about_button = QPushButton("About")
        about_button.setStyleSheet(self.sidebar_button_style())
        about_button.clicked.connect(lambda: self.set_active_page("About", about_button))
        sidebar_layout.addWidget(about_button)

        sidebar_layout.addStretch()

        # Spacer for 50px gap
        spacer_widget = QWidget()
        spacer_widget.setFixedHeight(50)

        # Add Files button (vertical and at the bottom)
        add_files_button = QPushButton(" Add Files \n to Scan \n +")
        add_files_button.setStyleSheet(self.add_files_button_style())
        add_files_button.setFixedWidth(110)
        add_files_button.setFixedHeight(150)

        sidebar_layout.addWidget(spacer_widget)
        sidebar_layout.addWidget(add_files_button, alignment=Qt.AlignCenter)

        # Main content area with border (Solid Color Border)
        content_border = QFrame()
        content_border.setStyleSheet(
            "background-color: #1d2e4a; "
            "border-top-left-radius: 0px; "
            "border-bottom-left-radius: 0px; "
            "border-top-right-radius: 20px; "
            "border-bottom-right-radius: 20px; "
            "padding: -5px -5px 10px 0px;"
        )
        content_layout = QVBoxLayout()
        content_border.setLayout(content_layout)

        # Add the stacked widget to the content area
        content_layout.addWidget(self.stacked_widget)

        # Combine sidebar and main content
        top_layout = QHBoxLayout()
        top_layout.addWidget(sidebar)
        top_layout.addWidget(content_border)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addLayout(top_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)

        # Notification dialog
        self.notification_dialog = NotificationDialog(self)
        self.notification_dialog.hide()  # Initially hidden

        # Set the default active page
        self.set_active_page("Dashboard", dashboard_button)

    def set_active_page(self, page_name, button):
        """Set the active page and update button styles."""
        if self.active_button:
            # Reset the style of the previously active button
            self.active_button.setStyleSheet(self.sidebar_button_style())

        # Set the new active button and apply its style
        self.active_button = button
        self.active_button.setStyleSheet(self.active_button_style())

        # Set the current page in the stacked widget
        self.stacked_widget.setCurrentWidget(self.pages[page_name])

    def active_button_style(self):
        """Style for the active sidebar button."""
        return (
            "QPushButton {"
            "    border: none;"
            "    text-align: left;"
            "    padding: 10px 25px;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: #1d2e4a;"  # Different background for active button
            "} "
            "QPushButton:hover {"
            "    background-color: #4A5B6E;"  # Slightly different hover color
            "} "
        )

    def show_notification_dialog(self):
        print("Notification button clicked!")  # Debug print
        if not self.notification_dialog:
            print("Dialog not initialized!")  # Debug print
            return

        # Calculate the position relative to the right side of the window
        window_width = self.width()
        dialog_width = self.notification_dialog.width()
        dialog_x = window_width - dialog_width - 20  # 20px margin from the right edge
        dialog_y = 22  # Fixed vertical position (adjust as needed)

        # Move the dialog to the calculated position
        self.notification_dialog.move(dialog_x, dialog_y)

        # Ensure the dialog is raised to the top
        self.notification_dialog.raise_()
        self.notification_dialog.activateWindow()

        # Show the dialog
        self.notification_dialog.show()

    def resizeEvent(self, event):
        # Reposition the notification dialog when the window is resized
        if self.notification_dialog and self.notification_dialog.isVisible():
            self.show_notification_dialog()
        super().resizeEvent(event)

    def sidebar_button_style(self):
        return (
            "QPushButton {"
            "    border: none;"
            "    text-align: left;"
            "    padding: 10px 25px;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: transparent;"
            "} "
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "} "
        )

    def add_files_button_style(self):
        return (
            "QPushButton {"
            "    border: 2px dashed #888;"
            "    border-radius: 20px;"
            "    text-align: center;"
            "    padding: 10px;"
            "    font-size: 16px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "} "
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "} "
        )

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