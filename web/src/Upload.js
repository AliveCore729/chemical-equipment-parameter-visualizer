import React, { useState } from "react";
import axios from "axios";
import Charts from "./Charts";

function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadCSV = async () => {
    if (!file) return alert("Select a CSV file");

    const formData = new FormData();
    formData.append("file", file);

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
  };

  return (
    <div>
      <input
        type="file"
        accept=".csv"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button onClick={uploadCSV}>Upload</button>

      {result && (
        <div>
          <h3>Summary</h3>
          <p>Total Equipment: {result.total_equipment}</p>
          <p>Avg Flowrate: {result.avg_flowrate.toFixed(2)}</p>
          <p>Avg Pressure: {result.avg_pressure.toFixed(2)}</p>
          <p>Avg Temperature: {result.avg_temperature.toFixed(2)}</p>
          <Charts data={result} />
        </div>
      )}
    </div>
  );
}

export default Upload;
