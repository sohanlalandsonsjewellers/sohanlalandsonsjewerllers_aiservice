from fastapi import APIRouter

from app.services.segmentation_service import SegmentationService

router = APIRouter()


@router.get("/customer-segmentation")

async def customer_segmentation():

    data = await SegmentationService.segment_customers()

    return {

        "success": True,

        "count": len(data),

        "data": data

    }