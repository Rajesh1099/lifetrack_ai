
from datetime import datetime, timedelta, timezone  # Import date and time utilities
from jose import jwt  # Import JWT encoding and decoding functions
from jose.exceptions import ExpiredSignatureError, JWTError  # Import JWT error classes

from app.core.config import settings  # Import JWT configuration


def generate_email_token(email: str) -> str:  # Generate a verification token for an email
    expire = datetime.now(timezone.utc) + timedelta(minutes=5)  # Set token expiry to 5 minutes

    payload = {  # Create the information stored inside the token
        "sub": email,  # Store the user's email as the token subject
        "exp": expire,  # Set the token expiration time
        "type": "email_verification",  # Identify this as an email verification token
    }

    token = jwt.encode(payload, settings.EMAIL_SECRET_KEY, algorithm=settings.ALGORITHM)  # Sign the token
    return token  # Return the generated token


def verify_email_token(token: str) -> str:  # Verify a received email verification token
    try:  # Start token validation
        payload = jwt.decode(token, settings.EMAIL_SECRET_KEY, algorithms=[settings.ALGORITHM])  # Decode and validate the token

        email = payload.get("sub")  # Extract the email from the token
        token_type = payload.get("type")  # Extract the token type

        if email is None or token_type != "email_verification":  # Reject missing email or incorrect token type
            raise ValueError("Invalid email verification token")  # Report an invalid token

        return email  # Return the verified token's email address

    except ExpiredSignatureError:  # Handle an expired token
        raise ValueError("Email verification link has expired")  # Return an expiry error

    except JWTError:  # Handle other JWT validation errors
        raise ValueError("Invalid email verification token")  # Return an invalid-token error
