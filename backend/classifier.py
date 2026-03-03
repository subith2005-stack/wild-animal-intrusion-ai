import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import os

# -------- CONFIG --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "animal_classifier.pt")

# MUST MATCH TRAINING ORDER
CLASS_NAMES = ['Bear', 'Deer', 'Elephant', 'Tiger', 'Wild_Boar']

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

CONFIDENCE_THRESHOLD = 0.7  # Only accept predictions above this

# -------- LOAD MODEL --------
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))

model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()

# -------- IMAGE PREPROCESS --------
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],   # ImageNet normalization
        std=[0.229, 0.224, 0.225]
    )
])

def classify_animal(cropped_img):
    """
    cropped_img: OpenCV BGR image
    returns: (animal_name, confidence)
    """

    img = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB)
    img = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        outputs = model(img)
        probs = torch.softmax(outputs, dim=1)
        conf, pred = torch.max(probs, 1)

    confidence = conf.item()
    predicted_class = CLASS_NAMES[pred.item()]

    # 🔥 UNKNOWN REJECTION
    if confidence < CONFIDENCE_THRESHOLD:
        return "unknown", confidence

    return predicted_class, confidence

