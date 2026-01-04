import cv2
from model.detector import detect_ani

def process_video(video_pat):
    cap = cv2.VideoCapture(video_pat)

    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        if frame_count % 30 == 0:  # Process every 30th frame   
            continue

        temp_path = "data/sample_images/temp_frame.jpg"
        cv2.imwrite(temp_path, frame)

        detections = detect_ani(temp_path)

        yield detections


    cap.release()