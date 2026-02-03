import React from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import "./App.css"; 
import Upload from "./Upload";
import History from "./History";
import SignIn from "./SignIn";   
import Signup from "./Signup"; 

const PrivateRoute = ({ children }) => {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/" />;
};

function Dashboard() {
  const handleLogout = () => {
    localStorage.removeItem("token"); 
    window.location.href = "/";       
  };

  return (
    <div className="app-container">
      <header className="dashboard-header">
        {/* Header Flex Container for Title + Logout Button */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
          <div>
            <h1>Parameter Dashboard</h1>
            <p>Real-time Chemical Equipment Visualization</p>
          </div>
          
          <button onClick={handleLogout} className="btn-logout">
            Logout
          </button>
        </div>
      </header>

      <div className="main-grid">
        {/* Left Section: Upload & Charts */}
        <div className="content-area">
          <Upload />
        </div>

        {/* Right Section: History */}
        <div className="sidebar-area">
          <History />
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<SignIn />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected Route */}
        <Route 
          path="/dashboard" 
          element={
            <PrivateRoute>
              <Dashboard />
            </PrivateRoute>
          } 
        />
      </Routes>
    </Router>
  );
}

export default App;