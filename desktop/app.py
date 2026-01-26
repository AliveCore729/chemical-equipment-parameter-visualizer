import sys
import requests
import os
from dotenv import load_dotenv  # IMPORT THIS

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QGridLayout, QGroupBox, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

# --- 1. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()  # This loads the .env file

API_UPLOAD_URL = os.getenv("API_URL", "http://127.0.0.1:8000/api/upload/")
API_TOKEN = os.getenv("API_TOKEN")

# --- STYLESHEET (Keep existing stylesheet) ---
STYLESHEET = """
QMainWindow {
    background-color: #0f172a;
}
QLabel {
    color: #ffffff;
    font-family: 'Segoe UI', sans-serif;
}
QGroupBox {
    border: 1px solid #334155;
    border-radius: 8px;
    margin-top: 10px;
    background-color: #1e293b;
    color: #94a3b8;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
}
QPushButton {
    background-color: #f59e0b;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    font-weight: bold;
    font-size: 14px;
}
QPushButton:hover {
    background-color: #d97706;
}
QPushButton:pressed {
    background-color: #b45309;
}
QLabel#StatValue {
    font-size: 24px;
    font-weight: bold;
    color: #38bdf8;
}
QLabel#StatLabel {
    color: #94a3b8;
    font-size: 12px;
    text-transform: uppercase;
}
"""

class EquipmentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1100, 700)
        self.setStyleSheet(STYLESHEET)
        
        # Check if Token exists
        if not API_TOKEN:
            QMessageBox.critical(self, "Configuration Error", 
                                 "API_TOKEN not found.\nPlease create a .env file with your token.")

        self.initUI()

    def initUI(self):
        # ... (Keep the rest of your UI code EXACTLY the same) ...
        # Copy the initUI, create_stat_card, display_results methods from the previous answer
        # The logic below is just for the upload_csv method which uses the token
        
        # Main Container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # 1. Header
        header = QLabel("Parameter Dashboard")
        header.setFont(QFont("Segoe UI", 24, QFont.Bold))
        main_layout.addWidget(header)

        # 2. Upload Section
        upload_group = QGroupBox("Data Input")
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #64748b; font-style: italic;")
        
        self.upload_btn = QPushButton("Upload CSV & Analyze")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.clicked.connect(self.upload_csv)

        upload_layout.addWidget(self.upload_btn)
        upload_layout.addWidget(self.file_label)
        upload_layout.addStretch()
        
        upload_group.setLayout(upload_layout)
        main_layout.addWidget(upload_group)

        # 3. Stats Grid
        self.stats_group = QGroupBox("Overview")
        self.stats_layout = QGridLayout()
        self.stats_group.setLayout(self.stats_layout)
        self.stats_group.setVisible(False) 
        main_layout.addWidget(self.stats_group)

        # 4. Charts Area
        self.chart_group = QGroupBox("Visualization")
        chart_layout = QVBoxLayout()
        
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#1e293b')
        self.canvas = FigureCanvas(self.figure)
        
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)
        self.chart_group.setVisible(False)
        main_layout.addWidget(self.chart_group, stretch=1)

    def create_stat_card(self, title, value, row, col):
        container = QFrame()
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        
        lbl_title = QLabel(title)
        lbl_title.setObjectName("StatLabel")
        lbl_value = QLabel(str(value))
        lbl_value.setObjectName("StatValue")
        
        layout.addWidget(lbl_title)
        layout.addWidget(lbl_value)
        container.setLayout(layout)
        self.stats_layout.addWidget(container, row, col)

    def upload_csv(self):
        # Safety Check
        if not API_TOKEN:
            QMessageBox.critical(self, "Error", "Cannot upload: API Token is missing.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        self.file_label.setText(os.path.basename(file_path))

        try:
            with open(file_path, "rb") as f:
                response = requests.post(
                    API_UPLOAD_URL,
                    # SECURELY USE THE VARIABLE LOADED FROM .ENV
                    headers={"Authorization": f"Token {API_TOKEN}"},
                    files={"file": f}
                )

            if response.status_code != 200:
                QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
                return

            data = response.json()
            self.display_results(data)

        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def display_results(self, data):
        # Update Stats
        for i in reversed(range(self.stats_layout.count())): 
            self.stats_layout.itemAt(i).widget().setParent(None)

        self.create_stat_card("Total Equipment", data['total_equipment'], 0, 0)
        self.create_stat_card("Avg Flowrate", f"{data['avg_flowrate']:.2f}", 0, 1)
        self.create_stat_card("Avg Pressure", f"{data['avg_pressure']:.2f}", 0, 2)
        self.create_stat_card("Avg Temperature", f"{data['avg_temperature']:.2f}", 0, 3)
        
        self.stats_group.setVisible(True)

        # Update Charts
        self.figure.clear()
        text_color = 'white'
        bar_colors = ['#10b981', '#f59e0b', '#ef4444'] 
        
        ax1 = self.figure.add_subplot(121)
        ax1.pie(
            data["type_distribution"].values(),
            labels=data["type_distribution"].keys(),
            autopct="%1.1f%%",
            textprops={'color': text_color}
        )
        ax1.set_title("Equipment Types", color=text_color)

        ax2 = self.figure.add_subplot(122)
        ax2.bar(
            ["Flow", "Press", "Temp"],
            [data["avg_flowrate"], data["avg_pressure"], data["avg_temperature"]],
            color=bar_colors
        )
        ax2.set_title("Average Parameters", color=text_color)
        ax2.tick_params(axis='x', colors=text_color)
        ax2.tick_params(axis='y', colors=text_color)
        ax2.spines['bottom'].set_color(text_color)
        ax2.spines['top'].set_color('none') 
        ax2.spines['right'].set_color('none')
        ax2.spines['left'].set_color(text_color)
        ax2.set_facecolor('#1e293b')

        self.canvas.draw()
        self.chart_group.setVisible(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentApp()
    window.show()
    sys.exit(app.exec_())