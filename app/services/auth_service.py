# auth_service.py will handle registration, login, and authentication logic.
'''
The flow is:
1. API layer: FastAPI calls get_db() and obtains a database session.
2. Service layer: auth_service.py receives that already-created session through db: Session.
3. Business logic: The service uses that session to query, insert, update or delete records in PostgreSQL.
4. After the request: FastAPI runs the cleanup in get_db() and closes the session.
'''

from datetime import datetime, timedelta, timezone  # Imports date/time tools for calculating token expiry.
from sqlalchemy.orm import Session  # Imports the database session type.
from app.models.user import User  # Imports the User database model.
from app.schemas.user import UserCreate  # Imports the registration request schema.
from app.core.security import hash_password,verify_password  # Imports the password hashing n verify function.
from app.models.refresh_token import RefreshToken  # Imports the refresh token database model.
from app.core.tokens import create_access_token,create_refresh_token, hash_refresh_token  # Imports token generation and hashing functions.



def get_user_by_email(db: Session, email: str) -> User | None:  # Receives the database session and email.
    return db.query(User).filter(User.email == email).first()  # Finds and returns the matching user.

def register_user(db: Session, user_data: UserCreate) -> User:  # Handles the user registration business logic.
    existing_user = get_user_by_email(db, user_data.email)  # Checks whether this email is already registered.
    
    if existing_user:  # Checks whether a matching user was found.
        raise ValueError("Email already registered")  # Prevents duplicate registrations.
    
    new_user = User(  # Creates a new User database object.
        email=user_data.email,  # Stores the user's email address.
        first_name=user_data.first_name,  # Stores the user's first name.
        last_name=user_data.last_name,  # Stores the user's last name.
        password_hash=hash_password(user_data.password),  # Hashes the password before storing it.
    )

    db.add(new_user)  # Adds the new user to the database session.
    db.commit()  # Saves the new user permanently in PostgreSQL.
    db.refresh(new_user)  # Retrieves database-generated values such as the user ID.
    return new_user  # Returns the newly registered user.

def login_user(db:Session,email: str, password: str) -> User:  # Receives the database session, email and password.)
    user = get_user_by_email(db, email)  # Finds the user using their email address.
    
    if not user:  # Checks whether the email exists in the database.
        raise ValueError("Invalid email or password")  # Rejects an unknown email.

    if not verify_password(password,user.password_hash):  # Compares the entered password with the stored hash.
        raise ValueError("Invalid email or password")  # Rejects an incorrect password.
    
    if not user.is_verified:  # Checks whether the user has verified their email.
        raise ValueError("Please verify your email before logging in")  # Prevents unverified users from logging in.

    if not user.is_active:  # Checks whether the user account is active.
        raise ValueError("Your account is inactive")  # Prevents inactive users from logging in.
    
    access_token=create_access_token(user.id) # Generates a short-lived JWT access token.
    refresh_token = save_refresh_token(db, user.id)  # Generates and stores a hashed refresh token.
    
    return {  # Returns the authentication tokens.
        "access_token": access_token,  # Provides the access token to the client.
        "refresh_token": refresh_token,  # Provides the original refresh token to the client.
        "token_type": "bearer",  # Identifies the authentication scheme.
    }


def save_refresh_token(db: Session, user_id: int) -> str:  # Creates and stores a refresh token for a user.
    refresh_token=create_refresh_token() # Generates a secure random refresh token.
    token_hash=hash_refresh_token(refresh_token) # Hashes the original token before database storage.
    expires_at = datetime.now(timezone.utc) + timedelta(days=7)  # Sets the token expiry to seven days from now.

    db_token=RefreshToken( # Creates a database record for the refresh token.
        token_hash=token_hash,
        user_id=user_id,  # Associates the token with its user.
        expires_at=expires_at,  # Stores the expiry timestamp.
    )    
    
    db.add(db_token)
    db.add(db_token)  # Adds the token record to the database session.
    db.commit()  # Saves the refresh token record in PostgreSQL.
    db.refresh(db_token)  # Retrieves the saved database record.

    return refresh_token  # Returns the original token to the client, never the hash.

def validate_refresh_token(db:Session,raw_token:str) ->RefreshToken:
     # Convert the raw refresh token into its SHA256 hash
    token_hash=hash_refresh_token(raw_token)
     
     # Search the database for the matching hashed token
    stored_token=db.query(RefreshToken).filter(RefreshToken.token_hash==token_hash).first()
     
      # Reject the token if it does not exist in the database
    if stored_token is None:
        raise ValueError("Invalid refresh token")
     
      # Reject the token if it has already been revoked
    if stored_token.revoked_at is not None:
        raise ValueError("Refresh token has been revoked")
    
    # Get the current UTC time
    current_time = datetime.now(timezone.utc)
     
      # Reject the token if its expiry time has passed
    if stored_token.expires_at <= current_time:
        raise ValueError("Refresh token has expired")

    # Return the valid database token record
    return stored_token


def refresh_tokens(db: Session, raw_token: str) -> dict:
    old_token=validate_refresh_token(db,raw_token)
    
    # Generate a new access token for the same user
    access_token = create_access_token(old_token.user_id)
    
    # Generate a new random refresh token
    new_refresh_token = create_refresh_token()
    
    # Hash the new refresh token before storing it
    new_token_hash = hash_refresh_token(new_refresh_token)
    
     # Get the current UTC time
    current_time = datetime.now(timezone.utc)
    
    # Revoke the old refresh token so it cannot be reused
    old_token.revoked_at = current_time
    
    # Create a database record for the new refresh token
    replacement_token = RefreshToken(
        token_hash=new_token_hash,  # Store only the hashed token
        user_id=old_token.user_id,  # Keep the same user
        expires_at=current_time + timedelta(days=7),  # Set expiry to 7 days
    )
    
    # Add the new refresh token to the database session
    db.add(replacement_token)

    # Save revocation and replacement together in one transaction
    db.commit()

    # Refresh the record to get the latest database state
    db.refresh(replacement_token)

    # Return both newly generated tokens to the client
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
    }
    
     
     



    
    