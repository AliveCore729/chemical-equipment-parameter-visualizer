import React, { useState } from "react";
import axios from "axios";
import Charts from "./Charts";

function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  // --- DRAG & DROP HANDLERS ---
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const droppedFile = e.dataTransfer.files[0];
      
      // VALIDATION: Check if file ends with .csv
      if (!droppedFile.name.toLowerCase().endsWith('.csv')) {
        alert("Incorrect file format. Please upload a .csv file.");
        return;
      }
      
      setFile(droppedFile);
    }
  };

  const handleChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };
  // -----------------------------

  // --- UPLOAD LOGIC ---
  const uploadCSV = async () => {
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/upload/",
        formData,
        {
          headers: {
            Authorization: "Token 198094be83d8b909f71a8526901e5f8c4e2d46c7",
          },
        }
      );
      setResult(res.data);
    } catch (error) {
      console.error("Upload failed", error);
      // Show server error message if available, otherwise generic
      const errMsg = error.response?.data?.error || "Error uploading file. Ensure it is a valid CSV.";
      alert(errMsg);
    }
  };

  return (
    <div>
      {/* Upload Section */}
      <div className="glass-panel">
        <h2 className="section-title">New Analysis</h2>
        
        {/* Drag & Drop Zone */}
        <form
          onDragEnter={handleDrag}
          onSubmit={(e) => e.preventDefault()}
        >
          <input
            type="file"
            id="file-upload"
            accept=".csv"
            className="hidden-input"
            onChange={handleChange}
          />
          
          <label
            htmlFor="file-upload"
            className={`drag-drop-zone ${dragActive ? "active" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="upload-icon">📂</div>
            <div className="upload-text">
               Drop your CSV file here or <strong>browse</strong>
            </div>
            <p style={{fontSize:'0.75rem', color:'rgba(255,255,255,0.4)', marginTop: '5px'}}>
              Supports .csv files only
            </p>
          </label>

          {/* Selected File Feedback */}
          {file && (
            <div style={{textAlign:'center'}}>
              <div className="file-name-display">
                Selected: <strong>{file.name}</strong>
              </div>
            </div>
          )}

          {/* Action Button */}
          <div style={{ textAlign: 'center' }}>
            <button 
              onClick={uploadCSV} 
              className="btn-gradient"
              disabled={!file}
              style={{ opacity: file ? 1 : 0.5, cursor: file ? 'pointer' : 'not-allowed' }}
            >
              Analyze Data
            </button>
          </div>
        </form>
      </div>

      {/* Results Section (Stats & Charts) */}
      {result && (
        <div className="glass-panel">
          <h2 className="section-title">Overview</h2>
          
          <div className="stats-container">
            <div className="stat-card">
              <span className="stat-label">Equipment Count</span>
              <span className="stat-value">{result.total_equipment}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Avg Flowrate</span>
              <span className="stat-value">{result.avg_flowrate.toFixed(2)}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Avg Pressure</span>
              <span className="stat-value">{result.avg_pressure.toFixed(2)}</span>
            </div>
            <div className="stat-card">
              <span className="stat-label">Avg Temp</span>
              <span className="stat-value">{result.avg_temperature.toFixed(2)}</span>
            </div>
          </div>

          <Charts data={result} />
        </div>
      )}
    </div>
  );
}

export default Upload;