from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PySide6.QtGui import QIcon, QFont
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Antivirus UI")
        self.resize(1200, 700)
        self.setStyleSheet("background-color: #1E2A38; color: white;")
        
        # Main layout
        main_layout = QHBoxLayout()
        
        # Sidebar
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("background-color: #2E3A48;")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)
        
        add_user_button = QPushButton("➕ Add User")
        add_user_button.setStyleSheet(self.sidebar_button_style())
        sidebar_layout.addWidget(add_user_button)
        
        for label in ["Scan History", "Summary", "Top Threats", "System Health", "Graph", "Settings"]:
            button = QPushButton(label)
            button.setStyleSheet(self.sidebar_button_style())
            sidebar_layout.addWidget(button)
        
        add_files_button = QPushButton("📂 Add Files to Scan")
        add_files_button.setStyleSheet(self.add_files_button_style())
        sidebar_layout.addWidget(add_files_button, alignment=Qt.AlignTop)
        
        sidebar_layout.addStretch()
        
        # Main content area
        content_frame = QFrame()
        content_layout = QVBoxLayout()
        content_frame.setLayout(content_layout)
        
        # Header section
        header_label = QLabel("✔️ System is Secure")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("font-size: 28px; font-weight: bold;")
        content_layout.addWidget(header_label)
        
        # Scan options
        scan_layout = QHBoxLayout()
        for name, icon in [("Quick Scan", "⏱"), ("Full Scan", "💻"), ("Removable Scan", "💾"), ("Custom Scan", "📁")]:
            button = QPushButton(f"{icon}\n{name}")
            button.setStyleSheet(self.scan_button_style())
            button.setFixedSize(160, 110)
            scan_layout.addWidget(button)
        
        content_layout.addLayout(scan_layout)
        
        # Notifications and content assembly
        notifications_button = QPushButton("🔔 Notifications")
        notifications_button.setStyleSheet("border: none; color: white; font-size: 18px;")
        notifications_button.setFixedWidth(150)
        
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content_frame)
        central_widget = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(notifications_button, alignment=Qt.AlignRight)
        central_layout.addLayout(main_layout)
        central_widget.setLayout(central_layout)
        self.setCentralWidget(central_widget)
        
    def sidebar_button_style(self):
        return (
            "QPushButton {"
            "    border: none;"
            "    text-align: left;"
            "    padding: 12px 25px;"
            "    font-size: 18px;"
            "    color: white;"
            "    background-color: transparent;"
            "}"
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "}"
        )
    
    def add_files_button_style(self):
        return (
            "QPushButton {"
            "    border: 2px dashed #888;"
            "    border-radius: 12px;"
            "    text-align: center;"
            "    padding: 20px;"
            "    font-size: 16px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "}"
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "}"
        )
    
    def scan_button_style(self):
        return (
            "QPushButton {"
            "    border: 2px solid #888;"
            "    border-radius: 12px;"
            "    font-size: 16px;"
            "    color: white;"
            "    background-color: #2E3A48;"
            "}"
            "QPushButton:hover {"
            "    background-color: #3B4A5A;"
            "}"
        )
    
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()



