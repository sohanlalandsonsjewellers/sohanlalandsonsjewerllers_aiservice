from fastapi import APIRouter

from app.services.reorder_service import ReorderService

router = APIRouter()


@router.get("/reorder-plan")
async def reorder_plan(

    days: int = 30

):

    data = await ReorderService.reorder_plan(days)

    return {

        "success": True,

        "generatedAt": __import__("datetime").datetime.utcnow().isoformat(),

        "days": data["days"],

        "count": data["count"],

        "summary": data["summary"],

        "data": data["data"]

    }


@router.get("/reorder-summary")
async def reorder_summary(

    days: int = 30

):

    data = await ReorderService.reorder_plan(days)

    return {

        "success": True,

        "generatedAt": __import__("datetime").datetime.utcnow().isoformat(),

        "days": data["days"],

        "summary": data["summary"]

    }


@router.get("/critical-reorders")
async def critical_reorders(

    days: int = 30

):

    data = await ReorderService.reorder_plan(days)

    critical = [

        item

        for item in data["data"]

        if item["priority"] == "Critical"

    ]

    return {

        "success": True,

        "generatedAt": __import__("datetime").datetime.utcnow().isoformat(),

        "count": len(critical),

        "data": critical

    }


@router.get("/high-reorders")
async def high_reorders(

    days: int = 30

):

    data = await ReorderService.reorder_plan(days)

    high = [

        item

        for item in data["data"]

        if item["priority"] in [

            "Critical",

            "High"

        ]

    ]

    return {

        "success": True,

        "generatedAt": __import__("datetime").datetime.utcnow().isoformat(),

        "count": len(high),

        "data": high

    }