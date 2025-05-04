// Popup.jsx
import React from "react";
import "./Popup.css";

function Popup({ message, onClose }) {
  return (
    <div className="popup-overlay">
      <div className="popup-box">
        <p>{message}</p>
        <button onClick={onClose}>Close</button>
      </div>
    </div>
  );
}

export default Popup;
