# Wild Animal Intrusion Detection System for Crop Protection

## 1. Project Title & Overview

**Project Name:** Wild Animal Intrusion Detection System  
**Domain:** Agriculture & Wildlife Management  
**Hackathon:** AARAMBH 3.0 - 24-Hour Innovation Challenge

This project is a real-time camera-based system designed to detect the intrusion of wild animals into agricultural fields using computer vision and machine learning. The system monitors a fixed video feed, identifies specific wild animals (elephants, deer, wild boars, tigers), and triggers immediate alerts via SMS to farmers for protective action. The solution is built to be lightweight, CPU-friendly, and capable of running on standard laptops or edge devices.

## 2. Problem Statement

The intrusion of wild animals into agricultural fields has become a critical issue affecting farming communities worldwide. Crop damage due to elephants, wild boars, deer, and other wildlife results in significant economic losses for farmers, leading to reduced income and food security concerns. Traditional methods of animal deterrence are often ineffective or environmentally harmful.

This system addresses the challenge of real-time detection and early warning of wild animal presence in agricultural areas. By leveraging computer vision technology, the system provides an assistive early warning mechanism that enables farmers to take preventive actions before significant crop damage occurs.

The solution is strictly designed as an assistive early warning system without any tracking or enforcement capabilities, focusing solely on detection and notification.

## 3. System Architecture Overview

The system follows a comprehensive end-to-end architecture:

**Camera Input** → **YOLO Detection** → **Animal Classification** → **Confirmation Buffer** → **Alert Trigger** → **SMS Notification** → **Dashboard Display**

1. **Camera Input**: Real-time video feed from a standard camera
2. **YOLO Detection**: Initial detection of objects in the frame using YOLOv8
3. **Animal Classification**: Fine-grained classification of detected animals using a custom-trained ResNet model
4. **Confirmation Buffer**: Frame-based confirmation system to avoid false positives
5. **Alert Trigger**: Logic to determine when an actual intrusion occurs
6. **SMS Notification**: Automated SMS alerts sent to farmers via Twilio API
7. **Dashboard Display**: Real-time visualization of detections and system status

## 4. Technology Stack

### Programming Language

- **Python 3.x**: Primary programming language for computer vision and machine learning components

### Computer Vision Libraries

- **OpenCV**: Real-time video processing and image manipulation
- **YOLOv8 (Ultralytics)**: Real-time object detection for identifying animals in video frames

### Machine Learning Frameworks

- **PyTorch**: Deep learning framework for animal classification model
- **Torchvision**: Computer vision utilities and pre-trained models
- **ResNet-18**: Pre-trained model fine-tuned for wild animal classification

### Notification Services

- **Twilio API**: SMS notification service for sending alerts to farmers
- **Environment Variables**: Secure storage of API credentials

### Web Framework

- **Streamlit**: Interactive web-based dashboard for real-time monitoring and control

## 5. Folder Structure

```
wild-animal-intrusion-ai/
├── app.py                    # Main Streamlit application with UI and core logic
├── main.py                   # Alternative command-line application
├── model/                    # Machine learning model components
│   ├── detector.py           # YOLOv8 object detection implementation
│   ├── classifier.py         # ResNet-based animal classification model
│   ├── live_camera.py        # Live camera feed processing utility
│   └── video_detector.py     # Video file processing utility
├── ml/                       # Machine learning training components
│   └── train_classifier.py   # Training script for animal classification model
├── alerts/                   # Alert and notification system
│   ├── alert.py              # Basic alert trigger mechanism
│   └── sms_alerts.py         # Twilio-based SMS notification service
├── README.md                 # Project documentation
└── .gitignore                # Git ignore configuration
```

### File Descriptions

**Core Application Files:**

- [app.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/app.py): Main Streamlit application that orchestrates the entire system. Handles camera feed, detection logic, confirmation buffering, alert triggering, and dashboard display. Contains the primary business logic for preventing false positives through frame-based confirmation.
- [main.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/main.py): Alternative command-line application for running the detection system without the web interface.

**Model Directory Files:**

- [model/detector.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/model/detector.py): Implements YOLOv8 object detection to identify animals in video frames. Returns bounding boxes, confidence scores, and class IDs for detected objects.
- [model/classifier.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/model/classifier.py): Contains the ResNet-18 based classifier that performs fine-grained animal identification. Loads a pre-trained model to classify cropped animal images into specific species (boar, deer, elephant, tiger).
- [model/live_camera.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/model/live_camera.py): Utility for capturing and processing live camera feed (note: contains an import error that needs to be fixed).
- [model/video_detector.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/model/video_detector.py): Utility for processing video files frame-by-frame (note: contains an import error that needs to be fixed).

**ML Training Directory Files:**

- [ml/train_classifier.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/ml/train_classifier.py): Training script for the animal classification model. Uses a dataset of wild animal images to train a ResNet-18 model for species identification.

**Alerts Directory Files:**

