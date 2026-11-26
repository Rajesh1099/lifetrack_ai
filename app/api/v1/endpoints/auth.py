#auth.py will handle HTTP requests and responses.

from fastapi import APIRouter,Depends,HTTPException,status  # Import API routing, dependency injection, errors, and HTTP status codes
from sqlalchemy.orm import Session # Import the database session type
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # Extract access token from Authorization header

from app.database.session import get_db # Import the function that provides a database session
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token  # Import schemas for registration and login  
from app.services.auth_service import (  # Import authentication service functions
    register_user,  # Register a new user
    login_user,  # Authenticate a user
    refresh_tokens,  # Generate new tokens
    logout_user,  # Revoke a refresh token
    verify_user_email,  # Verify a user's email address
)
from app.schemas.refresh_token import RefreshTokenRequest  # Import refresh-token request schema


router=APIRouter(prefix="/auth",tags=["Authentication"]) # Create a router for authentication endpoints

bearer_scheme = HTTPBearer()  # Extract Bearer access token from incoming requests

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED) # Define POST /auth/register and its response
def register(data:UserCreate,db: Session=Depends(get_db)):# Receive request data and inject a database session
    try:  # Start handling possible registration errors
        user=register_user(db,data) # Call the service layer to register the user
        return user # Return the newly registered user
    except ValueError as exc:  # Catch business validation errors from the service
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))  # Return HTTP 409 for conflicts

@router.get("/verify-email")  # Create an endpoint for email verification
def verify_email(token: str, db: Session = Depends(get_db)):  # Accept token and database session
    try:  # Handle verification errors
        message = verify_user_email(db, token)  # Call the service function
        return {"message": message}  # Return the verification result
    except ValueError as exc:  # Catch invalid or expired token errors
        raise HTTPException(  # Return an HTTP error response
            status_code=status.HTTP_400_BAD_REQUEST,  # Use HTTP 400 for invalid verification
            detail=str(exc),  # Send the actual error message
        )


@router.post("/login",response_model=Token)  # Define POST /auth/login and its token response format
def login(data: UserLogin, db: Session = Depends(get_db)):  # Receive login credentials and database session
    try:  # Handle authentication errors
        tokens=login_user(db,data.email,data.password) # Verify credentials and generate tokens
        return tokens  # Return access token and refresh token
    except ValueError as exc:  # Catch invalid credentials or account status errors
        raise HTTPException(  # Convert the service error into an HTTP error
            status_code=status.HTTP_401_UNAUTHORIZED,  # Return HTTP 401 Unauthorized
            detail=str(exc),  # Send the error message to the client
            headers={"WWW-Authenticate": "Bearer"},  # Indicate Bearer token authentication
        )


@router.post("/refresh",response_model=Token)  # Define POST /auth/refresh and its response format
def refresh(data: RefreshTokenRequest, db: Session = Depends(get_db)):  # Receive refresh token and database session
    try:
        tokens=refresh_tokens(db,data.refresh_token) # Validate old token and generate new tokens
        return tokens  # Return the new access and refresh tokens
    except ValueError as exc:  # Catch invalid, revoked, or expired token errors
        raise HTTPException(  # Convert the service error into an HTTP response
            status_code=status.HTTP_401_UNAUTHORIZED,  # Return HTTP 401 Unauthorized
            detail=str(exc),  # Return the reason for rejection
        )


@router.post("/logout")  # Define the logout endpoint
def logout(
    data: RefreshTokenRequest,  # Receive refresh token from JSON body
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),  # Extract access token from Authorization header
    db: Session = Depends(get_db),  # Inject database session
):
    try:  # Handle token validation errors
        result = logout_user(
            db,
            data.refresh_token,
            credentials.credentials,  # Pass raw access token to logout service
        )
        return result  # Return logout success message

    except ValueError as exc:  # Catch invalid or expired token errors
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,  # Return HTTP 401
            detail=str(exc),  # Return error reason
        ) from exc

    
        

