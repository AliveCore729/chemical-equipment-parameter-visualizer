import React from "react";
import Upload from "./Upload";
import History from "./History";

function App() {
  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>Chemical Equipment Parameter Visualizer</h1>

      <Upload />
      <History />
    </div>
  );
}

export default App;
