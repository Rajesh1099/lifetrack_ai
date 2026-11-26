
from datetime import datetime  # Imports the datetime type.
from sqlalchemy import String, DateTime  # Imports database column types.
from sqlalchemy.orm import Mapped, mapped_column  # Imports typed column definitions.
from app.database.base import Base  # Imports the shared SQLAlchemy model base.


class RevokedAccessToken(Base):  # Defines the revoked access-token database model.
    __tablename__ = "revoked_access_tokens"  # Sets the PostgreSQL table name.

    id: Mapped[int] = mapped_column(primary_key=True)  # Creates the primary key.
    token_id_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)  # Stores the SHA-256 hash of JWT jti.
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)  # Stores when the JWT expires.
    revoked_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)  # Stores when the JWT was revoked.
