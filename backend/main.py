from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
from detector import detect_animals
from classifier import classify_animal
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (development only)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "WildWatch AI Backend Running"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    detections = detect_animals(frame)

    results = []

    for det in detections:
        x1, y1, x2, y2 = det["box"]

        crop = frame[y1:y2, x1:x2]
        if crop.size == 0:
            continue

        animal, conf = classify_animal(crop)

        results.append({
            "animal": animal,
            "confidence": float(conf),
            "box": [x1, y1, x2, y2]
        })

    return {"detections": results}