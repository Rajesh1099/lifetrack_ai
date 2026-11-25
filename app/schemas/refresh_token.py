from pydantic_settings import BaseModel

class RefreshTokenRequest(BaseModel):
    refresh_token: str

    