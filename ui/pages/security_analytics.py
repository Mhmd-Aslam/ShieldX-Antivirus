from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import calendar
from datetime import datetime

class GraphPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.create_charts()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # Page title
        title_label = QLabel("Security Analytics")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1; background: transparent;")
        main_layout.addWidget(title_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Subtitle with current date
        current_date = datetime.now().strftime("%B %d, %Y")
        subtitle_label = QLabel(f"Security Metrics - {current_date}")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setStyleSheet("color: #BDC3C7; background: transparent;")
        main_layout.addWidget(subtitle_label, alignment=Qt.AlignTop | Qt.AlignLeft)

        # Chart container
        chart_container = QHBoxLayout()
        chart_container.setSpacing(20)

        # Left column (Main chart)
        self.left_chart_card = self.create_chart_card("Daily Threat Activity", 600, 400)
        chart_container.addWidget(self.left_chart_card)

        # Right column (Smaller charts)
        right_column = QVBoxLayout()
        right_column.setSpacing(20)

        self.top_right_chart = self.create_chart_card("Threat Type Distribution", 300, 300)
        self.bottom_right_chart = self.create_chart_card("Severity Levels", 300, 300)
        
        right_column.addWidget(self.top_right_chart)
        right_column.addWidget(self.bottom_right_chart)
        
        chart_container.addLayout(right_column)
        main_layout.addLayout(chart_container)

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #2C3E50;")

    def create_chart_card(self, title, width, height):
        """Create a styled card container for charts"""
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: #34495E;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        layout = QVBoxLayout(card)
        
        # Card title
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 14, QFont.Bold))
        title_label.setStyleSheet("color: #ECF0F1; background: transparent;")
        layout.addWidget(title_label)
        
        # Matplotlib figure
        fig = Figure(figsize=(width/100, height/100), facecolor='none')
        fig.set_facecolor('#34495E00')  # Transparent background
        canvas = FigureCanvas(fig)
        canvas.setStyleSheet("background-color: transparent;")
        layout.addWidget(canvas)
        
        return card

    def create_charts(self):
        # Get current date info
        now = datetime.now()
        current_day = now.day
        current_month = now.month
        current_year = now.year
        
        # Create data only up to current day
        days = list(range(1, current_day + 1))
        threats = np.random.randint(0, 15, size=current_day)  # Integer threats 0-15
        
        # Create x-axis ticks - show every 5 days or every day if less than 10 days
        if current_day > 10:
            step = 5
            day_ticks = list(range(1, current_day + 1, step))
            # Make sure current day is included
            if day_ticks[-1] != current_day:
                day_ticks.append(current_day)
        else:
            day_ticks = days

        # Threat types and counts (integers)
        threat_types = ['Malware', 'Phishing', 'Ransomware', 'Spyware']
        type_counts = np.random.randint(1, 20, size=4)  # Integer counts 1-20
        
        # Severity levels (integer counts)
        severities = ['Critical', 'High', 'Medium', 'Low']
        severity_counts = np.random.randint(5, 30, size=4)  # Integer counts 5-30

        # Main timeline chart (line graph)
        main_fig = self.left_chart_card.layout().itemAt(1).widget().figure
        ax = main_fig.add_subplot(111)
        
        # Line plot with markers
        ax.plot(days, threats, color='#E74C3C', marker='o', 
               linestyle='-', linewidth=2, markersize=6)
        
        # Customize x-axis with dates
        ax.set_xticks(day_ticks)
        ax.set_xticklabels([str(d) for d in day_ticks])
        ax.set_xlim(0.5, current_day + 0.5)
        
        # Styling
        ax.set_facecolor('#34495E')
        ax.set_xlabel('Date', color='#ECF0F1')  # Changed from "Time Period" to "Date"
        ax.set_ylabel('Threat Count', color='#ECF0F1')
        ax.set_title(f"Daily Threat Activity", color='#ECF0F1')
        ax.tick_params(colors='#BDC3C7')
        ax.grid(color='#7F8C8D', alpha=0.3)
        main_fig.tight_layout()

        # Threat type distribution (Bar chart)
        type_fig = self.top_right_chart.layout().itemAt(1).widget().figure
        ax2 = type_fig.add_subplot(111)
        colors = ['#3498DB', '#2ECC71', '#F1C40F', '#E74C3C']
        ax2.bar(threat_types, type_counts, color=colors)
        ax2.set_facecolor('#34495E')
        ax2.set_title('Threat Type Distribution', color='#ECF0F1')
        ax2.tick_params(colors='#BDC3C7')
        ax2.yaxis.grid(color='#7F8C8D', alpha=0.3)
        type_fig.tight_layout()

        # Severity levels (Pie chart with percentages only)
        severity_fig = self.bottom_right_chart.layout().itemAt(1).widget().figure
        ax3 = severity_fig.add_subplot(111)
        explode = (0.1, 0, 0, 0)
        colors = ['#E74C3C', '#F1C40F', '#3498DB', '#2ECC71']
        
        ax3.pie(severity_counts, explode=explode, labels=severities, colors=colors,
                autopct='%1.1f%%', startangle=140, 
                textprops={'color': '#ECF0F1'})
        ax3.set_title('Severity Distribution', color='#ECF0F1')
        ax3.axis('equal')
        severity_fig.tight_layout()

if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    app = QApplication([])
    window = GraphPage()
    window.show()
    app.exec()