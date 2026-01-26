import React, { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [history, setHistory] = useState([]);

  // --- LOGIC: UNCHANGED ---
  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/api/history/",
          {
            headers: { Authorization: "Token 198094be83d8b909f71a8526901e5f8c4e2d46c7" },
          }
        );
        setHistory(res.data);
      } catch (err) {
        console.error("Error fetching history", err);
      }
    };

    fetchHistory();
  }, []);

  const downloadPDF = async (datasetId, filename) => {
    try {
      const res = await axios.get(
        `http://127.0.0.1:8000/api/report/${datasetId}/`,
        {
          headers: { Authorization: "Token 198094be83d8b909f71a8526901e5f8c4e2d46c7" },
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
  // ------------------------

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

          {/* New Detailed Metrics Layout */}
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