
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered personal information and management platform",
    version="1.0.0",
    debug=settings.DEBUG,
)

app.include_router(api_router, prefix=settings.API_V1_PREFIX)



@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} backend is running"}
