from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError  # Imports JWT encoding, decoding, and error handling.
from app.core.config import settings
import secrets  # Generates cryptographically secure random values.
import hashlib  # Imports the SHA-256 hashing utility.

SECRET_KEY = settings.SECRET_KEY  # Retrieves the secret key from the application settings for JWT encoding.
ALGORITHM = settings.ALGORITHM  # Specifies the algorithm used for JWT encoding.


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    token_id = secrets.token_urlsafe(32)  # Generate a unique ID for this access token
    
    payload={
        "sub":str(user_id),
        "exp":expire,
        "type":"access",
        "jti": token_id  # Store the unique JWT ID
    }
    
    token=jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
    
    return token


def decode_access_token(token: str) -> dict:  # Validate JWT and return all its claims
    try:  # Start JWT validation
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Verify signature and expiry

        if payload.get("type") != "access":  # Check token type
            raise ValueError("Invalid token type")  # Reject incorrect token type

        if not payload.get("sub"):  # Check user ID exists
            raise ValueError("User ID not found")  # Reject missing user ID

        if not payload.get("jti"):  # Check unique token ID exists
            raise ValueError("JWT ID not found")  # Reject missing JWT ID

        int(payload["sub"])  # Validate that user ID is an integer

        return payload  # Return all validated JWT claims

    except (JWTError, ValueError) as exc:  # Handle invalid or expired tokens
        raise ValueError("Invalid or expired access token") from exc  # Return clear error    

def create_refresh_token() -> str:
    refresh_token = secrets.token_urlsafe(64)  # Creates a cryptographically secure random string.
    return refresh_token  # Returns the generated refresh token.


def hash_refresh_token(token: str) -> str:  # Accepts the original refresh token.
    token_hash = hashlib.sha256(token.encode()).hexdigest()  # Converts the token into a SHA-256 hash.
    return token_hash  # Returns the hashed token for database storage.



        

            
            
            
