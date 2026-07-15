from fastapi import APIRouter

from app.services.business_summary_service import BusinessSummaryService

router = APIRouter()


@router.get("/business-summary")
async def business_summary():

    data = await BusinessSummaryService.summary()

    return {

        "success": True,

        "generatedAt": data["generatedAt"],

        "businessScore": data["businessScore"],

        "orders": data["orders"],

        "products": data["products"],
        
        "customers": data["customers"],   # ✅ Add this

        "sales": data["sales"],

        "inventoryHealth": data["inventoryHealth"],

        "alerts": data["alerts"],

        "recommendations": data["recommendations"]

    }