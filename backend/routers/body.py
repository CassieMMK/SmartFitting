from fastapi import APIRouter, UploadFile, File
import shutil
import os
from services.body_model_service import extract_body_features

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze_body")
async def analyze_body(user_image: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, user_image.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(user_image.file, f)

    features = extract_body_features(path)

    return features