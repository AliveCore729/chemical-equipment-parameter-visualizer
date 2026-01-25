import sys
import requests
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QLabel, QFileDialog
)

API_UPLOAD_URL = "http://127.0.0.1:8000/api/upload/"
API_TOKEN = "198094be83d8b909f71a8526901e5f8c4e2d46c7"


class EquipmentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(200, 200, 500, 400)

        layout = QVBoxLayout()

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.upload_csv)

        self.result_label = QLabel("Upload a CSV file to see results")
        self.result_label.setWordWrap(True)

        layout.addWidget(self.upload_btn)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def upload_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if not file_path:
            return

        with open(file_path, "rb") as f:
            response = requests.post(
                API_UPLOAD_URL,
                headers={"Authorization": f"Token {API_TOKEN}"},
                files={"file": f}
            )

        if response.status_code != 200:
            self.result_label.setText("Error uploading file")
            return

        data = response.json()

        # Update summary text
        self.result_label.setText(
            f"Total Equipment: {data['total_equipment']}\n"
            f"Avg Flowrate: {data['avg_flowrate']:.2f}\n"
            f"Avg Pressure: {data['avg_pressure']:.2f}\n"
            f"Avg Temperature: {data['avg_temperature']:.2f}"
        )

        self.show_charts(data)

    def show_charts(self, data):
        # Pie chart
        plt.figure(figsize=(6, 4))
        plt.pie(
            data["type_distribution"].values(),
            labels=data["type_distribution"].keys(),
            autopct="%1.1f%%"
        )
        plt.title("Equipment Type Distribution")
        plt.show()

        # Bar chart
        plt.figure(figsize=(6, 4))
        plt.bar(
            ["Flowrate", "Pressure", "Temperature"],
            [
                data["avg_flowrate"],
                data["avg_pressure"],
                data["avg_temperature"],
            ]
        )
        plt.title("Average Parameters")
        plt.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EquipmentApp()
    window.show()
    sys.exit(app.exec_())
