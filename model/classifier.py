import torch
import torch.nn as nn
from torchvision import models, transforms
import cv2
import numpy as np

# -------- CONFIG --------
MODEL_PATH = "model/animal_classifier.pt"
CLASS_NAMES = ["boar", "deer", "elephant", "tiger"]
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -------- LOAD MODEL --------
model = models.resnet18(weights=None)
model.fc = nn.Linear(model.fc.in_features, len(CLASS_NAMES))

model.load_state_dict(torch.load(MODEL_PATH, map_location=DEVICE))
model = model.to(DEVICE)
model.eval()   # 🔥 VERY IMPORTANT

# -------- IMAGE PREPROCESS --------
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor()
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

    return CLASS_NAMES[pred.item()], conf.item()

