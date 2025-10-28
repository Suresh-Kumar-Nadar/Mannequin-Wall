// src/App.jsx
import React from "react";
import CameraCapture from "./CameraCapture";

function App() {
  return (
    <div className="p-4">
      <h1 className="text-xl font-bold mb-4">Face Swap App</h1>
      <CameraCapture />
    </div>
  );
}

export default App;
