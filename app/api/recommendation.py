from fastapi import APIRouter

from app.services.recommendation_service import RecommendationService
from app.ml.recommendation_model import RecommendationModel

router = APIRouter()


@router.get("/recommend/{product_id}")

async def recommend_products(product_id: str):

    products = await RecommendationService.get_products()

    model = RecommendationModel()

    recommendations = model.recommend(

        products,

        product_id

    )

    return {

        "success": True,

        "count": len(recommendations),

        "data": recommendations

    }