from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="The user's email address.")
    password: str = Field(..., min_length=8, description="The user's password.")
    first_name: str = Field(..., description="The user's first name.")
    last_name: str = Field(..., description="The user's last name.")


class UserResponse(BaseModel):
    id:int
    email: EmailStr
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


