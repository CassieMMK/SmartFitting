from fastapi import APIRouter
from services.recommendation_service import generate_recommendation

router = APIRouter()

@router.post("/recommend")
async def recommend_api(body_data: dict, clothes_data: dict):

    result = generate_recommendation(body_data, clothes_data)

    return result