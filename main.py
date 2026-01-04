import cv2
from model.live_camera import run_live_camera
from alerts.alert import trigger_alert

wild_animal_classes = ["elephant", "boar", "tiger", "deer"]


animal_present = False # Flag to track if an animal is currently present


for frame,detections in run_live_camera():
    wild_detected = False

    for det in detections:
        name = det["name"]
        confidence = det["confidence"]
        x1, y1, x2, y2 = det["box"]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"{name} {confidence:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 0, 255),
            2,
        )

        if name.lower() in wild_animal_classes and confidence > 0.5:
            wild_detected = True

            if not animal_present:
                trigger_alert(name, confidence)
                animal_present = True
                
    if not wild_detected:
        animal_present = False

    cv2.imshow("Live Camera Feed", frame)