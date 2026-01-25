```markdown
# Chemical Equipment Parameter Visualizer ⚗️
### Hybrid Web + Desktop Application

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.0+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt-5-yellow.svg)

---

## 📌 Project Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application designed to analyze and visualize operational parameters of chemical equipment. The system allows users to upload CSV datasets, automatically compute analytics, visualize results using charts, maintain upload history, and generate downloadable PDF reports.

A **single Django REST backend** powers both:
1.  A **React-based Web Application**
2.  A **PyQt5-based Desktop Application**

This ensures consistency, scalability, and a real-world architectural approach.

---

## 🧠 Problem Statement

Chemical plants often maintain equipment data in CSV format. Manually analyzing this data is time-consuming and error-prone.

**This application solves this by:**
* Automating CSV ingestion.
* Computing summary statistics immediately.
* Visualizing trends for quick decision-making.
* Generating standardized PDF reports.
* Supporting both web (remote) and desktop (local) environments.

---

## ⚙️ Tech Stack

### 🔙 Backend
* **Framework:** Django, Django REST Framework (DRF)
* **Data Processing:** Pandas
* **Database:** SQLite
* **Reporting:** ReportLab (PDF Generation)

### 🌐 Web Frontend
* **Framework:** React.js
* **Visualization:** Chart.js
* **HTTP Client:** Axios

### 🖥️ Desktop Frontend
* **GUI Framework:** PyQt5
* **Visualization:** Matplotlib
* **HTTP Client:** Requests

### 🔐 Authentication
* **Method:** Token-based Authentication (DRF)

---

## ✨ Features

### Core Features
- [x] CSV file upload & validation
- [x] Automatic data parsing using Pandas
- [x] **Summary Analytics:**
    - Total equipment count
    - Average flowrate
    - Average pressure
    - Average temperature
- [x] Equipment type distribution analysis
- [x] Secure REST APIs with Token-based authentication

### 🌐 Web Application
- Interactive dashboard
- Pie chart for equipment distribution & Bar chart for average parameters
- Upload history (Retains last 5 datasets)
- Secure PDF report download

### 🖥️ Desktop Application
- Native desktop window for CSV upload
- Summary analytics display
- Embedded Matplotlib charts (Pie and Bar)
- Consumes the exact same backend APIs as the web app

### 📄 Reporting
- Server-side PDF generation via ReportLab
- **Includes:** Dataset metadata, upload timestamp, summary analytics, and equipment distribution.

---

## 📁 Project Structure

```text
ChemicalProject/
├── backend/                  # Django Project Root
│   ├── backend/              # Project Settings (settings.py, urls.py)
│   ├── equipment/            # Core App
│   │   ├── models.py         # Database Models
│   │   ├── views.py          # API Logic
│   │   ├── urls.py           # App routing
│   │   └── migrations/       # DB Migrations
│   ├── db.sqlite3            # SQLite Database
│   └── manage.py             # Django Entry Point
│
├── web/                      # React Frontend
│   ├── src/
│   │   ├── App.js            # Main Component
│   │   ├── History.js        # History Component
│   │   └── index.js          # Entry Point
│   └── package.json          # Dependencies
│
├── desktop/                  # Desktop Client
│   └── app.py                # PyQt5 Application Entry
│
├── venv/                     # Virtual Environment
└── README.md                 # Project Documentation

```

---

## 🚀 How to Run the Project

### 1️⃣ Backend (Django)

The backend must be running for the Web and Desktop apps to work.

```bash
cd backend
source ../venv/bin/activate  # Or 'venv\Scripts\activate' on Windows
python manage.py runserver

```

*The backend will run at:* `http://127.0.0.1:8000/`

### 2️⃣ Web Frontend (React)

Open a new terminal:

```bash
cd web
npm install
npm start

```

*The web app will run at:* `http://localhost:3000/`

### 3️⃣ Desktop Application (PyQt5)

Open a new terminal:

```bash
cd desktop
# Ensure requirements are installed (pip install PyQt5 matplotlib requests)
python app.py

```

*A desktop window will open for CSV upload and visualization.*

---

## 📊 Sample Data

Use the provided `sample_equipment_data.csv` file for testing. The system expects the following columns:

| Equipment Name | Type | Flowrate | Pressure | Temperature |
| --- | --- | --- | --- | --- |
| Tank-01 | Reactor | 500 | 12.5 | 85 |

---

## 🔐 Authentication & Reporting

* **Security:** Token-based authentication is enforced for CSV uploads, history retrieval, and PDF downloads.
* **PDF Reports:** Reports are generated on the backend using **ReportLab** and downloaded via authenticated API calls. They include dataset metadata and statistical summaries.

---

## 👤 Author

**Shreyansh Jain**
*Undergraduate | Software & Web Development*

Focus: Data Structures, Backend Systems, Full-Stack Development.

---

## 🏁 Conclusion

This project demonstrates a complete **end-to-end hybrid system** using industry-relevant technologies. It follows clean architecture principles and is suitable for real-world data visualization and reporting use cases.

```
