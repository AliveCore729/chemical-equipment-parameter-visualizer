import React from "react";
import { Pie, Bar } from "react-chartjs-2";

function Charts({ data }) {
  if (!data) return null;

  // Pie chart data (Equipment types)
  const pieData = {
    labels: Object.keys(data.type_distribution),
    datasets: [
  {
    data: Object.values(data.type_distribution),
    backgroundColor: [
      "#4CAF50",
      "#2196F3",
      "#FF9800",
      "#9C27B0",
      "#F44336",
      "#00BCD4",
    ],
  },
],

  };

  // Bar chart data (Averages)
  const barData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [
  {
    label: "Average Values",
    data: [
      data.avg_flowrate,
      data.avg_pressure,
      data.avg_temperature,
    ],
    backgroundColor: ["#4CAF50", "#FF9800", "#F44336"],
  },
],

  };

  return (
    <div style={{ display: "flex", gap: "50px", flexWrap: "wrap" }}>
  <div style={{ width: "400px" }}>
    <Pie data={pieData} />
  </div>

  <div style={{ width: "500px" }}>
    <Bar data={barData} />
  </div>
</div>

  );
}

export default Charts;
