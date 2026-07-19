from fastapi import APIRouter, HTTPException, Query

from app.services.customer_analytics_service import (
    CustomerAnalyticsService,
)

router = APIRouter(
    prefix="/customer-analytics",
    tags=["Customer Analytics AI"],
)


@router.get("/")
async def customer_analytics(
    segment: str | None = Query(None),
    customer_type: str |None = Query(None),
    at_risk: bool = Query(False),
):

    return await CustomerAnalyticsService.get_customer_analytics(
        segment=segment,
        customer_type=customer_type,
        at_risk=at_risk,
    )


@router.get("/summary")
async def customer_summary():

    result = await CustomerAnalyticsService.get_customer_analytics()

    return {

        "success": True,

        "summary": result["summary"],

        "segments": result["segments"]

    }


@router.get("/top-customers")
async def top_customers(
    limit: int = Query(
        10,
        ge=1,
        le=100,
    )
):

    result = await CustomerAnalyticsService.get_customer_analytics()

    return {

        "success": True,

        "count": min(
            limit,
            len(result["data"])
        ),

        "data": result["data"][:limit],

    }


@router.get("/repeat-customers")
async def repeat_customers():

    return await CustomerAnalyticsService.get_customer_analytics(
        customer_type="repeat"
    )


@router.get("/new-customers")
async def new_customers():

    return await CustomerAnalyticsService.get_customer_analytics(
        customer_type="new"
    )


@router.get("/at-risk")
async def at_risk_customers():

    return await CustomerAnalyticsService.get_customer_analytics(
        at_risk=True
    )


@router.get("/segment/{segment}")
async def customers_by_segment(
    segment: str,
):

    return await CustomerAnalyticsService.get_customer_analytics(
        segment=segment
    )


@router.get("/segments")
async def segments():

    result = await CustomerAnalyticsService.get_customer_analytics()

    grouped = {

        "VIP": [],

        "Premium": [],

        "Regular": [],

        "New Customer": []

    }

    for customer in result["data"]:

        grouped.setdefault(

            customer["segment"],

            []

        ).append(customer)

    return {

        "success": True,

        "count": len(result["data"]),

        "data": grouped,

    }


@router.get("/customer/{customer_id}")
async def customer_details(
    customer_id: str,
):

    result = await CustomerAnalyticsService.get_customer_analytics()

    customer = next(

        (

            customer

            for customer in result["data"]

            if customer["customerId"] == customer_id

        ),

        None,

    )

    if customer is None:

        raise HTTPException(

            status_code=404,

            detail="Customer not found",

        )

    return {

        "success": True,

        "data": customer,

    }