import React from "react";
import "./LoadingSpinner.css";

function LoadingSpinner({height}) {
    return (
        <div className="spinner-container" style={{ height: height || "300px" }}>
            <div className="spinner"></div>
        </div>
    );
}

export default LoadingSpinner;