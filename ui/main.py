# ui/main.py
import sys
import os

# Debug: Print the current working directory and Python path
print("Current Working Directory:", os.getcwd())
print("Python Path:", sys.path)

# Add the 'project-av' folder to the Python path
project_av_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print("Adding to Python Path:", project_av_path)
sys.path.append(project_av_path)

# Debug: Check if 'ui' folder is in the Python path
print("Updated Python Path:", sys.path)
from ui.main_window import MainWindow
from PySide6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.showMaximized()
    app.exec()