from PySide6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame, QProgressBar
)
from PySide6.QtCore import Qt, QTimer, QThread, Signal
from PySide6.QtGui import QFont, QPixmap
import psutil
import platform
import time

class NetworkSpeedWorker(QThread):
    speed_updated = Signal(str)

    def run(self):
        """Run the network speed test in a separate thread."""
        try:
            import speedtest
            print("Running network speed test...")  # Debugging
            st = speedtest.Speedtest()
            st.get_best_server()  # Fetch the best server
            download_speed = st.download() / 1_000_000  # Convert to Mbps
            print(f"Download Speed: {download_speed:.2f} Mbps")  # Debugging
            self.speed_updated.emit(f"{download_speed:.2f} Mbps")
        except Exception as e:
            print(f"Speed test failed: {e}")  # Debugging
            self.speed_updated.emit("Offline")


class SystemHealthPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_timer()
        self.last_network_test_time = 0  # Track last network test time
        self.network_worker = None  # Initialize the network worker

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Page title
        title_label = QLabel("System Health")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1;")
        main_layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Overview of System Performance and Health Metrics")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #BDC3C7;")
        main_layout.addWidget(subtitle_label)

        # Metrics Layout
        self.metrics_layout = QHBoxLayout()
        self.metrics_layout.setSpacing(20)

        # CPU Usage Card
        self.cpu_card = self.create_metric_card("CPU Usage", "ui/logos/cpu_icon.png", 0, "#3498DB")
        self.metrics_layout.addWidget(self.cpu_card)

        # Memory Usage Card
        self.memory_card = self.create_metric_card("Memory Usage", "ui/logos/memory_icon.png", 0, "#E74C3C")
        self.metrics_layout.addWidget(self.memory_card)

        # Disk Usage Card
        self.disk_card = self.create_metric_card("Disk Usage", "ui/logos/disk_icon.png", 0, "#2ECC71")
        self.metrics_layout.addWidget(self.disk_card)

        main_layout.addLayout(self.metrics_layout)

        # System Status Section
        status_label = QLabel("System Status")
        status_label.setFont(QFont("Arial", 18, QFont.Bold))
        status_label.setStyleSheet("color: #ECF0F1;")
        main_layout.addWidget(status_label)

        # Status cards layout
        self.status_layout = QHBoxLayout()
        self.status_layout.setSpacing(20)

        # Temperature Status
        self.temp_card = self.create_status_card("Temperature", "ui/logos/temp_icon.png", "Loading...", "#F1C40F")
        self.status_layout.addWidget(self.temp_card)

        # Network Status
        self.network_card = self.create_status_card("Network", "ui/logos/network_icon.png", "Loading...", "#3498DB")
        self.status_layout.addWidget(self.network_card)

        # Power Status
        self.power_card = self.create_status_card("Power", "ui/logos/power_icon.png", "Loading...", "#2ECC71")
        self.status_layout.addWidget(self.power_card)

        main_layout.addLayout(self.status_layout)

        # Set the main layout
        self.setLayout(main_layout)

    def init_timer(self):
        """Initialize a QTimer to update data periodically."""
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # Update every 1 second

    def update_data(self):
        """Update all system health data."""
        self.update_cpu_usage()
        self.update_memory_usage()
        self.update_disk_usage()
        self.update_temperature()
        self.update_network_status()
        self.update_power_status()

    def update_cpu_usage(self):
        """Update CPU usage."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        self.update_progress_bar(self.cpu_card, cpu_percent)

    def update_memory_usage(self):
        """Update memory usage."""
        memory_info = psutil.virtual_memory()
        memory_percent = memory_info.percent
        self.update_progress_bar(self.memory_card, memory_percent)

    def update_disk_usage(self):
        """Update disk usage."""
        disk_info = psutil.disk_usage('/')
        disk_percent = disk_info.percent
        self.update_progress_bar(self.disk_card, disk_percent)

    def update_temperature(self):
        """Update system temperature."""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.label == "Package id 0":
                            self.update_status_label(self.temp_card, f"{entry.current}°C")
                            break
                    break
            else:
                self.update_status_label(self.temp_card, "N/A")
        except Exception as e:
            self.update_status_label(self.temp_card, "N/A")

    def update_network_status(self):
        """Run network test only every 30 seconds."""
        current_time = time.time()
        if current_time - self.last_network_test_time > 30:
            self.last_network_test_time = current_time
            self.start_network_test()

    def start_network_test(self):
        """Start the network speed test in a separate thread."""
        if self.network_worker and self.network_worker.isRunning():
            return  # Avoid multiple threads

        self.network_worker = NetworkSpeedWorker()
        self.network_worker.speed_updated.connect(
            lambda status: self.update_status_label(self.network_card, status)
        )
        self.network_worker.start()

    def update_power_status(self):
        """Update power status."""
        battery = psutil.sensors_battery()
        if battery:
            power_status = f"{battery.percent}%"
            if battery.power_plugged:
                power_status += " (Plugged In)"
            else:
                power_status += " (Battery)"
            self.update_status_label(self.power_card, power_status)
        else:
            self.update_status_label(self.power_card, "N/A")

    def update_progress_bar(self, card, value):
        """Update the progress bar in a metric card."""
        progress_bar = card.layout().itemAt(2).widget()
        progress_bar.setValue(int(value))
        value_label = card.layout().itemAt(3).widget()
        value_label.setText(f"{value}%")

    def update_status_label(self, card, status):
        """Update the status label in a status card."""
        status_label = card.layout().itemAt(2).widget()
        status_label.setText(status)

    def create_metric_card(self, title, icon_path, value, color):
        """Create a card for displaying a system metric."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #34495E;
                border-radius: 10px;
                padding: 15px;
            }}
            """
        )
        card_layout = QVBoxLayout(card)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio))
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Progress bar
        progress_bar = QProgressBar()
        progress_bar.setValue(value)
        progress_bar.setTextVisible(False)
        progress_bar.setStyleSheet(
            f"""
            QProgressBar {{
                background-color: #2C3E50;
                border-radius: 5px;
                height: 10px;
            }}
            QProgressBar::chunk {{
                background-color: {color};
                border-radius: 5px;
            }}
            """
        )
        card_layout.addWidget(progress_bar)

        # Value
        value_label = QLabel(f"{value}%")
        value_label.setFont(QFont("Arial", 12))
        value_label.setStyleSheet("color: #BDC3C7;")
        card_layout.addWidget(value_label, alignment=Qt.AlignCenter)

        return card


    def create_status_card(self, title, icon_path, status, color):
        """Create a card for displaying system status."""
        card = QFrame()
        card.setStyleSheet(
            f"""
            QFrame {{
                background-color: #34495E;
                border-radius: 10px;
                padding: 15px;
            }}
            """
        )
        card_layout = QVBoxLayout(card)

        # Icon
        icon_label = QLabel()
        icon_label.setPixmap(QPixmap(icon_path).scaled(40, 40, Qt.KeepAspectRatio))
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)

        # Title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)

        # Status
        status_label = QLabel(status)
        status_label.setFont(QFont("Arial", 12))
        status_label.setStyleSheet(f"color: {color};")
        card_layout.addWidget(status_label, alignment=Qt.AlignCenter)

        return card


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = SystemHealthPage()
    window.show()
    app.exec()