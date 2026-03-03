import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import Alerts from "./pages/Alerts";

function App() {
  return (
    <Router>
      <nav
        style={{
          padding: "20px",
          textAlign: "center",
          background: "rgba(0,0,0,0.5)",
          backdropFilter: "blur(8px)",
        }}
      >
        <Link
          to="/"
          style={{ marginRight: "20px", color: "white", textDecoration: "none" }}
        >
          Dashboard
        </Link>

        <Link
          to="/alerts"
          style={{ color: "white", textDecoration: "none" }}
        >
          Alerts
        </Link>
      </nav>

      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/alerts" element={<Alerts />} />
      </Routes>
    </Router>
  );
}

export default App;