- [alerts/alert.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/alerts/alert.py): Basic alert trigger mechanism that prints alert messages to console when wild animals are detected.
- [alerts/sms_alerts.py](file:///c:/Users/subit/Desktop/wild-animal-intrusion-ai/alerts/sms_alerts.py): Implements Twilio-based SMS notifications to send alerts to farmers when animal intrusions are confirmed.

## 6. Core Logic Explanation

### Animal Detection Logic

The system employs a two-stage detection process:

1. **Primary Detection**: YOLOv8 model detects objects in each frame and identifies potential animals
2. **Classification**: Cropped animal images are passed to a ResNet-based classifier for species identification

### Frame-Based Confirmation to Avoid False Positives

The system implements a sophisticated buffering mechanism:

- A prediction buffer stores animal classifications from recent frames
- Only animals with confidence ≥ 0.7 are added to the buffer
- When the buffer reaches full capacity (7 frames), the system analyzes the most common detection
- An animal is confirmed present only if it appears in at least 4 out of 7 frames (MIN_STABLE_COUNT)

### Definition of a "Trigger"

A trigger occurs when:

1. An animal with confidence ≥ 0.7 is detected
2. The animal appears consistently in the buffer (≥ 4 out of 7 frames)
3. The animal was not previously detected as present in the system
4. The system transitions from "no animal present" to "animal present" state

### Duplicate Alert Prevention

The system prevents alert spamming through:

- A set to track animals for which SMS has already been sent
- SMS notifications are only sent once per unique animal type during a session
- Absence counter ensures that when an animal leaves and returns, it's treated as a new encounter

### Animal Handling

The system handles different animals by:

- Classifying them into specific species (boar, deer, elephant, tiger)
- Maintating separate tracking for each animal type
- Replacing current animal tracking when a different species is detected

## 7. Alert & Notification Workflow

### When Alerts Are Sent

- When a wild animal is confirmed present through the buffering system
- Only for animals with classification confidence ≥ 0.7
- Once per animal type during a session (prevents spam)

### Conditions for SMS/Email

- Twilio credentials must be properly configured in environment variables
- Animal classification confidence must exceed 0.7 threshold
- The animal type must not have been previously notified in the current session

### Logic to Prevent Alert Spamming

- SMS sent tracking set prevents duplicate notifications for the same animal type
- Absence threshold (10 frames) ensures animal is truly gone before resetting tracking
- Buffer system prevents rapid-fire notifications from temporary detections

### Example Alert Message Format

```
🚨 ALERT!
Wild Animal Detected: elephant
Confidence: 1.00
Time: 2023-06-15 14:30:25
Please take immediate action.
```

## 8. Installation & Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Step-by-Step Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/subith2005-stack/wild-animal-intrusion-ai.git
   cd wild-animal-intrusion-ai
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install opencv-python ultralytics torch torchvision streamlit twilio
   ```

4. **Download the pre-trained animal classifier model:**

   - Place the `animal_classifier.pt` file in the `model/` directory
   - This model is trained to classify boar, deer, elephant, and tiger

5. **Set up Twilio credentials (optional):**
   ```bash
   export TWILIO_ACCOUNT_SID=your_account_sid
   export TWILIO_AUTH_TOKEN=your_auth_token
   export TWILIO_PHONE_NUMBER=your_twilio_number
   ```

## 9. Usage Instructions

### Starting the Detection System

1. **Run the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

2. **Using the web interface:**

   - Click "Start Camera" to begin detection
   - Monitor the live feed and detection results
   - View detected animals in the table (confidence ≥ 0.5)
   - Stop the camera using the "Stop Camera" button

3. **Alternative command-line usage:**
   ```bash
   python main.py
   ```

### Testing with Camera/Video Input

- The system uses the default camera (index 0) for real-time detection
- Ensure proper lighting and positioning of the camera
- Test with images of wild animals to verify detection accuracy

### Viewing Logs and Dashboard Output

- Real-time detection results are displayed in the web interface
- Encounter summary shows all confirmed animal detections
- Console output provides additional debug information

## 10. Limitations & Disclaimer

### System Limitations

- **Environmental Factors**: Performance may be affected by poor lighting, weather conditions, or camera quality
- **Hardware Constraints**: Requires sufficient processing power for real-time detection
- **Animal Variability**: May not detect all wild animal species outside the trained categories
- **False Positives**: Despite buffering mechanisms, some false detections may occur

### Disclaimer

This system is designed as an assistive early warning mechanism only. It does not guarantee:

- Complete prevention of crop damage
- 100% accuracy in animal detection
- Protection against all types of wildlife intrusion
- Replacement for other protective measures

Users should combine this system with other traditional and modern farming protection methods for comprehensive crop security.

## 11. Future Enhancements

### Technical Improvements

- **Night Vision Support**: Integration with infrared cameras for 24/7 monitoring
- **Edge Deployment**: Optimized models for deployment on edge devices like Raspberry Pi
- **Improved Classification**: Expanded animal species recognition capabilities
- **Performance Optimization**: Model quantization and pruning for faster inference

### Feature Enhancements

- **Multi-Location Monitoring**: Support for multiple camera feeds simultaneously
- **IoT Integration**: Connection with IoT sensors for environmental monitoring
- **Government Integration**: API connections with agricultural and wildlife departments
- **Advanced Analytics**: Historical data analysis for pattern recognition

### User Experience

- **Mobile Application**: Native mobile app for farmers to receive alerts
- **Dashboard Analytics**: Comprehensive reporting and analytics dashboard
- **Customizable Alerts**: Configurable alert thresholds and notification preferences
- **Offline Capability**: Local processing without internet connectivity


