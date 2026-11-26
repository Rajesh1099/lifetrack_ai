from pydantic import BaseModel  # Import Pydantic's schema base class

class RefreshTokenRequest(BaseModel):
    refresh_token: str

    