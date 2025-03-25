# ui/scan_button.py
from PySide6.QtWidgets import (QPushButton, QLabel, QVBoxLayout, QSizePolicy, 
                              QMessageBox, QDialog, QVBoxLayout, QListWidget, 
                              QDialogButtonBox)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from scanner.scanner import Scanner

class ScanButton(QPushButton):
    start_scan_signal = Signal(str, list)  # scan_type, paths
    
    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)
        self.icon_path = icon_path
        self.name = name
        self.scanner = Scanner()
        self.init_ui()
        self.clicked.connect(self.handle_scan_click)
    
    def handle_scan_click(self):
        """Handle scan button click based on scan type"""
        if self.name == "Removable Scan":
            self.handle_removable_scan()
        elif self.name == "Quick Scan":
            self.start_scan_signal.emit("Quick Scan", [])
        elif self.name == "Full Scan":
            self.start_scan_signal.emit("Full Scan", [])
        elif self.name == "Custom Scan":
            pass  # Handled by DashboardPage
    
    def handle_removable_scan(self):
        """Handle removable device scanning with user selection"""
        removable_drives = self.scanner.get_removable_drives()
        
        if not removable_drives:
            QMessageBox.information(self, "No Removable Drives", 
                                  "No removable drives were detected.")
            return
        
        if len(removable_drives) == 1:
            # Auto-select if only one drive found
            self.start_scan_signal.emit("Removable Scan", removable_drives)
        else:
            # Show selection dialog for multiple drives
            self.show_removable_selection_dialog(removable_drives)
    
    def show_removable_selection_dialog(self, drives):
        """Show dialog to select which removable drives to scan"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Drive to Scan")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        label = QLabel("Select removable drive to scan:")
        layout.addWidget(label)
        
        list_widget = QListWidget()
        for drive in drives:
            list_widget.addItem(drive)
        layout.addWidget(list_widget)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.Accepted:
            selected_items = list_widget.selectedItems()
            if selected_items:
                selected_drive = selected_items[0].text()
                self.start_scan_signal.emit("Removable Scan", [selected_drive])

    def init_ui(self):
        """Initialize button UI"""
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
        return """
            QPushButton {
                border: 2px solid #888;
                border-radius: 20px;
                font-size: 18px;
                color: white;
                background-color: #2E3A48;
                padding: 10px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #3B4A5A;
            }
        """

    def enterEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: #3B4A5A;
                border: 2px solid #888;
                border-radius: 20px;
            }
        """)
        self.icon_label.setStyleSheet("background-color: #3B4A5A;")
        self.text_label.setStyleSheet("font-size: 18px; color: white; background-color: #3B4A5A;")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setStyleSheet(self.default_style())
        self.icon_label.setStyleSheet("background-color: #2E3A48;")
        self.text_label.setStyleSheet("font-size: 16px; color: white; background-color: #2E3A48;")
        super().leaveEvent(event)