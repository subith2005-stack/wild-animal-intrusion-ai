from ultralytics import YOLO

model = YOLO("yolov8n.pt")

def detect_animals(frame):
    results = model(frame, verbose=False)

    detections = []
    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])        # 🔥 ADD THIS
            conf = float(box.conf[0])
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "box": (x1, y1, x2, y2),
                "confidence": conf,
                "cls_id": cls_id             # 🔥 ADD THIS
            })

    return detections

