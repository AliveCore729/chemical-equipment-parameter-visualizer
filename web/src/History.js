import React, { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [history, setHistory] = useState([]);

  const API_URL = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
  const TOKEN = process.env.REACT_APP_API_TOKEN;

  useEffect(() => {
    const fetchHistory = async () => {
      if (!TOKEN) {
        console.warn("API Token is missing. Please check your .env file.");
        return;
      }

      try {
        const res = await axios.get(
          `${API_URL}/api/history/`,
          {
            headers: { 
              Authorization: `Token ${TOKEN}`
            },
          }
        );
        setHistory(res.data);
      } catch (err) {
        console.error("Error fetching history", err);
      }
    };

    fetchHistory();
  }, [API_URL, TOKEN]);

  const downloadPDF = async (datasetId, filename) => {
    if (!TOKEN) {
      alert("Authentication Error: Token missing.");
      return;
    }

    try {
      const res = await axios.get(
        `${API_URL}/api/report/${datasetId}/`, 
        {
          headers: { 
            Authorization: `Token ${TOKEN}` 
          },
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", `${filename}_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      console.error("PDF download failed", err);
      alert("Failed to download PDF");
    }
  };

  return (
    <div className="glass-panel" style={{ minHeight: '100%' }}>
      <h2 className="section-title">Recent Activity</h2>

      {history.length === 0 && (
        <p style={{ color: 'rgba(255,255,255,0.4)', textAlign: 'center' }}>
          No uploads found.
        </p>
      )}

      {history.map((item, index) => (
        <div key={index} className="history-item">
          {/* Header: Filename and Date */}
          <div className="history-header">
            <span className="history-filename" style={{ wordBreak: 'break-all' }}>
              {item.filename}
            </span>
            <span className="history-meta" style={{ minWidth: 'fit-content' }}>
              {new Date(item.uploaded_at).toLocaleDateString()}
            </span>
          </div>

          {/* Detailed Metrics Layout */}
          <div style={{ marginBottom: '15px' }}>
            
            {/* Equipment Count Row */}
            <div style={{ fontSize: '0.85rem', color: 'rgba(255,255,255,0.6)', marginBottom: '8px' }}>
              Equipment Count: <strong style={{ color: '#fff' }}>{item.total_equipment}</strong>
            </div>

            {/* 3-Column Grid for Averages */}
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: '1fr 1fr 1fr', 
              gap: '5px', 
              background: 'rgba(0,0,0,0.2)', 
              padding: '10px', 
              borderRadius: '8px',
              textAlign: 'center'
            }}>
              {/* Flowrate */}
              <div>
                <span style={{ display: 'block', fontSize: '0.7rem', color: '#94a3b8', marginBottom: '2px' }}>FLOW</span>
                <span style={{ fontWeight: '600', color: '#10b981', fontSize: '0.9rem' }}>
                  {item.avg_flowrate.toFixed(1)}
                </span>
              </div>
              
              {/* Pressure */}
              <div>
                <span style={{ display: 'block', fontSize: '0.7rem', color: '#94a3b8', marginBottom: '2px' }}>PRESS</span>
                <span style={{ fontWeight: '600', color: '#f59e0b', fontSize: '0.9rem' }}>
                  {item.avg_pressure.toFixed(1)}
                </span>
              </div>
              
              {/* Temperature */}
              <div>
                <span style={{ display: 'block', fontSize: '0.7rem', color: '#94a3b8', marginBottom: '2px' }}>TEMP</span>
                <span style={{ fontWeight: '600', color: '#ef4444', fontSize: '0.9rem' }}>
                  {item.avg_temperature.toFixed(1)}
                </span>
              </div>
            </div>

          </div>
          
          {/* Action Button */}
          <button 
            onClick={() => downloadPDF(item.id, item.filename)}
            className="btn-glass"
          >
            Download Report PDF
          </button>
        </div>
      ))}
    </div>
  );
}

export default History;