Wild Animal Intrusion Detection System
Overview

The Wild Animal Intrusion Detection System is a real-time computer vision–based application designed to detect and classify wild animals entering agricultural areas. The system distinguishes humans from animals, confirms animal identity using temporal analysis, logs intrusion events (triggers), and sends SMS alerts only when a new animal type is detected.

The project is designed to be technically simple, efficient, scalable, and robust, making it suitable for real-world agricultural safety use cases and hackathon demonstrations.

Problem Statement

Farmers and agricultural workers face significant risks from wild animal intrusions, which can lead to crop damage and human–wildlife conflict. Existing solutions often generate false alerts due to unstable predictions and lack proper notification control.

This system addresses these issues by:

Using real-time object detection and classification

Confirming animal identity over multiple frames

Defining a clear and consistent concept of an intrusion event (trigger)

Reducing alert fatigue through controlled SMS notifications

Key Features

Real-time video feed processing using a webcam

Human detection handled separately to avoid false animal alerts

Machine learning–based animal classification

Temporal smoothing using majority voting across frames

Clear definition of a trigger as a continuous presence event

Accurate trigger counting and history display

SMS alerts sent only when a different animal type is detected

Streamlit-based web interface for monitoring and statistics

Git-based version control for collaborative development

Definition of a Trigger

A trigger is defined as:

The continuous presence of a confirmed wild animal from the moment it appears on the screen until it fully disappears.

Key points:

One trigger corresponds to one appearance–disappearance cycle

Multiple frames of the same animal count as a single trigger

Trigger count and logs are updated once per trigger

System Architecture
Detection Layer

YOLO-based object detection identifies objects in each frame

Humans are filtered out using the YOLO person class

Classification Layer

Cropped animal regions are passed to a trained classification model

Only predictions above a confidence threshold are considered

Temporal Confirmation Layer

Predictions are collected over a fixed number of frames

Majority voting is applied to confirm the animal identity

Early misclassifications are ignored

Trigger and Alert Layer

A trigger starts when a confirmed animal appears

A trigger ends only after the animal is absent for a defined number of frames

SMS alerts are sent only if the animal type differs from the last alerted animal

Technology Stack

Python 3

OpenCV

Streamlit

YOLO (Ultralytics)

Custom-trained animal classification model

Twilio (for SMS alerts)

Git and GitHub for version control

Project Structure
wild-animal-intrusion-ai/
│
├── app.py                 # Main Streamlit application
├── model/
│   ├── detector.py        # YOLO-based object detection
│   └── classifier.py      # Animal classification model
│
├── alerts/
│   └── sms_alert.py       # SMS alert handling (Twilio)
│
├── requirements.txt       # Python dependencies
├── .gitignore             # Ignored files and folders
└── README.md              # Project documentation

Installation and Setup
1. Clone the Repository
git clone <repository-url>
cd wild-animal-intrusion-ai

2. Create and Activate Virtual Environment
python -m venv .venv


On Windows:

.venv\Scripts\activate


On Linux/macOS:

source .venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

Environment Configuration (SMS Alerts)

Set the following environment variables for Twilio:

TWILIO_ACCOUNT_SID
TWILIO_AUTH_TOKEN
TWILIO_PHONE_NUMBER


Ensure:

The Twilio phone number is valid

The recipient phone number is verified if using a trial account

Restart the terminal after setting environment variables.

Running the Application
streamlit run app.py


Steps:

Click Start Camera in the web interface

Show an animal in front of the camera

Observe detection, confirmation, and trigger logging

SMS is sent only if a new animal type is detected

User Interface Outputs

Live video feed with bounding boxes

Human and animal labels

Current intrusion status

Total number of triggers

Trigger history with timestamps and animal names

Alert Logic Summary

Trigger count increments once per intrusion

Trigger history logs all intrusions

SMS alerts are rate-limited:

Sent only when the detected animal type differs from the previous SMS alert

Prevents repeated notifications for the same animal

Design Rationale

Temporal smoothing reduces false positives

State-based trigger management ensures reliable alerts

Separation of detection, confirmation, and notification logic improves maintainability

The system is robust against flickering detections and confidence noise

Version Control Workflow

Feature-based branching was used during development

Stable checkpoints were committed regularly

Training datasets and virtual environments are excluded from version control

Future Enhancements

Multi-camera support

Cloud-based deployment

Integration with local alert systems (sirens, lights)

Extended animal dataset

Dashboard analytics and exportable reports

Conclusion

This system demonstrates a practical and scalable approach to real-time wildlife intrusion detection for agriculture. By combining computer vision, temporal reasoning, and controlled alerting, it provides reliable monitoring while minimizing false alarms and alert fatigue.