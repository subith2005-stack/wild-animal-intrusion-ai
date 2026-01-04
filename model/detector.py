from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # load a pretrained YOLOv8n model   

def detect_ani(image_path):
    results = model(image_path, verbose=False)  # perform inference on an image
    
    detections = []

    for r in results:
        if r.boxes is None:
            continue
        
        for box in r.boxes:
            cls_id = int(box.cls.item())
            conf = float(box.conf.item())

            class_name = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])

            detections.append({
                "name": class_name,
                "confidence": conf,
                "box": (x1, y1, x2, y2)
            })

    return detections
