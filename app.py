import streamlit as st
from PIL import Image
import torch
from torchvision import transforms
from torchvision.models import vit_b_16
import gdown
import os

# Download model from Google Drive
MODEL_PATH = "best_vit_model.pth"
if not os.path.exists(MODEL_PATH):
    st.info("Downloading model...")
    gdown.download(id="1ydAG-VddNwqXuRT2yAnIdSutgcrgRMUP", output=MODEL_PATH, quiet=False)

# Load the model
@st.cache_resource
def load_model():
    model = vit_b_16(pretrained=False)
    model.heads.head = torch.nn.Linear(model.heads.head.in_features, 2)
    model.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))
    model.eval()
    return model

model = load_model()
class_names = ["Cat", "Dog"]

# Transform
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=(0.5,), std=(0.5,))
])

st.title("🐶🐱 Cat vs Dog Classifier (Vision Transformer)")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    img_t = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img_t)
        _, pred = torch.max(outputs, 1)
        predicted_class = class_names[pred.item()]
    
    st.success(f"Prediction: **{predicted_class}** 🐾")
