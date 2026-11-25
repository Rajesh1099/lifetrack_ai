
from datetime import datetime  # Imports the datetime type.
from sqlalchemy import String, DateTime, ForeignKey  # Imports database column types and foreign keys.
from sqlalchemy.orm import Mapped, mapped_column  # Imports SQLAlchemy typed column definitions.
from app.database.base import Base  # Imports the shared SQLAlchemy model base.

class RefreshToken(Base):  # Defines the refresh token database model.
    __tablename__ = "refresh_tokens"  # Sets the PostgreSQL table name.

    id: Mapped[int] = mapped_column(primary_key=True)  # Creates the primary key.
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)  # Stores the SHA-256 hash of the refresh token.
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)  # Links the token to its user.
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # Stores the refresh session expiry time.
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)  # Stores when the token was revoked.
