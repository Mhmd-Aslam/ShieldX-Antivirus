from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QCheckBox, QComboBox,
    QLineEdit, QSlider, QFrame, QScrollArea, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Page title
        title_label = QLabel("Settings")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1; background-color: transparent;")
        main_layout.addWidget(title_label)

        # Scroll area for settings
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("background-color: transparent; border: none;")

        # Container for settings
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(10, 10, 10, 10)
        container_layout.setSpacing(20)

        # General Settings
        general_settings = self.create_setting_section("General Settings")
        self.add_setting(general_settings, "Auto-start with system", QCheckBox())
        self.add_setting(general_settings, "Language", QComboBox(), items=["English", "Spanish", "French", "German"])
        self.add_setting(general_settings, "Check for updates", QCheckBox())
        container_layout.addLayout(general_settings)

        # Scan Settings
        scan_settings = self.create_setting_section("Scan Settings")
        self.add_setting(scan_settings, "Enable real-time scanning", QCheckBox())
        self.add_setting(scan_settings, "Scan sensitivity", QSlider(Qt.Horizontal), min_value=1, max_value=10)
        self.add_setting(scan_settings, "Exclude files/folders", QLineEdit(), placeholder="Enter paths to exclude")
        container_layout.addLayout(scan_settings)

        # Notifications
        notification_settings = self.create_setting_section("Notifications")
        self.add_setting(notification_settings, "Enable notifications", QCheckBox())
        self.add_setting(notification_settings, "Notification sound", QComboBox(), items=["Default", "Beep", "Silent"])
        self.add_setting(notification_settings, "Show notifications for:", QCheckBox("Critical threats only"))
        container_layout.addLayout(notification_settings)

        # Appearance
        appearance_settings = self.create_setting_section("Appearance")
        self.add_setting(appearance_settings, "Theme", QComboBox(), items=["Dark", "Light", "System Default"])
        self.add_setting(appearance_settings, "Font size", QSlider(Qt.Horizontal), min_value=10, max_value=20)
        self.add_setting(appearance_settings, "Accent color", QComboBox(), items=["Blue", "Red", "Green", "Yellow"])
        container_layout.addLayout(appearance_settings)

        # Add a spacer to push content to the top
        container_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Set the container to the scroll area
        scroll_area.setWidget(container)
        main_layout.addWidget(scroll_area)

        # Save button
        save_button = QPushButton("Save Settings")
        save_button.setFont(QFont("Arial", 12))
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #3498DB;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #2980B9;
            }
        """)
        save_button.clicked.connect(self.save_settings)
        main_layout.addWidget(save_button, alignment=Qt.AlignRight)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #2C3E50; color: #ECF0F1;")

    def create_setting_section(self, title):
        """Create a collapsible settings section"""
        section_layout = QVBoxLayout()
        section_layout.setSpacing(10)

        # Section title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #3498DB;")
        section_layout.addWidget(title_label)

        # Separator line
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #7F8C8D;")
        section_layout.addWidget(separator)

        return section_layout

    def add_setting(self, layout, label_text, widget, items=None, placeholder=None, min_value=None, max_value=None):
        """Add a setting with a label and widget"""
        setting_layout = QHBoxLayout()
        setting_layout.setSpacing(20)

        # Label
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12))
        label.setStyleSheet("color: #ECF0F1;")
        setting_layout.addWidget(label)

        # Widget
        if isinstance(widget, QComboBox) and items:
            widget.addItems(items)
        if isinstance(widget, QSlider) and min_value is not None and max_value is not None:
            widget.setRange(min_value, max_value)
        if isinstance(widget, QLineEdit) and placeholder:
            widget.setPlaceholderText(placeholder)
        setting_layout.addWidget(widget)

        layout.addLayout(setting_layout)

    def save_settings(self):
        """Save settings (placeholder for actual implementation)"""
        print("Settings saved!")

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = SettingsPage()
    window.show()
    app.exec()
