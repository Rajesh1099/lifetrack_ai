# auth_service.py will handle registration, login, and authentication logic.
'''
The flow is:
1. API layer: FastAPI calls get_db() and obtains a database session.
2. Service layer: auth_service.py receives that already-created session through db: Session.
3. Business logic: The service uses that session to query, insert, update or delete records in PostgreSQL.
4. After the request: FastAPI runs the cleanup in get_db() and closes the session.
'''

import hashlib  # Hashes JWT IDs before storing them.
from app.core.tokens import decode_access_token  # Validates access tokens and extracts JWT claims.
from app.models.revoked_access_token import RevokedAccessToken  # Imports revoked access-token model.
from html import escape  # Safely escape user-provided text before inserting it into HTML
from datetime import datetime, timedelta, timezone  # Imports date/time tools for calculating token expiry.
from sqlalchemy.orm import Session  # Imports the database session type.
from app.models.user import User  # Imports the User database model.
from app.schemas.user import UserCreate  # Imports the registration request schema.
from app.core.security import hash_password,verify_password  # Imports the password hashing n verify function.
from app.models.refresh_token import RefreshToken  # Imports the refresh token database model.
from app.core.tokens import create_access_token,create_refresh_token, hash_refresh_token  # Imports token generation and hashing functions.
from app.services.email_service import send_email
from app.core.email_tokens import generate_email_token,verify_email_token
from app.core.config import settings
from textwrap import dedent  # Remove common indentation from multiline HTML


def get_user_by_email(db: Session, email: str) -> User | None:  # Receives the database session and email.
    return db.query(User).filter(User.email == email).first()  # Finds and returns the matching user.


def register_user(db: Session, user_data: UserCreate) -> User:  # Handle user registration
    existing_user = get_user_by_email(db, user_data.email)  # Check whether the email already exists

    if existing_user:  # Check whether a matching user was found
        raise ValueError("Email already registered")  # Reject duplicate registration

    new_user = User(  # Create a new user database object
        email=user_data.email,  # Store the user's email
        first_name=user_data.first_name,  # Store the first name
        last_name=user_data.last_name,  # Store the last name
        password_hash=hash_password(user_data.password),  # Hash the password before storing it
    )

    db.add(new_user)  # Add the user to the database session
    db.commit()  # Save the user in PostgreSQL
    db.refresh(new_user)  # Retrieve database-generated values

    email_token = generate_email_token(new_user.email)  # Generate a verification token

    verification_link = (  # Construct the verification URL
        f"{settings.BACKEND_BASE_URL}"  # Add the backend base URL
        f"{settings.API_V1_PREFIX}/auth/verify-email?token={email_token}"  # Add endpoint and token
    )

    safe_first_name = escape(new_user.first_name)  # Escape HTML-sensitive characters in the first name

    subject = "Verify your LifeTrack AI account"  # Set the email subject

    body = (  # Create the plain-text email fallback
        f"Hello {new_user.first_name},\n\n"  # Greet the user
        "Welcome to LifeTrack AI!\n"  # Welcome the user
        "Please verify your email using this link:\n\n"  # Explain the required action
        f"{verification_link}\n\n"  # Include the verification link
        "This link expires in 5 minutes.\n"  # Explain the expiry time
        "If you did not create this account, ignore this email."  # Add a security notice
    )

    html_body = dedent(f""" 
    <!DOCTYPE html> <!-- Declare an HTML document -->
    <html> <!-- Start the email HTML -->
    <body style="margin:0; padding:0; background-color:#f1f5f9; font-family:Arial,sans-serif;"> <!-- Set the email background and font -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f1f5f9; padding:30px 10px;"> <!-- Create the outer email layout -->
            <tr> <!-- Start the outer row -->
                <td align="center"> <!-- Center the email card -->
                    <table width="100%" cellpadding="0" cellspacing="0" style="max-width:560px; background-color:#ffffff; border-radius:12px; overflow:hidden;"> <!-- Create the main email card -->
                        <tr> <!-- Start the header row -->
                            <td align="center" style="background-color:#142d4e; padding:30px 20px;"> <!-- Create the branded header -->
                                <h1 style="color:#ffffff; margin:0; font-size:28px;">LifeTrack AI</h1> <!-- Display the application name -->
                                <p style="color:#c7d8ed; margin:8px 0 0; font-size:12px; letter-spacing:2px;">YOUR PERSONAL LIFE ASSISTANT</p> <!-- Display the tagline -->
                            </td> <!-- End the header cell -->
                        </tr> <!-- End the header row -->
                        <tr> <!-- Start the content row -->
                            <td style="padding:35px 30px; color:#334155;"> <!-- Add content spacing -->
                                <h2 style="color:#172b4d; text-align:center; font-size:24px;">Verify your email</h2> <!-- Display the email heading -->
                                <p style="font-size:15px;">Hello {safe_first_name},</p> <!-- Greet the user -->
                                <p style="font-size:15px; line-height:1.7;">Welcome to LifeTrack AI! Please verify your email address to activate your account.</p> <!-- Explain why verification is needed -->
                                <table align="center" cellpadding="0" cellspacing="0" style="margin:30px auto;"> <!-- Center the button -->
                                    <tr> <!-- Start the button row -->
                                        <td align="center" style="background-color:#2563eb; border-radius:8px;"> <!-- Style the button background -->
                                            <a href="{escape(verification_link, quote=True)}" style="display:inline-block; padding:15px 28px; color:#ffffff; text-decoration:none; font-weight:bold; font-size:15px;">Verify Email Address</a> <!-- Create the verification link button -->
                                        </td> <!-- End the button cell -->
                                    </tr> <!-- End the button row -->
                                </table> <!-- End the button table -->
                                <p style="font-size:13px; color:#64748b; text-align:center;">This verification link expires in <strong>5 minutes</strong>.</p> <!-- Display expiry information -->
                                <hr style="border:none; border-top:1px solid #e2e8f0; margin:30px 0;"> <!-- Add a separator -->
                                <p style="font-size:12px; color:#64748b; line-height:1.6;">If you did not create this account, you can safely ignore this email.</p> <!-- Add a security notice -->
                            </td> <!-- End the content cell -->
                        </tr> <!-- End the content row -->
                        <tr> <!-- Start the footer row -->
                            <td align="center" style="background-color:#f8fafc; padding:20px;"> <!-- Style the footer -->
                                <p style="font-size:11px; color:#94a3b8; margin:0;">© LifeTrack AI. All rights reserved.</p> <!-- Display the footer text -->
                            </td> <!-- End the footer cell -->
                        </tr> <!-- End the footer row -->
                    </table> <!-- End the main email card -->
                </td> <!-- End the centered cell -->
            </tr> <!-- End the outer row -->
        </table> <!-- End the outer email layout -->
    </body> <!-- End the email body -->
    </html> <!-- End the HTML document -->
    """)

    send_email(new_user.email, subject, body, html_body)  # Send both plain-text and HTML email versions

    return new_user  # Return the newly registered user

