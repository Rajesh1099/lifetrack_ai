from fastapi import Depends, HTTPException, status  # Imports dependency injection and HTTP error handling.
from fastapi.security import OAuth2PasswordBearer  # Imports the Bearer token extractor.
from sqlalchemy.orm import Session  # Imports the database session type.
from app.database.session import get_db  # Imports the database session dependency.
from app.core.tokens import verify_access_token  # Imports our access token validator.
from app.models.user import User  # Imports the User database model.

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login") # Extracts the Bearer token from requests.

def get_current_user(token: str=Depends(oauth2_scheme), db:Session= Depends(get_db)):
    
    try: # Starts validating the access token.
        user_id= verify_access_token(token) # Validates the token and extracts the user ID.
    
    except ValueError:  # Handles invalid or expired access tokens.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")  # Returns HTTP 401.
    
    user=db.query(User).filter(User.id==user_id).first() # Finds the user with this ID in PostgreSQL.
    
    if user is None:  # Checks whether the user exists.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")  # Rejects unknown users.
    
    if not user.is_active:  # Checks whether the user's account is active.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")  # Rejects inactive accounts.

    return user  # Returns the authenticated user to the endpoint.
    
    
    
