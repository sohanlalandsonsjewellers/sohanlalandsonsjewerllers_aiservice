from fastapi import FastAPI
from app.database import db
import uvicorn
from fastapi.responses import Response
from config import APP_PORT

app = FastAPI(
    title="Jewellery AI Service"
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

if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=APP_PORT,
        reload=True
    )