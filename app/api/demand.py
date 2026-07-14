from fastapi import APIRouter

from app.services.demand_service import DemandService

router = APIRouter()


@router.get("/demand-forecast")
async def demand_forecast(days: int = 30):

    data = await DemandService.forecast(days)

    return {

        "success": True,

        "days": days,

        "count": len(data),

        "data": data

    }


@router.get("/demand-insights")
async def demand_insights(days: int = 30):

    data = await DemandService.demand_insights(days)

    return {

        "success": True,

        "days": days,

        "count": len(data),

        "data": data

    }