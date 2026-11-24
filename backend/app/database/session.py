from sqlalchemy import create_engine
from collections.abc import Generator
from sqlalchemy.orm import sessionmaker,Session

from app.core.config import settings

DATABASE_URL = (
    f"postgresql+psycopg://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

#Creates SQLAlchemy's engine, which manages database connectivity and connection pooling.
engine=create_engine(DATABASE_URL,echo=settings.DEBUG)
#echo is a named parameter. We must explicitly identify it.


#Creates database sessions whenever our application needs to read or write data.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False, #A flush means SQLAlchemy sends pending database changes to PostgreSQL, but it does not permanently commit them yet.
    autocommit=False, #With autocommit=False, SQLAlchemy doesn't automatically commit each operation.
)

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

