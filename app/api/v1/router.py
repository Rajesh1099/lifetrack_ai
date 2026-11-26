from fastapi import APIRouter  # Import FastAPI router functionality

from app.api.v1.endpoints import health, auth,users  # Import health and authentication endpoints

api_router = APIRouter()  # Create the main API router

api_router.include_router(health.router)  # Register health endpoints
api_router.include_router(auth.router)  # Register authentication endpoints
api_router.include_router(users.router)  # Register user endpoints