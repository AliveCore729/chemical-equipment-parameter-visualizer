import sys
import requests
import os
from dotenv import load_dotenv
from functools import partial

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QFrame, QGridLayout, QGroupBox, 
    QMessageBox, QScrollArea, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

load_dotenv()
API_URL_BASE = os.getenv("API_URL", "http://127.0.0.1:8000")

API_LOGIN = f"{API_URL_BASE}/api/login/"
API_REGISTER = f"{API_URL_BASE}/api/register/"
API_UPLOAD = f"{API_URL_BASE}/api/upload/"
API_HISTORY = f"{API_URL_BASE}/api/history/"
API_REPORT = f"{API_URL_BASE}/api/report/"

STYLESHEET = """
QMainWindow, QWidget#LoginWindow { 
    background-color: #0f172a; 
}
QLabel { 
    color: #ffffff; 
    font-family: 'Segoe UI', sans-serif; 
}

/* FIX: Make the Scroll Area Transparent so it isn't white */
QScrollArea {
    background-color: transparent;
    border: none;
}
QScrollArea > QWidget > QWidget {
    background-color: transparent;
}

/* Inputs */
QLineEdit {
    padding: 12px;
    border-radius: 8px;
    border: 1px solid #334155;
    background-color: #1e293b;
    color: white;
    font-size: 14px;
    selection-background-color: #f59e0b;
}
QLineEdit:focus { 
    border: 1px solid #f59e0b; 
}

/* Panels */
QGroupBox {
    border: 1px solid #334155; 
    border-radius: 12px; 
    margin-top: 10px;
    background-color: #1e293b; 
    font-weight: bold; 
    color: #94a3b8;
}
QGroupBox::title { 
    subcontrol-origin: margin; 
    left: 10px; 
    padding: 0 5px; 
}

/* Login Container Frame */
QFrame#LoginFrame {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 16px;
}

/* Buttons */
QPushButton {
    background-color: #f59e0b; 
    color: white; 
    border: none;
    padding: 10px; 
    border-radius: 6px; 
    font-weight: bold;
    font-size: 13px;
}
QPushButton:hover { 
    background-color: #d97706; 
}

QPushButton#SecondaryBtn {
    background-color: transparent; 
    border: 1px solid #475569; 
    color: #cbd5e1;
}
QPushButton#SecondaryBtn:hover { 
    background-color: rgba(255,255,255,0.05); 
    color: white; 
    border-color: #94a3b8;
}

QPushButton#DownloadBtn {
    background-color: rgba(255, 255, 255, 0.1); 
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #cbd5e1; 
    font-size: 11px; 
    padding: 6px; 
    margin-top: 5px;
}
QPushButton#DownloadBtn:hover { 
    background-color: rgba(255, 255, 255, 0.2); 
    color: white; 
}

/* History Items */
QFrame#HistoryCard {
    background-color: rgba(0, 0, 0, 0.2); 
    border-radius: 8px;
    border-left: 3px solid rgba(255, 255, 255, 0.1);
}
QFrame#HistoryCard:hover {
    background-color: rgba(255, 255, 255, 0.05); 
    border-left: 3px solid #f59e0b;
}

/* Stats */
QLabel#StatValue { font-size: 20px; font-weight: bold; color: #38bdf8; }
QLabel#StatLabel { color: #94a3b8; font-size: 11px; text-transform: uppercase; }
QLabel#HistTitle { font-weight: bold; font-size: 13px; color: #e2e8f0; }
QLabel#HistMeta { font-size: 11px; color: #64748b; }
"""

