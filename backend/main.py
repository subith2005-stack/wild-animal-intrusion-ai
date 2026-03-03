from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import cv2
from ultralytics import YOLO
from backend.classifier import classify_animal

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
yolo_model = YOLO("yolov8n.pt")

WILD_ANIMAL_CLASSES = ["bear", "deer", "elephant", "tiger", "wild_boar"]
CONFIDENCE_THRESHOLD = 0.7


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    np_img = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

    results = yolo_model(frame)

    detections = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            cls_id = int(box.cls[0])
            label = yolo_model.names[cls_id]

            if label in WILD_ANIMAL_CLASSES:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cropped = frame[y1:y2, x1:x2]
                animal_name, ml_conf = classify_animal(cropped)

                if animal_name != "unknown" and ml_conf >= CONFIDENCE_THRESHOLD:
                    detections.append({
                        "animal": animal_name,
                        "confidence": ml_conf,
                        "box": [x1, y1, x2, y2]
                    })

    return {"detections": detections}