def verify_user_email(db: Session, token: str) -> str:  # Verify the email using the token
    email=verify_email_token(token) # Decode the token and extract the email
    
    user = get_user_by_email(db, email)  # Find the user using the email
    
    if not user:  # Check whether the user exists
        raise ValueError("User not found")  # Stop if the user does not exist

    if user.is_verified:  # Check whether the email is already verified
        return "Email is already verified"  # Avoid verifying it again

    user.is_verified = True  # Mark the user's email as verified
    db.commit()  # Save the verification status in the database
    db.refresh(user)  # Reload the updated user from the database

    return "Email verified successfully"  # Return the success message
    
    

def login_user(db:Session,email: str, password: str) -> dict:  # Receives the database session, email and password.)
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
    

def logout_user(db: Session, raw_token: str, access_token: str) -> dict:  # Accept database, refresh token, and access token

    try:  # Start a database transaction
        stored_token = validate_refresh_token(db, raw_token)  # Validate refresh token and retrieve its database record

        payload = decode_access_token(access_token)  # Validate access JWT and retrieve its claims

        if int(payload["sub"]) != stored_token.user_id:  # Ensure both tokens belong to the same user
            raise ValueError("Access and refresh tokens belong to different users")  # Reject mismatched tokens

        token_id = payload["jti"]  # Extract the unique JWT ID
        token_id_hash = hashlib.sha256(token_id.encode()).hexdigest()  # Hash JWT ID before database storage

        current_time = datetime.now(timezone.utc)  # Get current UTC time
        expires_at = datetime.fromtimestamp(payload["exp"], timezone.utc)  # Convert JWT expiry timestamp to datetime

        revoked_token = RevokedAccessToken(  # Create revoked access-token database record
            token_id_hash=token_id_hash,  # Store hashed JWT ID
            expires_at=expires_at,  # Store original access-token expiry
            revoked_at=current_time,  # Store revocation time
        )

        stored_token.revoked_at = current_time  # Revoke the refresh token
        db.add(revoked_token)  # Add revoked access-token record

        db.commit()  # Save both revocations in one transaction

        return {"message": "Successfully logged out"}  # Return logout success message

    except Exception:  # Handle failures during logout
        db.rollback()  # Undo all uncommitted database changes
        raise  # Pass the original error to the API layer



      
    
     
     



    
    