
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator  # Import Pydantic validation tools
from datetime import datetime  # Import datetime for created_at


class UserCreate(BaseModel):  # Schema for user registration
    first_name: str = Field(  # Validate first name
        ...,  # Make this field mandatory
        min_length=3,  # Require at least 3 characters
        pattern=r"^[A-Za-z]+$",  # Allow only English alphabets
        description="Mandatory. Minimum 3 alphabetic characters."  # Explain validation
    )
    last_name: str = Field(  # Validate last name
        ...,  # Make this field mandatory
        min_length=3,  # Require at least 3 characters
        pattern=r"^[A-Za-z]+$",  # Allow only English alphabets
        description="Mandatory. Minimum 3 alphabetic characters."  # Explain validation
    )
    email: EmailStr = Field(  # Validate email address
        ...,  # Make this field mandatory
        description="Mandatory. Must be a valid email address."  # Explain validation
    )
    password: str = Field(  # Define password field
    ...,  # Make password mandatory
    min_length=8,  # Require at least 8 characters
    description="Minimum 8 characters with uppercase, lowercase, number and special character."  # Explain password rules
)

@field_validator("password")  # Run custom validation on password
@classmethod  # Define this as a class-level validator
def validate_password(cls, value: str) -> str:  # Receive and validate password
    if not any(char.isupper() for char in value):  # Check for uppercase letter
        raise ValueError("Password must contain at least one uppercase letter")  # Reject invalid password

    if not any(char.islower() for char in value):  # Check for lowercase letter
        raise ValueError("Password must contain at least one lowercase letter")  # Reject invalid password

    if not any(char.isdigit() for char in value):  # Check for a number
        raise ValueError("Password must contain at least one number")  # Reject invalid password

    if not any(char in "@$!%*?&" for char in value):  # Check for an allowed special character
        raise ValueError("Password must contain at least one special character (@$!%*?&)")  # Reject invalid password

    if not all(char.isalnum() or char in "@$!%*?&" for char in value):  # Reject unsupported characters
        raise ValueError("Password contains unsupported special characters")  # Explain validation failure

    return value  # Return the validated password


class UserResponse(BaseModel):  # Schema for user details returned by API
    id: int  # User's unique ID
    first_name: str  # User's first name
    last_name: str  # User's last name
    email: EmailStr  # User's email address
    is_active: bool  # Account active status
    is_verified: bool  # Email verification status
    created_at: datetime  # Account creation timestamp

    model_config = ConfigDict(from_attributes=True)  # Allow conversion from SQLAlchemy models


class UserLogin(BaseModel):  # Schema for user login
    email: EmailStr = Field(  # Validate login email
        ...,  # Make this field mandatory
        description="Mandatory. Must be a valid email address."  # Explain validation
    )
    password: str = Field(  # Validate login password
        ...,  # Make this field mandatory
        min_length=1,  # Prevent an empty password
        description="Mandatory. Enter your account password."  # Explain validation
    )


class Token(BaseModel):  # Schema for authentication tokens
    access_token: str  # JWT access token
    refresh_token: str  # JWT refresh token
    token_type: str  # Token type, normally bearer
