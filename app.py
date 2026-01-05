import streamlit as st
import cv2
import time
from datetime import datetime
from collections import deque, Counter

from model.detector import detect_ani
from model.classifier import classify_animal
from alerts.sms_alerts import send_sms

# ================= CONFIG =================
CONF_THRESHOLD = 0.7

BUFFER_SIZE = 7          # frames for majority voting
MIN_STABLE_COUNT = 4     # minimum occurrences in buffer
ABSENCE_THRESHOLD = 10   # frames animal must be absent to end trigger

ENABLE_SMS = True
FARMER_PHONE = "+918921828286"   # replace with verified number

# ================= STREAMLIT SETUP =================
st.set_page_config(page_title="Wild Animal Intrusion Detection")
st.title("🌾 Wild Animal Intrusion Detection System")

# ================= SESSION STATE =================
if "run" not in st.session_state:
    st.session_state.run = False

if "animal_present" not in st.session_state:
    st.session_state.animal_present = False

if "alert_count" not in st.session_state:
    st.session_state.alert_count = 0

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

# ---- Temporal smoothing ----
if "prediction_buffer" not in st.session_state:
    st.session_state.prediction_buffer = deque(maxlen=BUFFER_SIZE)

if "absence_counter" not in st.session_state:
    st.session_state.absence_counter = 0

# ---- Trigger & SMS control ----
if "last_confirmed_animal" not in st.session_state:
    st.session_state.last_confirmed_animal = None

if "sms_last_animal" not in st.session_state:
    st.session_state.sms_last_animal = None

# ================= UI CONTROLS =================
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Camera"):
        st.session_state.run = True

with col2:
    if st.button("⏹ Stop Camera"):
        st.session_state.run = False

frame_placeholder = st.empty()
status_placeholder = st.empty()

# ================= CAMERA LOOP =================
if st.session_state.run:
    cap = cv2.VideoCapture(0)

    while st.session_state.run:
        ret, frame = cap.read()
        if not ret:
            break

        detections = detect_ani(frame)
        wild_detected = False

        # -------- DETECTION & BUFFERING --------
        for det in detections:
            x1, y1, x2, y2 = det["box"]
            cls_id = det["cls_id"]
            det_conf = det["confidence"]

            # ---- HUMAN ----
            if cls_id == 0 and det_conf > 0.6:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(
                    frame, "Human",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                    (0, 255, 0), 2
                )
                continue

            # ---- ANIMAL ----
            crop = frame[y1:y2, x1:x2]
            if crop.size == 0:
                continue

            animal, cls_conf = classify_animal(crop)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(
                frame,
                f"{animal} {cls_conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                (0, 0, 255), 2
            )

            if cls_conf > CONF_THRESHOLD:
                wild_detected = True
                st.session_state.prediction_buffer.append(animal)

        # -------- STABLE ANIMAL CONFIRMATION --------
        confirmed_animal = None

        if len(st.session_state.prediction_buffer) == BUFFER_SIZE:
            counts = Counter(st.session_state.prediction_buffer)
            animal, count = counts.most_common(1)[0]

            if count >= MIN_STABLE_COUNT:
                confirmed_animal = animal

        # -------- TRIGGER & SMS LOGIC --------
        if confirmed_animal:
            st.session_state.absence_counter = 0

            if not st.session_state.animal_present:
                # ---- NEW TRIGGER START ----
                st.session_state.animal_present = True
                st.session_state.last_confirmed_animal = confirmed_animal

                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                # ---- UI TRIGGER LOG (ALWAYS) ----
                st.session_state.alert_count += 1
                st.session_state.alert_log.append(
                    f"Trigger {st.session_state.alert_count}: "
                    f"{confirmed_animal} at {alert_time}"
                )

                # ---- SMS ONLY IF ANIMAL TYPE CHANGES ----
                if ENABLE_SMS and st.session_state.sms_last_animal != confirmed_animal:
                    send_sms(
                        FARMER_PHONE,
                        confirmed_animal,
                        1.0,
                        alert_time
                    )
                    st.session_state.sms_last_animal = confirmed_animal

        else:
            # ---- NO CONFIRMED ANIMAL ----
            if st.session_state.animal_present:
                st.session_state.absence_counter += 1

                if st.session_state.absence_counter >= ABSENCE_THRESHOLD:
                    # ---- TRIGGER ENDS ----
                    st.session_state.animal_present = False
                    st.session_state.absence_counter = 0
                    st.session_state.prediction_buffer.clear()
                    st.session_state.last_confirmed_animal = None

        # -------- UI STATUS --------
        if st.session_state.animal_present:
            status_placeholder.error(
                f"🚨 Wild Animal Detected: {st.session_state.last_confirmed_animal}"
            )
        else:
            status_placeholder.success("✅ No Wild Animals Detected")

        frame_placeholder.image(frame, channels="BGR")
        time.sleep(0.03)

    cap.release()

# ================= DASHBOARD =================
st.markdown("---")
st.subheader("📊 Trigger Statistics")
st.write("Total Triggers:", st.session_state.alert_count)

st.subheader("📜 Trigger History")
for log in st.session_state.alert_log[-10:]:
    st.write(log)
