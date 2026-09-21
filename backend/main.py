from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from ultralytics import YOLO
from backend.classifier import classify_animal
from alerts.sms_alerts import send_sms

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load YOLO model
yolo_model = YOLO("backend/wildwatch_yolo.pt")

WILD_ANIMAL_CLASSES = ["bear", "deer", "elephant", "tiger", "wild_boar"]
CONFIDENCE_THRESHOLD = 0.7

alerted_animals = set()


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    global alert_sent
    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = yolo_model(frame, imgsz=416)

    detections = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls_id = int(box.cls[0])
            label = yolo_model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            pad = 20

            x1 = max(0, x1 - pad)
            y1 = max(0, y1 - pad)
            x2 = min(frame.shape[1], x2 + pad)
            y2 = min(frame.shape[0], y2 + pad)

            cropped = frame[y1:y2, x1:x2]
            # animal_name, ml_conf = classify_animal(cropped)
    
            if label in ["Tiger", "Bear", "Elephant", "Deer"]:
                detections.append({
                "animal": label,
                "confidence": float(box.conf[0]),
                "box": [x1, y1, x2, y2]
            })

    if detections:
        animal = detections[0]["animal"]

        if animal not in alerted_animals:
            send_sms()
            alerted_animals.add(animal)

    return {"detections": detections}