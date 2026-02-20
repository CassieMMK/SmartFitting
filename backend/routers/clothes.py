from fastapi import APIRouter, UploadFile, File
import os
import shutil
from services.clothes_analysis_service import analyze_clothes

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/analyze_clothes")
async def analyze_clothes_api(cloth_image: UploadFile = File(...)):
    path = os.path.join(UPLOAD_DIR, cloth_image.filename)

    with open(path, "wb") as f:
        shutil.copyfileobj(cloth_image.file, f)

    result = analyze_clothes(path)
    return result