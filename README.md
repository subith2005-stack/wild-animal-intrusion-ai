# 🌾 Wild Animal Intrusion Detection System for Crop Protection

An AI-based, real-time, camera-driven early warning system to detect wild animal intrusion into agricultural fields and alert farmers for timely action.

---

## 📌 Problem Statement

Farmers often suffer severe crop losses due to unexpected intrusion of wild animals such as elephants, wild boars, deer, and other large animals.  
Traditional solutions like physical fencing or manual monitoring are costly, labor-intensive, and not always effective.

There is a need for a **lightweight, affordable, real-time, camera-based system** that can automatically detect wild animals and provide **early alerts**, enabling farmers to respond before significant damage occurs.

---

## 🎯 Solution Overview

This project implements a **real-time AI-powered wildlife intrusion detection system** using computer vision.

The system:
- Continuously monitors a **live camera feed**
- Uses a **YOLOv8 deep learning model** to detect animals
- Filters detections to focus only on **wild or harmful animals**
- Displays **live bounding boxes and confidence scores**
- Triggers a **non-spamming early warning alert** when a wild animal enters the scene

The solution is designed to be:
- CPU-friendly
- Edge-device compatible
- Simple to deploy
- Easy to extend

---

## 🧠 Key Features

- ✅ Real-time live camera monitoring
- ✅ AI-based animal detection (YOLOv8)
- ✅ Bounding boxes with labels and confidence scores
- ✅ Smart alert logic (no repeated alert spam)
- ✅ Lightweight and edge-friendly
- ✅ Modular and well-structured codebase
- ✅ Git-based collaboration ready

---

## 🏗️ System Architecture

Live Camera Feed
↓
Frame Capture (Continuous)
↓
AI Inference (YOLOv8 - CPU)
↓
Wild Animal Filtering Logic
↓
State-Based Alert System
↓
Early Warning Notification

yaml
Copy code

---

## 🧩 Project Structure

wild-animal-intrusion-ai/
│── main.py
│── requirements.txt
│── .gitignore
│
├── model/
│ ├── detector.py # YOLO model loading & inference
│ ├── live_camera.py # Live camera frame processing
│ └── video_detector.py # Video file based detection
│
├── alerts/
│ └── alert.py # Alert logic
│
└── data/
└── (ignored - runtime data only)

yaml
Copy code

---

## ⚙️ Technologies Used

- **Language:** Python
- **AI Model:** YOLOv8 (Ultralytics)
- **Computer Vision:** OpenCV
- **Deep Learning Backend:** PyTorch (via Ultralytics)
- **Version Control:** Git & GitHub

---

## 🚀 How It Works

1. The system captures frames from a **live camera feed**
2. Every few frames, AI inference is performed using YOLOv8
3. Detected objects are filtered to identify **wild animals**
4. Bounding boxes and labels are drawn on the live feed
5. When a wild animal is detected:
   - An alert is triggered **only once per intrusion**
   - Alerts reset automatically when the animal leaves

This prevents alert flooding and mimics real-world early warning systems.

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository
```bash
git clone <your-repo-url>
cd wild-animal-intrusion-ai
2️⃣ Create Virtual Environment (Recommended)
bash
Copy code
python -m venv venv
venv\Scripts\activate   # Windows
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
4️⃣ Run Live Camera Detection
bash
Copy code
python main.py
Press Q or ESC to exit the live feed.

🔔 Alert Logic (Important Design Choice)
The system uses state-based alerting:

Alert triggers when a wild animal enters the scene

No repeated alerts while the animal remains

Alert resets when the animal leaves

Alert triggers again if the animal re-enters

This avoids alert spam and reflects real-world surveillance behavior.

⚠️ Dataset & Model Limitations
YOLOv8 (COCO dataset) natively supports elephant

Animals like boar, deer, tiger are not explicitly present

Proxy classes (e.g., large animals) are used for demonstration

👉 In a real deployment, the model would be fine-tuned on a custom wildlife dataset.

🔮 Future Scope
🔹 Custom wildlife dataset training

🔹 SMS / mobile notification alerts

🔹 Multi-camera support

🔹 IoT integration (sirens, lights)

🔹 Night vision / infrared camera support

🔹 Cloud dashboard for monitoring

📜 Disclaimer
This system is intended solely as an assistive early warning mechanism.
It does not guarantee complete prevention of crop damage and does not replace physical fencing, human supervision, or wildlife management policies.

🏁 Conclusion
This project demonstrates how AI and computer vision can be applied practically in agriculture to reduce crop damage and improve farmer safety using simple, efficient, and scalable technology.