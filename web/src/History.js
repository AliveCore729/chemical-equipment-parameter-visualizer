import React, { useEffect, useState } from "react";
import axios from "axios";

function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const res = await axios.get(
          "http://127.0.0.1:8000/api/history/",
          {
            headers: {
              Authorization: "Token 198094be83d8b909f71a8526901e5f8c4e2d46c7",
            },
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
          headers: {
            Authorization: "Token 198094be83d8b909f71a8526901e5f8c4e2d46c7",
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
    <div style={{ marginTop: "40px" }}>
      <h2>Upload History (Last 5)</h2>

      {history.length === 0 && <p>No history available.</p>}

      {history.map((item, index) => (
        <div
          key={index}
          style={{
            border: "1px solid #ccc",
            padding: "15px",
            marginBottom: "15px",
            borderRadius: "6px",
          }}
        >
          <h4>{item.filename}</h4>
          <p><b>Uploaded at:</b> {new Date(item.uploaded_at).toLocaleString()}</p>
          <p>Total Equipment: {item.total_equipment}</p>
          <p>Avg Flowrate: {item.avg_flowrate.toFixed(2)}</p>
          <p>Avg Pressure: {item.avg_pressure.toFixed(2)}</p>
          <p>Avg Temperature: {item.avg_temperature.toFixed(2)}</p>
          
          <button onClick={() => downloadPDF(item.id, item.filename)}>
            Download PDF
          </button>
        </div>
      ))}
    </div>
  );
}

export default History;
