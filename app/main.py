from fastapi import FastAPI
from app.database import db
import uvicorn
from fastapi.responses import Response
from config import APP_PORT

from app.api.recommendation import router as recommendation_router
from app.api.segmentation import router as segmentation_router
from app.api.inventory import router as inventory_router
from app.api.demand import router as demand_router
from app.api.sales import router as sales_router
from app.api.business_summary import router as business_summary_router
from app.api.reorder import router as reorder_router
from app.api.product_performance import router as product_performance_router

app = FastAPI(
    title="Jeweller AI Service"
)


@app.get("/")
async def home():

    return {
        "message": "AI Service Running"
    }


@app.get("/health")
async def health():

    await db.command("ping")

    return {
        "status": "healthy",
        "database": "connected"
    }


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)



app.include_router(
    recommendation_router,
    prefix="/ai",
    tags=["AI Recommendation"]
)

app.include_router(
    segmentation_router,
    prefix="/ai",
    tags=["AI Customer Segmentation"]
)

app.include_router(
    inventory_router,
    prefix="/ai",
    tags=["AI Inventory Insights"]
)

app.include_router(
    demand_router,
    prefix="/ai",
    tags=["AI Demand Forecast"]
)

app.include_router(
    sales_router,
    prefix="/ai",
    tags=["Sales Forecast"]
)

app.include_router(
    business_summary_router,
    prefix="/ai",
    tags=["Business Intelligence"]
)

app.include_router(
    reorder_router,
    prefix="/ai",
    tags=["Smart Reorder Engine"]
)

app.include_router(
    product_performance_router,
    prefix="/ai",
    tags=["Product Performance AI"]
)




if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=APP_PORT,
        reload=True
    )