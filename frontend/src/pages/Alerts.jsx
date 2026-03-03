import { useEffect, useState } from "react";

function Alerts() {
  const [alerts, setAlerts] = useState([]);

  useEffect(() => {
    const stored = JSON.parse(localStorage.getItem("alerts")) || [];
    setAlerts(stored);
  }, []);

  const clearAlerts = () => {
    localStorage.removeItem("alerts");
    setAlerts([]);
  };

  return (
    <div className="dashboard">
      <div className="header">
        <h1>📄 Alert Summary</h1>
      </div>

      <div className="panel">
        {alerts.length === 0 && <p>No important alerts recorded.</p>}

        {alerts.map((alert, index) => (
          <div
            key={index}
            style={{
              padding: "15px",
              marginBottom: "15px",
              borderBottom: "1px solid rgba(255,255,255,0.2)"
            }}
          >
            <p><strong>Animal:</strong> {alert.animal}</p>
            <p><strong>Confidence:</strong> {(alert.confidence * 100).toFixed(1)}%</p>
            <p><strong>Time:</strong> {alert.time}</p>
          </div>
        ))}

        {alerts.length > 0 && (
          <button
            onClick={clearAlerts}
            style={{
              marginTop: "20px",
              padding: "10px 20px",
              borderRadius: "25px",
              border: "none",
              background: "red",
              color: "white",
              cursor: "pointer"
            }}
          >
            Clear All Alerts
          </button>
        )}
      </div>
    </div>
  );
}

export default Alerts;