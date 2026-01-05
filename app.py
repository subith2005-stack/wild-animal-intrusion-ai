import streamlit as st
import cv2
import time
from datetime import datetime

from model.detector import detect_ani
from model.classifier import classify_animal
from alerts.alert import trigger_alert
# from alerts.sms_alert import send_sms_alert

# ---------------- CONFIG ----------------
CONF_THRESHOLD = 0.7
ENABLE_SMS = False
FARMER_PHONE = "+91XXXXXXXXXX"

# ---------------- STREAMLIT SETUP ----------------
st.set_page_config(page_title="Wild Animal Intrusion Detection")
st.title("🌾 Wild Animal Intrusion Detection System")

# ---------------- SESSION STATE ----------------
if "run" not in st.session_state:
    st.session_state.run = False

if "animal_present" not in st.session_state:
    st.session_state.animal_present = False

if "alert_count" not in st.session_state:
    st.session_state.alert_count = 0

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

# ---------------- UI BUTTONS ----------------
col1, col2 = st.columns(2)
with col1:
    if st.button("▶ Start Camera"):
        st.session_state.run = True

with col2:
    if st.button("⏹ Stop Camera"):
        st.session_state.run = False

frame_placeholder = st.empty()
status_placeholder = st.empty()

# ---------------- LIVE CAMERA ----------------
if st.session_state.run:
    cap = cv2.VideoCapture(0)

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_ani(frame)
        wild_detected = False

        for det in detections:
            x1, y1, x2, y2 = det["box"]
            conf = det["confidence"]
            cls_id = det["cls_id"]

    # ---------------- HUMAN DETECTION ----------------
            if cls_id == 0 and conf > 0.6:  # person
                label = "Human"

                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                            frame, "Human",
                            (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0, 255, 0),
                            2
                            )

                continue  # 🔥 DO NOT send humans to classifier

    # ---------------- ANIMAL CLASSIFICATION ----------------
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            animal, cls_conf = classify_animal(crop)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                        frame,
                        f"{animal} {cls_conf:.2f}",
                        (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 0, 255),
                        2
                    )
            
            if conf > CONF_THRESHOLD:
                wild_detected = True

                if not st.session_state.animal_present:
                    trigger_alert(animal, conf)
                    st.session_state.animal_present = True

                    alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.session_state.alert_count += 1
                    st.session_state.alert_log.append(
                        f"{st.session_state.alert_count}. {animal} at {alert_time}"
                    )

                    # if ENABLE_SMS:
                    #     send_sms_alert(FARMER_PHONE, animal, conf, alert_time)

        if not wild_detected:
            st.session_state.animal_present = False
            status_placeholder.success("✅ No wild animals detected")

        frame_placeholder.image(frame, channels="BGR")
        time.sleep(0.03)

    cap.release()

# ---------------- DASHBOARD ----------------
st.markdown("---")
st.subheader("📊 Alert Statistics")
st.write("Total Alerts:", st.session_state.alert_count)

st.subheader("📜 Alert History")
for log in st.session_state.alert_log[-5:]:
    st.write(log)
