# 🌿 WATCHEROO - Wild Animal Intrusion Detection System

[![Domain: Agriculture & Wildlife Management](https://img.shields.io/badge/Domain-Agriculture%20%26%20Wildlife%20Management-2e7d32.svg)](#)
[![Backend: FastAPI](https://img.shields.io/badge/Backend-FastAPI%20%7C%20Python-009688.svg)](#)
[![Frontend: React + Vite](https://img.shields.io/badge/Frontend-React%2019%20%7C%20Vite-61dafb.svg)](#)
[![Model: Ultralytics YOLOv8](https://img.shields.io/badge/Model-Custom%20YOLOv8-blue.svg)](#)

---

## 1. Project Title & Overview

**Project Name:** WATCHEROO  
**Project Type:** Real-Time Wild Animal Intrusion Detection System  
**Domain:** Agriculture & Wildlife Management  

**WATCHEROO** is an automated, real-time wild animal intrusion detection and alert system designed to mitigate human-wildlife conflict and protect agricultural fields from crop raiding. Built on a decoupled client-server architecture, the system captures live video feeds via a modern browser-based React dashboard, processes incoming frames through a custom-trained **YOLOv8** object detection model hosted on a **FastAPI** backend, and initiates dual-channel alerts:
1. **Local Acoustic Alarm:** Instant sound playback (`alarm.wav`) on the monitoring workstation to provide a local audible warning and alert local personnel.
2. **Remote Mobile Notification:** Automated SMS dispatch via the **Twilio REST API** to warn farmers or forest rangers of impending intrusions.

---

## 2. Problem Statement

Agricultural farmlands situated near forest borders and wildlife corridors face recurring crop raids by wild animals such as elephants, tigers, bears, and deer. These intrusions cause:
- **Catastrophic Economic Losses:** Massive damage to standing crops, farm infrastructure, and seasonal yields.
- **Human-Wildlife Conflict:** Severe risks to the safety and lives of farmers and agricultural workers.
- **Ecological Consequences:** Retaliatory harm to endangered wild animals due to crude deterrence methods (e.g., unauthorized electric fencing or poisons).
- **Ineffective Traditional Guarding:** Manual night guarding is hazardous, labor-intensive, and prone to fatigue and human error.

### The WATCHEROO Solution
WATCHEROO provides an **assistive, non-invasive early warning system**. By continuously analyzing camera feeds with computer vision, WATCHEROO detects target wild animals the moment they approach the farm boundary, instantly alerting farmers locally and remotely so preventive deterrence can be executed safely and proactively.

---

## 3. Current System Architecture

The current WATCHEROO architecture is structured as a decoupled, real-time client-server pipeline:

```
┌─────────────────────────────────────────────────────────┐
│                      CAMERA FEED                        │
│            (Client Webcam / Browser Capture)            │
└───────────────────────────┬─────────────────────────────┘
                            │
                            │ Frame Snapshots (JPEG)
                            │ HTTP POST /predict (every 800ms)
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     FASTAPI BACKEND                     │
│                (backend/main.py :8000)                  │
│                                                         │
│  1. Decode image buffer via OpenCV (BGR NumPy array)    │
│  2. Run Custom YOLOv8 inference (imgsz=416)             │
│  3. Filter detections for Target Animals                │
│     [Tiger, Bear, Elephant, Deer]                       │
└─────────────┬─────────────────────────────┬─────────────┘
              │                             │
              │ Detection JSON              │ Intrusion Trigger
              │ (Boxes, Labels, Conf)       │ (First occurrence in session)
              ▼                             ▼
┌───────────────────────────┐ ┌───────────────────────────┐
│      REACT DASHBOARD      │ │       ALERT SYSTEM        │
│   (frontend/src :5173)    │ │                           │
│                           │ │  1. Local Windows Alarm   │
│ • Real-time Canvas Feed   │ │     (alarm.py + winsound) │
│ • Bounding Box Overlays   │ │     (Plays alarm.wav)     │
│ • SAFE / INTRUSION Badge  │ │                           │
│ • Radar Sweep Animation   │ │  2. Twilio SMS Gateway    │
│ • Live FPS & Alert Count  │ │     (sms_alerts.py)       │
│ • Species History Logs    │ │     (SMS dispatched)      │
└───────────────────────────┘ └───────────────────────────┘
```

### Architectural Workflow
1. **Video Ingestion:** The React frontend captures video frames from the user's camera feed using HTML5 Canvas (`toBlob` as JPEG).
2. **API Communication:** Frames are transmitted asynchronously every 800ms to the FastAPI `/predict` endpoint via Axios multipart `FormData`.
3. **Model Inference:** The backend decodes the frame with OpenCV and executes custom YOLOv8 model inference at a resolution of 416x416 pixels.
4. **Target Animal Filtering:** Detections are filtered against the target species list (`Tiger`, `Bear`, `Elephant`, `Deer`).
5. **Telemetry Response:** Detected bounding box coordinates, confidence scores, and animal labels are returned to the frontend for real-time visualization.
6. **Multi-Modal Alert Execution:** If a target animal is confirmed and has not already been alerted during the current backend session, the backend simultaneously triggers the local acoustic alarm and dispatches a Twilio SMS notification.

---

## 4. Current Detection Model

WATCHEROO uses a single-stage, custom-trained **YOLOv8** (Ultralytics) object detection model.

- **Model Weights File:** `backend/wildwatch_yolo.pt`
- **Inference Configuration:** Executed via `yolo_model(frame, imgsz=416)`
- **Dataset Scope:** Trained on a 54-class wildlife dataset (`data.yaml` comprising mammals, reptiles, birds, and insects).
- **Target Species Filter:** The production application selectively filters detections for four primary agricultural conflict animals:
  - 🐯 **Tiger**
  - 🐻 **Bear**
  - 🐘 **Elephant**
  - 🦌 **Deer**

> [!IMPORTANT]
> **Model File Excluded from Git:**  
> The model weight file `backend/wildwatch_yolo.pt` is ignored by Git in `.gitignore` under the rule `*.pt`. The model weights are not hosted directly in this repository. Users must place their trained `wildwatch_yolo.pt` model file inside the `backend/` directory prior to running the backend.

---

## 5. Technology Stack

### Backend
- **Language:** Python 3.10+
- **API Framework:** FastAPI (`fastapi`)
- **ASGI Server:** Uvicorn (`uvicorn`)
- **Deep Learning Framework:** PyTorch (`torch`, `torchvision`)
- **Computer Vision:** Ultralytics YOLO (`ultralytics`), OpenCV (`opencv-python`)
- **Numerical Operations:** NumPy (`numpy`)
- **Messaging & Notifications:** Twilio Python Helper Library (`twilio`)
- **Environment Management:** `python-dotenv`
- **System Audio:** `winsound` (Native Windows multimedia audio API)

### Frontend
- **Library:** React 19 (`react`, `react-dom`)
- **Build Tool / Dev Server:** Vite 7 (`vite`, `@vitejs/plugin-react`)
- **Routing:** React Router DOM v7 (`react-router-dom`)
- **HTTP Client:** Axios (`axios`)
- **Visual Effects:** `react-tsparticles` & `tsparticles` (Ambient particle background)
- **Styling:** Vanilla CSS3 with Glassmorphism, CSS radar sweep keyframes, responsive flex/grid layouts

---

## 6. Current Folder Structure

Below is the verified repository structure reflecting all active files:

```
wild-animal-intrusion-ai/
├── .env                              # Environment variables (Twilio credentials - NOT in git)
├── .gitignore                        # Git exclusion rules (*.pt, .env, venv, runs, etc.)
├── README.md                         # Comprehensive project documentation
├── requirements.txt                  # Python dependencies
├── alarm.py                          # Local audio alarm trigger using winsound
├── alarm.wav                         # Audio sound file for the local audible warning.
├── alerts/
│   ├── alert.py                      # Console-based alert logger utility
│   └── sms_alerts.py                 # Twilio REST API client for dispatching SMS notifications
├── backend/
│   ├── main.py                       # FastAPI application, YOLO model loader, /predict route
│   └── wildwatch_yolo.pt             # Custom YOLOv8 weights (Local only, ignored by Git)
└── frontend/
    ├── .gitignore                    # Frontend build & dependency ignore rules
    ├── README.md                     # Vite template documentation
    ├── eslint.config.js              # ESLint configuration
    ├── index.html                    # Single Page Application HTML template
    ├── package.json                  # Node.js dependencies and script definitions
    ├── package-lock.json             # NPM dependency lockfile
    ├── vite.config.js                # Vite build and plugin configuration
    ├── public/
    │   ├── forest-bg.jpg             # High-resolution dashboard background image
    │   └── vite.svg                  # Vite branding asset
    └── src/
        ├── App.css                   # Custom styles (glassmorphism cards, radar, alert badge)
        ├── App.jsx                   # Navigation bar and route configuration (/ and /alerts)
        ├── index.css                 # Global CSS resets
        ├── main.jsx                  # React application root mount
        ├── assets/
        │   └── react.svg             # React branding asset
        └── pages/
            ├── Alerts.jsx            # Persistent alert history view with clear functionality
            └── Dashboard.jsx         # Live camera stream, Canvas bounding boxes, radar, stats
```

---

## 7. Important File Descriptions

| File Path | Description |
|---|---|
| `backend/main.py` | Core FastAPI application. Initializes CORS middleware, loads `backend/wildwatch_yolo.pt`, defines the `/predict` POST endpoint, decodes image files, filters target animal classes, and orchestrates alert calls. |
| `alerts/sms_alerts.py` | Houses `send_sms()`, which loads Twilio credentials from `.env` and uses the Twilio REST API client to send intrusion alert messages to registered recipient phone numbers. |
| `alarm.py` | Houses `play_alarm()`, which asynchronously triggers playback of `alarm.wav` on the host machine using Python's native `winsound` library. |
| `alarm.wav` | Audio sound file played whenever a target animal intrusion is detected. |
| `alerts/alert.py` | Utility function `trigger_alert()` that formats and prints intrusion telemetry (timestamp, animal type, confidence) to the console. |
| `frontend/src/pages/Dashboard.jsx` | Main monitoring dashboard. Manages browser webcam capture using HTML5 video/canvas, draws real-time bounding boxes on an HTML5 canvas overlay, sends periodic JPEG frame uploads to the backend every 800ms, calculates live FPS, and displays system status badges. |
| `frontend/src/pages/Alerts.jsx` | Secondary view accessible via top navigation. Reads recorded intrusion alerts from `localStorage`, displays formatted alert cards, and provides a "Clear All Alerts" button. |
| `frontend/src/App.jsx` | Application router configuring navigation links between the live monitoring `Dashboard` and historical `Alerts` page. |
| `requirements.txt` | Python package specification for FastAPI, Ultralytics, PyTorch, OpenCV, NumPy, Twilio, and supporting libraries. |
| `.gitignore` | Prevents temporary files, caches, virtual environments, `.env` files, dataset directories, training runs, and large binary weight files (`*.pt`) from being committed to version control. |

---

## 8. Detection and Alert Workflow

The complete end-to-end detection and alert lifecycle proceeds as follows:

```
[Webcam Stream] ──(requestAnimationFrame)──> [Canvas Overlay at 640x480]
                                                       │
                     Every 800ms Interval Snapshot     ▼
                                             [FormData (image/jpeg)]
                                                       │
                                   HTTP POST /predict  ▼
                                            [FastAPI Backend]
                                                       │
                                    OpenCV Decode Frame BGR
                                                       │
                                     YOLOv8 Inference (416px)
                                                       │
                                     Extract Boxes, Labels, Conf
                                                       │
                                        Is Label in Target List?
                                        [Tiger, Bear, Elephant, Deer]
                                           /                       \
                                         YES                        NO
                                         /                            \
                     Check Session Deduplication Set               Ignore
                     (animal not in alerted_animals)                     │
                             /            \                              │
                           YES             NO (Already alerted)          │
                           /                \                            │
             ┌────────────┴────────────┐     \                           │
             ▼                         ▼      \                          │
     [Local Alarm]              [Twilio SMS]   \                         │
    play_alarm() (winsound)     send_sms()      \                        │
             │                         │         │                       │
             └────────────┬────────────┘         │                       │
                          ▼                      │                       │
               alerted_animals.add(animal)       │                       │
                          │                      │                       │
                          └──────────┬───────────┘                       │
                                     ▼                                   ▼
                         Return JSON Detections ─────────────> [React Dashboard]
                                                               • Render Red Box & Label
                                                               • Status: INTRUSION
                                                               • Increment Alert Counter
                                                               • Display Warning Popup
```

1. **Client Frame Capture:** In `Dashboard.jsx`, an interval triggers every 800 milliseconds, drawing the current video frame onto an off-screen HTML5 Canvas and serializing it into an image blob (`image/jpeg`).
2. **Payload Transmission:** The blob is packaged into a `FormData` object under the field key `file` and sent via `axios.post("http://127.0.0.1:8000/predict", formData)`.
3. **Frame Processing:** FastAPI receives the `UploadFile`, reads bytes asynchronously, and decodes the image with `cv2.imdecode(np.frombuffer(contents, np.uint8), cv2.IMREAD_COLOR)`.
4. **YOLOv8 Model Inference:** The frame is passed through `yolo_model(frame, imgsz=416)`.
5. **Species Verification:** Each detected bounding box is evaluated against the target classes:
   ```python
   if label in ["Tiger", "Bear", "Elephant", "Deer"]:
       detections.append({
           "animal": label,
           "confidence": float(box.conf[0]),
           "box": [x1, y1, x2, y2]
       })
   ```
6. **Multi-Modal Alerting:** If detections exist and the detected animal species has not yet been notified during this server session:
   - `play_alarm()` executes asynchronously.
   - `send_sms()` dispatches the SMS alert.
   - The animal is added to `alerted_animals`.
7. **Frontend Visualization:** The client receives `{ detections: [...] }`, draws red bounding boxes with labels and percentages onto the live canvas overlay, sets the status banner to `INTRUSION`, increments the alert counter, and displays a temporary intrusion alert banner.

---

## 9. Duplicate Alert Prevention

In agricultural surveillance, wild animals often remain within the camera frame for extended periods (seconds to minutes). Without deduplication, an 800ms polling loop would trigger dozens of siren plays and hundreds of costly SMS messages for a single intrusion event.

WATCHEROO implements **session-based duplicate alert prevention**:
- In `backend/main.py`, a global set tracks alerted species:
  ```python
  alerted_animals = set()
  ```
- Before triggering alarms or sending an SMS, the backend checks:
  ```python
  if detections:
      animal = detections[0]["animal"]
      if animal not in alerted_animals:
          play_alarm()
          send_sms()
          alerted_animals.add(animal)
  ```
- **Behavioral Result:**
  - When an animal (e.g., "Elephant") first appears, the local sound plays and an SMS alert is sent immediately.
  - As long as the elephant stays in frame, subsequent frames continue to receive bounding box updates on the dashboard without re-triggering the alarm sound or sending duplicate SMS messages.
  - If a different target animal enters the frame (e.g., "Tiger"), the system recognizes that "Tiger" is not in `alerted_animals` and triggers the alerts for the new threat.

---

## 10. Local Alarm Functionality

The local acoustic alarm provides an on-site audible warning:
- **Module:** `alarm.py`
- **Implementation:**
  ```python
  import winsound

  def play_alarm():
      try:
          winsound.PlaySound("alarm.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
      except Exception as e:
          print("Alarm error:", e)
  ```
- **Non-Blocking Operation:** The `winsound.SND_ASYNC` flag ensures the audio file plays in the background without blocking the Python execution thread or delaying FastAPI HTTP response cycles.
- **Platform Scope:** Built for Windows host systems using Python's standard `winsound` library.

---

## 11. Twilio SMS Functionality

Remote mobile alerting is handled by Twilio:
- **Module:** `alerts/sms_alerts.py`
- **Mechanism:** Integrates `twilio.rest.Client` to dispatch an SMS message when an intrusion occurs.
- **Configuration:** Credentials are read from environment variables via `python-dotenv`:
  - `TWILIO_ACCOUNT_SID`
  - `TWILIO_AUTH_TOKEN`
- **Security Rule:** Never commit real credentials to GitHub. Always store them in a local, uncommitted `.env` file.

```
┌─────────────────┐       HTTPS REST API       ┌──────────────────┐       Cellular SMS       ┌──────────────────┐
│  FastAPI Server │ ─────────────────────────> │  Twilio Gateway  │ ───────────────────────> │  Farmer's Phone  │
│ (sms_alerts.py) │   Auth SID + Auth Token    │   Cloud Server   │   "Intrusion Alert"      │   (Destination)  │
└─────────────────┘                            └──────────────────┘                          └──────────────────┘
```

---

## 12. Installation Requirements

Before setting up the project, ensure you have the following installed:
- **Operating System:** Windows 10/11 (required for native `winsound` local alarm support)
- **Python:** Version 3.10+ (64-bit recommended)
- **Node.js:** Version 18.x or 20.x+ with `npm`
- **Hardware:** Standard webcam or USB camera for video capture
- **Accounts (Optional for SMS):** Active Twilio account with an SMS-enabled virtual number

---

## 13. Python Virtual Environment Setup

Open **PowerShell** or **Command Prompt** in the project root directory:

```powershell
# Navigate to the project root
cd path\to\wild-animal-intrusion-ai

# Create a virtual environment named 'venv'
python -m venv venv

# Activate the virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1

# On Windows Command Prompt (CMD):
.\venv\Scripts\activate.bat
```

> [!TIP]
> If PowerShell blocks script execution, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in your PowerShell window.

---

## 14. Python Dependency Installation

With your virtual environment activated, install all backend dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

Verify the key packages are installed:
```powershell
python -c "import fastapi, uvicorn, ultralytics, torch, cv2, twilio; print('All core backend modules loaded successfully!')"
```

---

## 15. Frontend Dependency Installation

Open a separate terminal window and install the required Node.js packages:

```powershell
# Navigate to the frontend directory
cd frontend

# Install all npm dependencies
npm install
```

This installs React 19, Vite, Axios, React Router DOM, and tsparticles as specified in `frontend/package.json`.

---

## 16. Model Setup

The trained detection model is excluded from Git via `.gitignore`. You must obtain or train the weights and place them into the `backend/` directory:

1. Locate your trained YOLOv8 model weights file (`wildwatch_yolo.pt`).
2. Copy the file into the `backend/` directory:
   ```
   wild-animal-intrusion-ai/
   └── backend/
       └── wildwatch_yolo.pt
   ```
3. Ensure the filename matches exactly: `wildwatch_yolo.pt`. `backend/main.py` directly references:
   ```python
   yolo_model = YOLO("backend/wildwatch_yolo.pt")
   ```

---

## 17. How to Run the FastAPI Backend

1. Create a `.env` file in the root directory for Twilio credentials (if using SMS alerts):
   ```env
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   ```
2. Activate your Python virtual environment:
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```
3. Launch the FastAPI server with Uvicorn from the project root:
   ```powershell
   uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
   ```
4. Verify the backend is operational:
   - Terminal will display: `Application startup complete. Uvicorn running on http://127.0.0.1:8000`
   - Interactive API documentation can be accessed at: `http://127.0.0.1:8000/docs`

---

## 18. How to Run the React/Vite Frontend

1. Open a new terminal and navigate to the `frontend` folder:
   ```powershell
   cd frontend
   ```
2. Start the Vite development server:
   ```powershell
   npm run dev
   ```
3. Open your browser and navigate to:
   ```
   http://localhost:5173
   ```
4. Grant the browser permission to access your webcam when prompted.

---

## 19. Dashboard Features

The WATCHEROO frontend dashboard provides a comprehensive monitoring interface:

- **Live Video & Canvas Overlays:** Displays the webcam feed locally in the browser while periodic JPEG snapshots are sent to the backend, and dynamically draws red bounding boxes around detected target animals along with confidence percentages (e.g., `Elephant (94.2%)`).
- **Real-Time Status Indicator:** Prominently displays a green `SAFE` badge during normal operations, switching immediately to a flashing red `INTRUSION` badge when a target animal is detected.
- **Radar Scanner Animation:** A green rotating radar sweep is positioned over the camera feed, providing a clear visual indication of active surveillance.
- **Live System Telemetry:** Real-time metrics tracking:
  - Current inference FPS (Frames Per Second).
  - The dashboard's detection/alert counter for the monitoring session.
  - Real-time timestamp of the last frame evaluated.
- **Intrusion Warning Popup:** A temporary modal banner (`🚨 Intrusion Detected: [ANIMAL]`) flashes at the bottom of the screen upon detection.
- **Multi-Page Routing:** Seamless navigation using React Router:
  - `/`: Primary Live Monitoring Dashboard.
  - `/alerts`: Dedicated Alert History view with stored entries and a "Clear All Alerts" action.
- **Modern Glassmorphism Design:** Dark-themed aesthetic featuring semi-transparent frosted glass cards, subtle typography, and a dynamic particle background.

---

## 20. Development Evolution / Project Progression

The development of WATCHEROO progressed across distinct engineering phases during the hackathon lifecycle:

```
[Phase 1: Initial Prototype]
  • Streamlit monolithic application (app.py)
  • Generic object detection prototype
       │
       ▼
[Phase 2: Two-Stage Classification Experiment]
  • YOLOv8 detection + cropped ResNet-18 classification (animal_classifier.pt)
  • Issues: Two-stage latency overhead, noise in cropped frames, fragile pipeline
       │
       ▼
[Phase 3: Unified Custom YOLOv8 Model]
  • Trained unified custom YOLOv8 model on a 54-class wildlife dataset
  • Direct bounding box localization and species identification in a single pass
  • Production filter focused on 4 target intrusion species: Tiger, Bear, Elephant, Deer
       │
       ▼
[Phase 4: Modern Decoupled Architecture (Current)]
  • Removed legacy scripts (app.py, main.py, classifier.py, detector.py, ResNet-18)
  • Built FastAPI REST backend
  • Developed responsive React 19 + Vite dashboard with browser webcam capture using HTML5 video/canvas and periodic JPEG frame uploads to the FastAPI backend
  • Implemented dual-channel alert dispatch (local winsound alarm + Twilio SMS)
  • Added session-based alert deduplication to prevent notification spam
```

### Deprecated Components Cleaned Up in Current Release
To maintain a clean and maintainable codebase, legacy components from earlier iterations were removed during the current cleanup:
- `app.py`: Legacy Streamlit application.
- `main.py`: Legacy standalone console script.
- `backend/classifier.py`: Legacy PyTorch ResNet-18 image classification module.
- `backend/detector.py`: Legacy YOLO bounding box extractor.
- `model/live_camera.py`: Deprecated OpenCV camera loop.
- `model/video_detector.py`: Deprecated offline video detector.
- `ml/train_classifier.py`: Deprecated ResNet-18 classifier training script.

---

## 21. Current Limitations

While WATCHEROO functions as a working prototype, several limitations exist in the current implementation:
- **Client-Side Camera Dependence:** The video feed is captured via browser webcam capture using HTML5 video/canvas and periodic JPEG frame uploads to the FastAPI backend rather than an IP camera or RTSP server directly ingested by the backend.
- **In-Memory Session Deduplication:** The `alerted_animals` set resides in backend server memory; restarting the server process resets the deduplication state.
- **Platform-Specific Local Audio:** `alarm.py` utilizes Windows-native `winsound`. Running the local alarm on Linux or macOS requires a cross-platform audio library (such as `pygame` or `playsound`).
- **Fixed Polling Cadence:** The frontend captures and posts frames at a fixed 800ms interval rather than a dynamic, event-driven stream.
- **Single Camera Node:** The current dashboard handles a single camera feed at a time.

---

## 22. Future Enhancements

- **Direct RTSP / IP Camera Ingestion:** Ingest multi-camera RTSP feeds directly within the FastAPI backend using OpenCV or GStreamer pipelines.
- **WebSocket Streaming:** Replace 800ms HTTP polling with full-duplex WebSockets for lower latency and continuous frame streaming.
- **Persistent Database & Analytics:** Integrate SQLite or PostgreSQL to record timestamped intrusion logs, capture incident snapshots, and plot historical invasion trends.
- **Edge Deployment Optimization:** Export the custom YOLOv8 model to TensorRT or ONNX Runtime for low-power edge gateways (e.g., NVIDIA Jetson or Raspberry Pi with AI accelerators).
- **Physical Deterrent Integration:** Connect relay modules or IoT microcontrollers (ESP32 / Arduino) to trigger physical strobe lights, water sprinklers, or ultrasonic sound repellents.
- **Multi-Channel Alerts:** Expand notifications to WhatsApp, Telegram bots, and automated voice phone calls.

---

## 23. Disclaimer

> [!WARNING]
> **Assistive Warning System Only:**  
> WATCHEROO is an early warning and monitoring tool intended to assist agricultural landholders and forest boundary monitors. It is **not** a replacement for primary physical barriers, electric fencing, or official wildlife management protocols.
> 
> Detection accuracy may vary depending on ambient illumination, camera angle, resolution, weather conditions (such as heavy rain or fog), and partial animal occlusion. Always exercise extreme caution in areas known for dangerous wildlife encounters.

---

## 24. Demo Video Section

A video walkthrough showing WATCHEROO in action is available at the link below:

🎥 **[Watch the Project Demo Video](https://drive.google.com/file/d/1n4cYSlPyXLr7SI0vAVhg8vKrGJVlB8Og/view?usp=sharing)**

---

## 25. Current Project Status

- **Status:** Functional Prototype / Working MVP
- **Evaluation Readiness:** Ready for demonstration, testing, and evaluation.
