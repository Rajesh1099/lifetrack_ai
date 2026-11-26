
from fastapi import Depends, HTTPException, status  # Imports dependency injection and HTTP error handling.
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials  # Imports Bearer authentication classes.
from sqlalchemy.orm import Session  # Imports the database session type.
from app.database.session import get_db  # Imports the database session dependency.
from app.core.tokens import decode_access_token  # Imports our access token validator.
from app.models.user import User  # Imports the User database model.
import hashlib  # Hashes the JWT ID before checking the database.
from app.models.revoked_access_token import RevokedAccessToken  # Imports the revoked access-token model.

bearer_scheme = HTTPBearer()  # Extracts Bearer credentials from requests.


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):  # Gets credentials and database session.

    token = credentials.credentials  # Extracts the actual JWT string.

    try:  # Starts validating the access token.
        payload = decode_access_token(token)  # Validates JWT and retrieves all claims.
        user_id = int(payload["sub"])  # Extracts the user ID from JWT claims.
        token_id = payload["jti"]  # Extracts the unique JWT ID.

    except (ValueError, KeyError) as exc:  # Handles invalid tokens or missing claims.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from exc  # Returns HTTP 401.

    token_id_hash = hashlib.sha256(token_id.encode()).hexdigest()  # Hashes the JWT ID to match the database value.

    revoked_token = db.query(RevokedAccessToken).filter(RevokedAccessToken.token_id_hash == token_id_hash).first()  # Checks whether this access token was revoked.

    if revoked_token is not None:  # Checks whether a matching revocation record exists.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access token has been revoked")  # Rejects the revoked token.

    user = db.query(User).filter(User.id == user_id).first()  # Finds the user in PostgreSQL.

    if user is None:  # Checks whether the user exists.
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")  # Rejects unknown users.

    if not user.is_active:  # Checks whether the account is active.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user")  # Rejects inactive accounts.

    if not user.is_verified:  # Checks whether the email is verified.
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Email not verified")  # Rejects unverified users.

    return user  # Returns the authenticated user.