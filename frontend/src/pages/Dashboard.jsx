import { useState, useRef, useEffect } from "react";
import axios from "axios";
import Particles from "react-tsparticles";

function Dashboard() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [streaming, setStreaming] = useState(false);
  const [detections, setDetections] = useState([]);
  const [status, setStatus] = useState("SAFE");
  const [fps, setFps] = useState(0);
  const [alertCount, setAlertCount] = useState(0);
  const [showPopup, setShowPopup] = useState(false);
  const [lastAnimal, setLastAnimal] = useState(null);

  const BACKEND_URL = "http://127.0.0.1:8000/predict";

  const startCamera = async () => {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoRef.current.srcObject = stream;
    setStreaming(true);
  };

  const stopCamera = () => {
    const tracks = videoRef.current?.srcObject?.getTracks();
    tracks?.forEach(track => track.stop());
    setStreaming(false);
  };

  // Smooth video loop
  useEffect(() => {
    let animationFrameId;
    let lastTime = performance.now();
    let frameCount = 0;

    const draw = () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;

      if (!video || !canvas || !streaming) return;

      const ctx = canvas.getContext("2d");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      ctx.drawImage(video, 0, 0);

      detections.forEach(det => {
        const [x1, y1, x2, y2] = det.box;

        ctx.strokeStyle = "#ff4444";
        ctx.lineWidth = 3;
        ctx.strokeRect(x1, y1, x2 - x1, y2 - y1);

        ctx.fillStyle = "#ff4444";
        ctx.font = "16px Arial";
        ctx.fillText(
          `${det.animal} (${(det.confidence * 100).toFixed(1)}%)`,
          x1,
          y1 - 5
        );
      });

      frameCount++;
      const now = performance.now();
      if (now - lastTime >= 1000) {
        setFps(frameCount);
        frameCount = 0;
        lastTime = now;
      }

      animationFrameId = requestAnimationFrame(draw);
    };

    if (streaming) draw();
    return () => cancelAnimationFrame(animationFrameId);
  }, [streaming, detections]);

  // Detection loop
  useEffect(() => {
    if (!streaming) return;

    const interval = setInterval(async () => {
      const video = videoRef.current;
      if (!video) return;

      const canvas = document.createElement("canvas");
      const ctx = canvas.getContext("2d");

      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0);

      const blob = await new Promise(resolve =>
        canvas.toBlob(resolve, "image/jpeg")
      );

      const formData = new FormData();
      formData.append("file", blob);

      try {
        console.log("Sending frame for detection to:", BACKEND_URL);
        const response = await axios.post(BACKEND_URL, formData);
        const dets = response.data.detections;

        setDetections(dets);

        if (dets.length > 0) {
          setStatus("INTRUSION");
          setAlertCount(prev => prev + 1);
          setLastAnimal(dets[0].animal);
          setShowPopup(true);

          setTimeout(() => setShowPopup(false), 4000);
        } else {
          setStatus("SAFE");
        }
      } catch (err) {
        console.error(err);
      }
    }, 800);

    return () => clearInterval(interval);
  }, [streaming]);

  return (
    <>
      {/* Particle Background */}
      <Particles
        options={{
          background: { color: { value: "transparent" } },
          particles: {
            number: { value: 40 },
            size: { value: 2 },
            move: { enable: true, speed: 0.6 },
            opacity: { value: 0.4 },
            color: { value: "#ffffff" },
          },
        }}
        style={{
          position: "fixed",
          top: 0,
          left: 0,
          width: "100%",
          height: "100%",
          zIndex: 0,
        }}
      />

      <div className="dashboard">
        <div className="header">
          <h1>🌿 WildWatch AI</h1>
          <div className={`status ${status === "SAFE" ? "safe" : "danger"}`}>
            {status}
          </div>
        </div>

        <div className="camera-section">
          {!streaming ? (
            <button onClick={startCamera}>Start Camera</button>
          ) : (
            <button onClick={stopCamera}>Stop Camera</button>
          )}

          <video ref={videoRef} autoPlay style={{ display: "none" }} />

          <div className="camera-wrapper">
            <canvas ref={canvasRef} />
            <div className="radar"></div>
          </div>
        </div>

        <div className="bottom-section">
          <div className="panel">
            <h3>Detected Animals</h3>
            {detections.length === 0 && <p>No detections</p>}
            {detections.map((det, i) => (
              <p key={i}>
                🐾 {det.animal} - {(det.confidence * 100).toFixed(1)}%
              </p>
            ))}
          </div>

          <div className="panel">
            <h3>System Stats</h3>
            <p>FPS: {fps}</p>
            <p>Total Alerts: {alertCount}</p>
            <p>Last Update: {new Date().toLocaleTimeString()}</p>
          </div>
        </div>

        {showPopup && (
          <div className="alert-popup">
            🚨 Intrusion Detected: {lastAnimal?.toUpperCase()}
          </div>
        )}
      </div>
    </>
  );
}

export default Dashboard;