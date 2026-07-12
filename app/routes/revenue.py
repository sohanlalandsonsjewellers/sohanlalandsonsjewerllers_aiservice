from fastapi import APIRouter

from app.services.revenue_service import RevenueService

router = APIRouter()


@router.get("/daily")

async def daily_revenue():

    data = await RevenueService.get_daily_revenue()

    return {
        "success": True,
        "count": len(data),
        "data": data
    }

@router.get("/monthly")
async def monthly_revenue():

    data = await RevenueService.get_monthly_revenue()

    return {
        "success": True,
        "count": len(data),
        "data": data
    }