import React, { useState, useEffect } from "react";
import "./App.css"; // Ensure this matches the file name exactly
import Upload from "./Upload";
import History from "./History";

function App() {
  return (
    <div className="app-container">
      <header className="dashboard-header">
        <h1>Parameter Dashboard</h1>
        <p>Real-time Chemical Equipment Visualization</p>
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

export default App;