import React from "react";
import { Pie, Bar } from "react-chartjs-2";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement } from "chart.js";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement);

function Charts({ data }) {
  if (!data) return null;

  const darkOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        labels: { color: "rgba(255,255,255,0.7)", font: { family: 'Inter' } } 
      },
      tooltip: {
        backgroundColor: 'rgba(0,0,0,0.8)',
        titleColor: '#fff',
        bodyColor: '#fff',
        borderColor: 'rgba(255,255,255,0.1)',
        borderWidth: 1
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
      plugins: { 
        legend: { 
          position: 'right',
          labels: { color: "rgba(255,255,255,0.7)", padding: 20, font: { family: 'Inter' } } 
        } 
      }
  };

  const pieData = {
    labels: Object.keys(data.type_distribution),
    datasets: [{
      data: Object.values(data.type_distribution),
      backgroundColor: ["#f59e0b", "#10b981", "#3b82f6", "#ef4444", "#8b5cf6"],
      borderColor: "transparent"
    }]
  };

  const barData = {
    labels: ["Flowrate", "Pressure", "Temperature"],
    datasets: [{
      label: "Average Values",
      data: [data.avg_flowrate, data.avg_pressure, data.avg_temperature],
      backgroundColor: ["#10b981", "#f59e0b", "#ef4444"],
      borderRadius: 6
    }]
  };

  return (
    <div className="charts-grid">
      <div className="chart-wrapper">
        <Pie data={pieData} options={pieOptions} />
      </div>
      <div className="chart-wrapper">
        <Bar data={barData} options={darkOptions} />
      </div>
    </div>
  );
}

export default Charts;