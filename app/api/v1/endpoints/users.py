from fastapi import APIRouter, Depends  # Import API routing and dependency injection
from app.api.dependencies import get_current_user  # Import current-user authentication
from app.models.user import User  # Import the User model
from app.schemas.user import UserResponse  # Import user response schema

router=APIRouter(prefix="/users",tags=["Users"])  # Create users router

@router.get("/me", response_model=UserResponse)  # Create protected current-user endpoint
def get_my_profile(current_user: User = Depends(get_current_user)):  # Require authentication
    return current_user  # Return the authenticated user's details