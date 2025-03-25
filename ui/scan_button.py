from PySide6.QtWidgets import QPushButton, QLabel, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

class ScanButton(QPushButton):
    # Signal to emit when scan should start
    start_scan_signal = Signal(str, list)  # scan_type, paths
    
    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.name = name
        self.init_ui()
        
        # Connect button click to emit signal
        self.clicked.connect(self.handle_scan_click)
    
    def handle_scan_click(self):
        """Handle scan button click based on scan type"""
        if self.name == "Quick Scan":
            # For quick scan, we don't need any paths - it will scan default locations
            self.start_scan_signal.emit("Quick Scan", [])
        elif self.name == "Custom Scan":
            # Custom scan will be handled by DashboardPage
            pass
        else:
            # Other scan types (Full Scan, Removable Scan)
            self.start_scan_signal.emit(self.name, [])
    
    def init_ui(self):
        self.setFixedSize(180, 130)
        self.setStyleSheet(self.default_style())

        button_layout = QVBoxLayout(self)
        button_layout.setAlignment(Qt.AlignCenter)
        button_layout.setContentsMargins(10, 10, 10, 10)
        button_layout.setSpacing(5)

        self.icon_label = QLabel()
        icon_pixmap = QPixmap(self.icon_path).scaled(65, 65, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.setStyleSheet("background-color: transparent;")
        self.icon_label.setFixedSize(100, 100)
        button_layout.addWidget(self.icon_label)

        self.text_label = QLabel(self.name)
        self.text_label.setStyleSheet("font-size: 16px; color: white; background-color: transparent;")
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setWordWrap(True)
        self.text_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        button_layout.addWidget(self.text_label)

    def default_style(self):
        return (
            "QPushButton {"
            "    border: 2px solid #888;"
            "    border-radius: 20px;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "    padding: 10px;"
            "    margin: 2px;"
            "}"
        )

    def enterEvent(self, event):
        self.setStyleSheet(
            "QPushButton {"
            "    background-color: #3B4A5A;"
            "    border: 2px solid #888;"
            "    border-radius: 20px;"
            "}"
        )
        self.icon_label.setStyleSheet("background-color: #3B4A5A;")
        self.text_label.setStyleSheet("font-size: 18px; color: white; background-color: #3B4A5A;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style())
        self.icon_label.setStyleSheet("background-color: #2E3A48;")
        self.text_label.setStyleSheet("font-size: 16px; color: white; background-color: #2E3A48;")
        super().leaveEvent(event)