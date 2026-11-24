from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

class RefreshToken(Base):
    __tablename__="RefreshTokens"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    token: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime)