class LoginWindow(QWidget):
    loginSuccess = pyqtSignal(str) 

    def __init__(self):
        super().__init__()
        self.setObjectName("LoginWindow")
        self.setWindowTitle("Login - Chemical Visualizer")
        self.setGeometry(100, 100, 400, 550)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        title_label = QLabel("Welcome Back")
        title_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        
        subtitle = QLabel("Sign in to continue")
        subtitle.setStyleSheet("color: #94a3b8; font-size: 14px;")
        subtitle.setAlignment(Qt.AlignCenter)

        form_frame = QFrame()
        form_frame.setObjectName("LoginFrame")
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(15)
        form_layout.setContentsMargins(25, 30, 25, 30)

        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Username")
        
        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Password")
        self.pass_input.setEchoMode(QLineEdit.Password)

        self.btn_login = QPushButton("Login")
        self.btn_login.setCursor(Qt.PointingHandCursor)
        self.btn_login.setFixedHeight(40)
        self.btn_login.clicked.connect(self.handle_login)

        self.btn_signup = QPushButton("Create Account")
        self.btn_signup.setObjectName("SecondaryBtn")
        self.btn_signup.setCursor(Qt.PointingHandCursor)
        self.btn_signup.setFixedHeight(40)
        self.btn_signup.clicked.connect(self.handle_signup)

        form_layout.addWidget(QLabel("Username"))
        form_layout.addWidget(self.user_input)
        form_layout.addWidget(QLabel("Password"))
        form_layout.addWidget(self.pass_input)
        form_layout.addSpacing(10)
        form_layout.addWidget(self.btn_login)
        form_layout.addWidget(self.btn_signup)

        layout.addStretch()
        layout.addWidget(title_label)
        layout.addWidget(subtitle)
        layout.addWidget(form_frame)
        layout.addStretch()
        
        self.setLayout(layout)

    def handle_login(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return

        try:
            response = requests.post(API_LOGIN, json={'username': username, 'password': password})
            
            if response.status_code == 200:
                token = response.json().get('token')
                self.loginSuccess.emit(token)
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", f"Could not connect to server.\n{e}")

    def handle_signup(self):
        username = self.user_input.text()
        password = self.pass_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter a username and password to register")
            return

        try:
            response = requests.post(API_REGISTER, json={'username': username, 'password': password})
            if response.status_code == 201:
                QMessageBox.information(self, "Success", "Account created successfully!\nPlease click Login.")
            else:
                QMessageBox.warning(self, "Error", "Username likely taken.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

class EquipmentApp(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 1200, 800)
        
        self.initUI()
        self.refresh_history()

    def get_headers(self):
        return {"Authorization": f"Token {self.token}"}

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header = QLabel("Parameter Dashboard")
        header.setFont(QFont("Segoe UI", 22, QFont.Bold))
        
        btn_logout = QPushButton("Logout")
        btn_logout.setObjectName("SecondaryBtn")
        btn_logout.setFixedWidth(80)
        btn_logout.clicked.connect(self.close)

        header_layout.addWidget(header)
        header_layout.addStretch()
        header_layout.addWidget(btn_logout)
        left_layout.addLayout(header_layout)

        upload_group = QGroupBox("New Analysis")
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel("No file selected")
        self.file_label.setStyleSheet("color: #64748b; font-style: italic;")
        
        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.setCursor(Qt.PointingHandCursor)
        self.upload_btn.setFixedWidth(120)
        self.upload_btn.clicked.connect(self.upload_csv)

        upload_layout.addWidget(self.upload_btn)
        upload_layout.addWidget(self.file_label)
        upload_group.setLayout(upload_layout)
        left_layout.addWidget(upload_group)

        self.stats_group = QGroupBox("Overview")
        self.stats_layout = QGridLayout()
        self.stats_group.setLayout(self.stats_layout)
        self.stats_group.setVisible(False) 
        left_layout.addWidget(self.stats_group)

        self.chart_group = QGroupBox("Visualization")
        chart_layout = QVBoxLayout()
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.figure.patch.set_facecolor('#1e293b')
        self.canvas = FigureCanvas(self.figure)
        chart_layout.addWidget(self.canvas)
        self.chart_group.setLayout(chart_layout)
        self.chart_group.setVisible(False)
        left_layout.addWidget(self.chart_group, stretch=1)

        right_panel = QWidget()
        right_panel.setFixedWidth(320) 
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)

        hist_label = QLabel("Recent Activity")
        hist_label.setFont(QFont("Segoe UI", 14, QFont.Bold))
        hist_label.setStyleSheet("color: #94a3b8; margin-bottom: 5px;")
        right_layout.addWidget(hist_label)

        self.hist_scroll = QScrollArea()
        self.hist_scroll.setWidgetResizable(True)

        self.hist_container = QWidget()
        self.hist_container.setAttribute(Qt.WA_StyledBackground, True)
        self.hist_container.setStyleSheet("background-color: transparent;") 
        
        self.hist_layout = QVBoxLayout(self.hist_container)
        self.hist_layout.setAlignment(Qt.AlignTop)
        self.hist_layout.setSpacing(10)
        
        self.hist_scroll.setWidget(self.hist_container)
        right_layout.addWidget(self.hist_scroll)

        main_layout.addWidget(left_panel, stretch=3)
        main_layout.addWidget(right_panel, stretch=1)

    def refresh_history(self):
        for i in reversed(range(self.hist_layout.count())): 
            self.hist_layout.itemAt(i).widget().setParent(None)

        try:
            response = requests.get(API_HISTORY, headers=self.get_headers())
            
            if response.status_code == 200:
                history_data = response.json()
                if not history_data:
                    self.hist_layout.addWidget(QLabel("No history found."))
                else:
                    for item in history_data:
                        self.add_history_card(item)
            elif response.status_code == 401:
                QMessageBox.warning(self, "Session Expired", "Please restart to login again.")
        except Exception as e:
            print("History connection error:", e)

    def add_history_card(self, item):
        card = QFrame()
        card.setObjectName("HistoryCard")
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(4)
        
        lbl_name = QLabel(item['filename'])
        lbl_name.setObjectName("HistTitle")
        lbl_name.setWordWrap(True)
        
        lbl_date = QLabel(item['uploaded_at'].split("T")[0])
        lbl_date.setObjectName("HistMeta")
        
        metrics = QLabel(f"Flow: {item['avg_flowrate']:.1f} | Press: {item['avg_pressure']:.1f}")
        metrics.setStyleSheet("color: #64748b; font-size: 11px;")
        
        btn_download = QPushButton("Download Report PDF")
        btn_download.setObjectName("DownloadBtn")
        btn_download.setCursor(Qt.PointingHandCursor)
        btn_download.clicked.connect(partial(self.download_report, item['id'], item['filename']))

        card_layout.addWidget(lbl_name)
        card_layout.addWidget(lbl_date)
        card_layout.addWidget(metrics)
        card_layout.addWidget(btn_download)
        self.hist_layout.addWidget(card)

    def download_report(self, report_id, filename):
        save_path, _ = QFileDialog.getSaveFileName(
            self, "Save Report", f"{filename}_report.pdf", "PDF Files (*.pdf)"
        )
        if not save_path: return

        try:
            response = requests.get(
                f"{API_REPORT}{report_id}/",
                headers=self.get_headers(),
                stream=True
            )
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                QMessageBox.information(self, "Success", "Report downloaded successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to download report.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Download failed: {str(e)}")

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
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if not file_path: return

        self.file_label.setText(os.path.basename(file_path))

        try:
            with open(file_path, "rb") as f:
                response = requests.post(
                    API_UPLOAD,
                    headers=self.get_headers(),
                    files={"file": f}
                )

            if response.status_code == 200:
                data = response.json()
                self.display_results(data)
                self.refresh_history() 
            else:
                QMessageBox.critical(self, "Error", f"Upload failed: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Connection Error", str(e))

    def display_results(self, data):
        for i in reversed(range(self.stats_layout.count())): 
            self.stats_layout.itemAt(i).widget().setParent(None)

        self.create_stat_card("Total Equipment", data['total_equipment'], 0, 0)
        self.create_stat_card("Avg Flowrate", f"{data['avg_flowrate']:.2f}", 0, 1)
        self.create_stat_card("Avg Pressure", f"{data['avg_pressure']:.2f}", 0, 2)
        self.create_stat_card("Avg Temperature", f"{data['avg_temperature']:.2f}", 0, 3)
        self.stats_group.setVisible(True)

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

class MainController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setStyleSheet(STYLESHEET)
        
        self.login_window = LoginWindow()
        self.login_window.loginSuccess.connect(self.switch_to_main)
        self.login_window.show()
        
        self.main_window = None
        sys.exit(self.app.exec_())

    def switch_to_main(self, token):
        self.login_window.close()
        self.main_window = EquipmentApp(token)
        self.main_window.show()

if __name__ == "__main__":
    MainController()