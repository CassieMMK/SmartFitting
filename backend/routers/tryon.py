from fastapi import APIRouter, UploadFile, File
import os
import shutil

from services.body_model_service import extract_body_features
from services.clothes_analysis_service import analyze_clothes
from services.tryon_client import request_tryon
from services.recommendation_service import generate_recommendation

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/smart_tryon")
async def smart_tryon(
    user_image: UploadFile = File(...),
    cloth_image: UploadFile = File(...)
):

    user_path = os.path.join(UPLOAD_DIR, user_image.filename)
    cloth_path = os.path.join(UPLOAD_DIR, cloth_image.filename)

    with open(user_path, "wb") as f:
        shutil.copyfileobj(user_image.file, f)

    with open(cloth_path, "wb") as f:
        shutil.copyfileobj(cloth_image.file, f)

    # 1️⃣ 人体分析
    body_result = extract_body_features(user_path)

    # 2️⃣ 服装分析
    clothes_result = analyze_clothes(cloth_path)

    # 3️⃣ 调用AI换装
    tryon_result = request_tryon(user_path, cloth_path)

    # 4️⃣ 推荐系统
    recommendation = generate_recommendation(
        body_result,
        clothes_result
    )

    return {
        "body_analysis": body_result,
        "clothes_analysis": clothes_result,
        "tryon_result": tryon_result,
        "recommendation": recommendation
    }