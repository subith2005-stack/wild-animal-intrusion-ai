import cv2
from model.detector import detect_ani

def run_live_camera():
    cap = cv2.VideoCapture(0)  # Open the default camera

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return
    
    print("Press 'q' to exit the live camera feed.")

    frame_count = 0
    last_detections = []


    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1

        cv2.imshow("Live Camera Feed", frame)

        if frame_count % 30 == 0:  # Process every 30th frame
            temp_path = "data/sample_images/temp_frame.jpg"
            cv2.imwrite(temp_path, frame)
            last_detections = detect_ani(temp_path)
        
        yield frame, last_detections
            
        cv2.imshow("Live Camera Feed", frame)

        key = cv2.waitKey(10) & 0xFF
        if key == ord('q') or key == ord('Q'):
            print("Exiting live feed...")
            break

    cap.release()   
    cv2.destroyAllWindows()


