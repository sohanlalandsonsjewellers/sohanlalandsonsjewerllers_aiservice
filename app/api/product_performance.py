from fastapi import APIRouter, Query

from app.services.product_performance_service import (
    ProductPerformanceService
)

router = APIRouter(
    prefix="/product-performance",
    tags=["Product Performance AI"]
)


@router.get("/")
async def get_product_performance(
    category: str | None = Query(None),
    grade: str | None = Query(None),
    moving: str | None = Query(None),
    trend: str | None = Query(None)
):

    return await ProductPerformanceService.get_product_performance(
        category=category,
        grade=grade,
        moving=moving,
        trend=trend
    )


@router.get("/summary")
async def product_summary():

    data = await ProductPerformanceService.get_product_performance()

    return {

        "success": True,

        "summary": data["summary"],

        "totalProducts": data["count"]

    }


@router.get("/top")
async def top_products(
    limit: int = Query(10, ge=1, le=100)
):

    data = await ProductPerformanceService.get_product_performance()

    return {

        "success": True,

        "count": min(limit, len(data["data"])),

        "data": data["data"][:limit]

    }


@router.get("/dead-stock")
async def dead_stock():

    return await ProductPerformanceService.get_product_performance(
        moving="Dead"
    )


@router.get("/fast-moving")
async def fast_moving():

    return await ProductPerformanceService.get_product_performance(
        moving="Fast"
    )


@router.get("/slow-moving")
async def slow_moving():

    return await ProductPerformanceService.get_product_performance(
        moving="Slow"
    )


@router.get("/grade/{grade}")
async def by_grade(
    grade: str
):

    return await ProductPerformanceService.get_product_performance(
        grade=grade.upper()
    )


@router.get("/trend/{trend}")
async def by_trend(
    trend: str
):

    return await ProductPerformanceService.get_product_performance(
        trend=trend.title()
    )