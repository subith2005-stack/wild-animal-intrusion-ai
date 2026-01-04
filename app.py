import streamlit as st
import cv2
import time
from datetime import datetime
from alerts.sms_alerts import send_sms

from model.detector import detect_ani
from alerts.alert import trigger_alert

#------------Configuration------------#

farmer_phone_number = "+918921828286"

wild_animals = ["elephant", "tiger", "boar", "deer"]
conf_threshold = 0.5

st.set_page_config(
    page_title="Wild Animal Intrusion Detection",
    page_icon=":lion_face:",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("Wild Animal Intrusion Detection System")
st.write(
    "AI-based real-time early warning system to detect wild animals "
    "intruding into agricultural fields."
)

#------------Session State Initialization------------#
if "run" not in st.session_state:
    st.session_state.run = False

if "animal_detected" not in st.session_state:
    st.session_state.animal_detected = False

if "alert_count" not in st.session_state:
    st.session_state.alert_count = 0

if "last_alert_time" not in st.session_state:
    st.session_state.last_alert_time = None

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

#---------------Functions (Buttons)---------------#
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Detection"):
        st.session_state.run = True
        st.session_state.animal_detected = False
with col2:
    if st.button("⏸ Stop Detection"):
        st.session_state.run = False


#---------------Placeholder---------------#
frame_placeholder = st.empty()
status_placeholder = st.empty()


#---------------Live Camera Feed---------------#
if st.session_state.run:
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        st.error("Error: Could not open webcam.")
    else:
        frame_count = 0
        last_detections = []

        while st.session_state.run:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1

            if frame_count % 30 == 0:
                temp_path = "data/sample_images/temp_frame.jpg"
                cv2.imwrite(temp_path, frame)
                last_detections = detect_ani(temp_path)

            wild_detected = False

            for det in last_detections:
                name = det["name"]
                conf = det["confidence"]
                x1, y1, x2, y2 = det["box"]

                color = (0, 0, 255) if name.lower() in wild_animals else (0, 255, 0)

                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv2.putText(
                    frame,
                    f"{name} {conf:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2,

                )
                
                if name.lower() in wild_animals and conf >=  conf_threshold:
                    wild_detected = True
                    if not st.session_state.animal_detected:
                        trigger_alert(name, conf)
                        st.session_state.animal_detected = True 

                        alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        send_sms(
                            to_number=farmer_phone_number,
                            animal_name=name,
                            confidence=conf,
                            
                            time=alert_time,
                            )

                        st.session_state.alert_count += 1
                        st.session_state.last_alert_time = alert_time
                        st.session_state.alert_log.append(
                            {
                                "time": alert_time,
                                "animal": name,
                                "confidence": conf,
                            }
                        )
            
            if not wild_detected:
                st.session_state.animal_detected = False

            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame_placeholder.image(frame_rgb, channels="RGB")

            if wild_detected:
                status_placeholder.error("⚠️ Wild Animal Detected!")
            else:
                status_placeholder.success("✅ No Wild Animals Detected.")
            
            time.sleep(0.03)
        
        cap.release()

st.markdown("## Alert Summary")
st.subheader("Alert Statistics:")

st.write(f"**Total Alerts Triggered:** {st.session_state.alert_count}")

if st.session_state.last_alert_time:
    st.write(f"**Last Alert Time:** {st.session_state.last_alert_time}")

else:
    st.write("**Last Alert Time:** N/A")

st.subheader("Alert Log:")

if st.session_state.alert_log:
    for log in st.session_state.alert_log[-5:]:
        st.write(
            f"- Time: {log['time']}, Animal: {log['animal']}, Confidence: {log['confidence']:.2f}"
        )                                                                                               
else:
    st.write("No alerts triggered yet.")