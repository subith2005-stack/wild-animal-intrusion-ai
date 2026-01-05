import streamlit as st
import cv2
import time
from datetime import datetime
from collections import deque, Counter
from alarm import play_alarm

from model.detector import detect_animals
from model.classifier import classify_animal
from alerts.sms_alerts import send_sms

# ================= CONFIG =================
DISPLAY_THRESHOLD = 0.5
SMS_THRESHOLD = 0.7

BUFFER_SIZE = 7
MIN_STABLE_COUNT = 4
ABSENCE_THRESHOLD = 10

ENABLE_SMS = True
FARMER_PHONE = "+918921828286"  # replace with verified number

# ================= STREAMLIT SETUP =================
st.set_page_config(page_title="Wild Animal Intrusion Detection")
st.title("Wild Animal Intrusion Detection System")



# ================= SESSION STATE =================
if "run" not in st.session_state:
    st.session_state.run = False

if "animal_present" not in st.session_state:
    st.session_state.animal_present = False

if "active_animal" not in st.session_state:
    st.session_state.active_animal = None

if "absence_counter" not in st.session_state:
    st.session_state.absence_counter = 0

if "prediction_buffer" not in st.session_state:
    st.session_state.prediction_buffer = deque(maxlen=BUFFER_SIZE)

if "alert_count" not in st.session_state:
    st.session_state.alert_count = 0

if "encounters" not in st.session_state:
    st.session_state.encounters = []

if "sms_sent_animals" not in st.session_state:
    st.session_state.sms_sent_animals = set()

# ================= UI CONTROLS =================
col1, col2 = st.columns(2)

with col1:
    if st.button("Start Camera"):
        st.session_state.run = True

with col2:
    if st.button("Stop Camera"):
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

        detections = detect_animals(frame)
        current_detections = []

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

            # ---- UI TABLE (≥ 0.5) ----
            if cls_conf >= DISPLAY_THRESHOLD:
                current_detections.append({
                    "Animal": animal,
                    "Confidence": round(cls_conf, 2)
                })

            # ---- BUFFER FOR CONFIRMATION (≥ 0.7) ----
            if cls_conf >= SMS_THRESHOLD:
                st.session_state.prediction_buffer.append(animal)

        # -------- STABLE CONFIRMATION --------
        confirmed_animal = None
        if len(st.session_state.prediction_buffer) == BUFFER_SIZE:
            counts = Counter(st.session_state.prediction_buffer)
            animal, count = counts.most_common(1)[0]
            if count >= MIN_STABLE_COUNT:
                confirmed_animal = animal

        # -------- TRIGGER & SMS LOGIC --------
        if confirmed_animal:

            # CASE 1: No trigger active
            if not st.session_state.animal_present:
                st.session_state.animal_present = True
                st.session_state.active_animal = confirmed_animal
                st.session_state.absence_counter = 0

                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                st.session_state.alert_count += 1
                st.session_state.encounters.append({
                    "Trigger": st.session_state.alert_count,
                    "Animal": confirmed_animal,
                    "Time": alert_time
                })

                if ENABLE_SMS and confirmed_animal not in st.session_state.sms_sent_animals:
                    send_sms(FARMER_PHONE, confirmed_animal, 1.0, alert_time)
                    play_alarm()
                    st.session_state.sms_sent_animals.add(confirmed_animal)

            # CASE 2: Different animal replaces current
            elif st.session_state.active_animal != confirmed_animal:
                st.session_state.prediction_buffer.clear()
                st.session_state.active_animal = confirmed_animal
                st.session_state.absence_counter = 0

                alert_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                st.session_state.alert_count += 1
                st.session_state.encounters.append({
                    "Trigger": st.session_state.alert_count,
                    "Animal": confirmed_animal,
                    "Time": alert_time
                })

                if ENABLE_SMS and confirmed_animal not in st.session_state.sms_sent_animals:
                    send_sms(FARMER_PHONE, confirmed_animal, 1.0, alert_time)
                    play_alarm()
                    st.session_state.sms_sent_animals.add(confirmed_animal)

        else:
            if st.session_state.animal_present:
                st.session_state.absence_counter += 1

                if st.session_state.absence_counter >= ABSENCE_THRESHOLD:
                    st.session_state.animal_present = False
                    st.session_state.active_animal = None
                    st.session_state.absence_counter = 0
                    st.session_state.prediction_buffer.clear()

        # -------- UI STATUS --------
        if st.session_state.animal_present:
            status_placeholder.error(
                f"Wild Animal Detected: {st.session_state.active_animal}"
            )
        else:
            status_placeholder.success("No Wild Animals Detected")

        frame_placeholder.image(frame, channels="BGR")

        # -------- LIVE DETECTION TABLE --------
        st.subheader("Detected Animals (Confidence ≥ 0.5)")
        if current_detections:
            st.table(current_detections)
        else:
            st.write("No animals detected above display threshold.")

        time.sleep(0.03)

    cap.release()

# ================= POST-RUN SUMMARY =================
st.markdown("---")
st.subheader("Encounter Summary")
st.write("Total Encounters:", st.session_state.alert_count)

if not st.session_state.run and st.session_state.encounters:
    st.subheader("Encounter Details")
    st.table(st.session_state.encounters)
else:
    st.write("Stop the camera to view encounter details.")

