import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement,
} from "chart.js";

ChartJS.register(
  ArcElement,
  Tooltip,
  Legend,
  CategoryScale,
  LinearScale,
  BarElement
);

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
