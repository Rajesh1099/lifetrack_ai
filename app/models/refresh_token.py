import uuid  # Generates unique token-family IDs.
from datetime import datetime  # Imports the datetime type.
from sqlalchemy import String, DateTime, ForeignKey  # Imports database column types.
from sqlalchemy.orm import Mapped, mapped_column  # Imports SQLAlchemy ORM mapping tools.
from app.database.base import Base  # Imports the shared SQLAlchemy Base class.


class RefreshToken(Base):  # Defines the refresh-token database model.
    __tablename__ = "refresh_tokens"  # Sets the PostgreSQL table name.

    id: Mapped[int] = mapped_column(primary_key=True)  # Stores the primary key.
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)  # Stores the hashed refresh token.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # Links the token to its user.
    family_id: Mapped[str] = mapped_column(String(36), default=lambda: str(uuid.uuid4()), index=True, nullable=False)  # Groups refresh tokens from the same login session.
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # Stores the token expiry time.
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # Stores when the token was revoked.