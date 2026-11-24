from pwdlib import PasswordHash  # Imports the password hashing utility.
from datetime import datetime, timedelta, timezone
from jose import jwt
from app.core.config import settings  # Imports application settings, including the secret key for JWT encoding.

password_hash = PasswordHash.recommended()  # Creates a recommended Argon2 password hasher.

SECRET_KEY = settings.SECRET_KEY  # Retrieves the secret key from the application settings for JWT encoding.
ALGORITHM = settings.ALGORITHM  # Specifies the algorithm used for JWT encoding.


def hash_password(password: str) -> str:  # Accepts a password string and returns its hash.
    return password_hash.hash(password)  # Converts the original password into a secure hash.


def verify_password(  # Defines a function to verify a password.
    plain_password: str,  # Password entered by the user.
    hashed_password: str  # Previously stored password hash.
) -> bool:  # Returns True if the password matches, otherwise False.
    return password_hash.verify(  # Checks the entered password against the stored hash.
        plain_password,  # Password entered during login.
        hashed_password  # Hash retrieved from the database.
    )

def generate_email_token(email: str) -> str:
    expire=datetime.now(timezone.utc) + timedelta(minutes=5)  # Sets the token to expire in 5 minutes.
    payload = {"sub": email, "exp": expire}  # Creates a payload with the email and expiration time.
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)  # Encodes the payload into a JWT using the secret key.
    return token  # Returns the generated token.

def verify_email_token(token: str) -> str:
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])  # Decodes the JWT using the secret key and algorithm.
        email=payload.get("sub")  # Retrieves the email from the decoded payload.
        if email is None:  # Checks if the email is present in the payload.
            raise ValueError("Invalid token: email not found")  # Raises an error if the email is missing.  
        return email  # Returns the email if the token is valid.
    except jwt.ExpiredSignatureError:  # Catches the exception if the token has expired.
        raise ValueError("Token has expired")  # Raises an error indicating the token has expired.
    except jwt.JWTError:  # Catches any other JWT-related errors.
        raise ValueError("Invalid token")  # Raises an error indicating the token is invalid.   
    