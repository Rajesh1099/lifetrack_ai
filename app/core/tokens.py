from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError  # Imports JWT encoding, decoding, and error handling.
from app.core.config import settings
import secrets  # Generates cryptographically secure random values.
import hashlib  # Imports the SHA-256 hashing utility.

SECRET_KEY = settings.SECRET_KEY  # Retrieves the secret key from the application settings for JWT encoding.
ALGORITHM = settings.ALGORITHM  # Specifies the algorithm used for JWT encoding.


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    payload={
        "sub":str(user_id),
        "exp":expire,
        "type":"access"
    }
    
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
    return token


def verify_access_token(token: str) -> int:  # Accepts a JWT access token and returns the user's ID.
    try:  # Starts checking the token for validity.
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # Decodes the token using our secret key.
        if payload.get("type") != "access":  # Checks whether this is actually an access token.
            raise ValueError("Invalid token type")  # Rejects email or other types of tokens.
        user_id = payload.get("sub")  # Extracts the user ID stored in the token.
        if user_id is None:  # Checks whether the token contains a user ID.
            raise ValueError("User ID not found")  # Rejects tokens without a user ID.
        return int(user_id)  # Converts the user ID to an integer and returns it.
    except (JWTError, ValueError) as exc:  # Catches invalid, expired, or incorrectly formatted tokens.
        raise ValueError("Invalid or expired access token") from exc  # Returns a clear error to the caller.

def create_refresh_token() -> str:
    refresh_token = secrets.token_urlsafe(64)  # Creates a cryptographically secure random string.
    return refresh_token  # Returns the generated refresh token.


def hash_refresh_token(token: str) -> str:  # Accepts the original refresh token.
    token_hash = hashlib.sha256(token.encode()).hexdigest()  # Converts the token into a SHA-256 hash.
    return token_hash  # Returns the hashed token for database storage.



        

            
            
            
