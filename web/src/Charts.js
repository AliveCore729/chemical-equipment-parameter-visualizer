import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

function Charts({ data }) {
  if (!data) return null;

  // DARK MODE SETTINGS FOR CHARTS
  const darkOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "rgba(255,255,255,0.7)" } // Legend text color
      }
    },
    scales: {
      x: {
        ticks: { color: "rgba(255,255,255,0.6)" },
        grid: { color: "rgba(255,255,255,0.1)" }
      },
      y: {
        ticks: { color: "rgba(255,255,255,0.6)" },
        grid: { color: "rgba(255,255,255,0.1)" }
      }
    }
  };

  const pieOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { labels: { color: "rgba(255,255,255,0.7)" } } }
  };

  // Chart Data with Bright Colors
  const pieData = {
    labels: Object.keys(data.type_distribution),
    datasets: [{
      data: Object.values(data.type_distribution),
      backgroundColor: ["#ff9f43", "#0abde3", "#ee5253", "#10ac84", "#5f27cd"],
      borderColor: "transparent"
    }]
  };

  const barData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [{
      label: "Average Values",
      data: [data.avg_flowrate, data.avg_pressure, data.avg_temperature],
      backgroundColor: ["#10ac84", "#ff9f43", "#ee5253"],
      borderRadius: 5
    }]
  };

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "20px", height: "300px", marginTop: "30px" }}>
      <div style={{ position: "relative" }}>
        <Pie data={pieData} options={pieOptions} />
      </div>
      <div style={{ position: "relative" }}>
        <Bar data={barData} options={darkOptions} />
      </div>
    </div>
  );
}

export default Charts;