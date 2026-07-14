from fastapi import APIRouter

from app.services.inventory_service import InventoryService

router = APIRouter()


@router.get("/inventory-insights")

async def inventory_insights():

    data = await InventoryService.get_inventory_insights()

    return {

        "success": True,

        "count": len(data),

        "data": data

    }