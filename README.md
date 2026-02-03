# Chemical Equipment Parameter Visualizer ⚗️
### Hybrid Web + Desktop Application with Secure Authentication

![Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-4.0+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![PyQt5](https://img.shields.io/badge/PyQt-5-yellow.svg)

---

## 📌 Overview

The **Chemical Equipment Parameter Visualizer** is a hybrid application that helps analyze and visualize operational data of chemical equipment. Users can securely log in, upload CSV files, view analytics through charts, track upload history, and generate PDF reports.

A **single Django REST backend** serves both a **React-based Web Application** and a **PyQt5-based Desktop Application**, ensuring consistent data access and authentication.

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

### 🔙 Backend- Django
- Django REST Framework
- Token-Based Authentication
- Pandas
- SQLite
- ReportLab (PDF Generation)

### 🌐 Web Frontend
- React.js
- React Router DOM
- Chart.js
- Axios
- Modern Dark UI

### 🖥️ Desktop Frontend
- PyQt5
- Matplotlib
- Requests
- Threaded API Calls

---

## ✨ Features

### 🔐 Authentication
- User Signup & Login
- Secure token-based sessions
- Protected routes and dashboards
- Logout support

### 📊 Core Features
- CSV upload and validation
- Automatic data analysis
- Summary analytics:
  - Equipment count
  - Average flowrate
  - Average pressure
  - Average temperature
- Equipment type distribution

### 🌐 Web Application
- Interactive charts
- Upload history
- PDF report downloads
- Responsive dark UI

### 🖥️ Desktop Application
- Dedicated login window
- Native PyQt5 interface
- Embedded Matplotlib charts
- Fully synchronized data

---

## 📁 Project Structure

ChemicalProject/
├── backend/
│   ├── backend/
│   ├── equipment/
│   └── manage.py
│
├── web/
│   └── src/
│
├── desktop/
│   ├── app.py
│   └── .env
│
├── venv/
└── README.md

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

## 📊 Sample CSV Format

Equipment Name | Type | Flowrate | Pressure | Temperature  
Tank-01 | Reactor | 500 | 12.5 | 85  
Pump-A | Pump | 1200 | 45.0 | 40  

---

## 👤 Author

**Shreyansh Jain**  
Undergraduate | Software & Web Development

Focus: Data Structures, Backend Systems, Full-Stack Development.

---

## 🏁 Conclusion

This project demonstrates a real-world **hybrid architecture** where a single secure backend efficiently serves both web and desktop applications.
