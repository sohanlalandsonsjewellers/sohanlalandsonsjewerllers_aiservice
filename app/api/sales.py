from fastapi import APIRouter

from app.services.sales_service import SalesService

router = APIRouter()


@router.get("/sales-forecast")
async def sales_forecast(days: int = 30):

    data = await SalesService.forecast(days)

    return {

        "success": True,

        "days": days,

        "historyLength": data["historyLength"],

        "forecastModel": data["forecastModel"],

        "forecast": data["forecast"]

    }


@router.get("/sales-history")
async def sales_history(days: int = 30):

    data = await SalesService.forecast(days)

    return {

        "success": True,

        "historyLength": data["historyLength"],

        "history": data["history"]

    }


@router.get("/sales-summary")
async def sales_summary(days: int = 30):

    data = await SalesService.forecast(days)

    total_forecast = round(

        sum(

            item["predictedRevenue"]

            for item in data["forecast"]

        ),

        2

    )

    average_daily = round(

        total_forecast / days,

        2

    ) if days else 0

    return {

        "success": True,

        "forecastModel": data["forecastModel"],

        "forecastDays": days,

        "predictedTotalRevenue": total_forecast,

        "predictedAverageDailyRevenue": average_daily

    }