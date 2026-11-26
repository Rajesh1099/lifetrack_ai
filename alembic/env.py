
from logging.config import fileConfig  # Import logging configuration support

from alembic import context  # Import Alembic migration context
from sqlalchemy import create_engine, pool  # Import SQLAlchemy engine and connection pool
from sqlalchemy.engine import URL  # Import database URL builder

from app.core.config import settings  # Import application settings
from app.database.base import Base  # Import shared SQLAlchemy model metadata

import app.models.user  # Register User model with SQLAlchemy metadata
import app.models.refresh_token  # Register RefreshToken model with SQLAlchemy metadata
import app.models.revoked_access_token  # Register RevokedAccessToken model with SQLAlchemy metadata

config = context.config  # Get Alembic configuration

if config.config_file_name is not None:  # Check whether Alembic config file exists
    fileConfig(config.config_file_name)  # Configure migration logging

target_metadata = Base.metadata  # Provide all registered models to Alembic

database_url = URL.create(  # Build PostgreSQL connection URL safely
    drivername="postgresql+psycopg",  # Specify PostgreSQL driver
    username=settings.DB_USER,  # Get database username
    password=settings.DB_PASSWORD,  # Get database password
    host=settings.DB_HOST,  # Get database host
    port=settings.DB_PORT,  # Get database port
    database=settings.DB_NAME,  # Get database name
)


def run_migrations_offline():  # Configure migrations without a live database connection
    context.configure(  # Configure Alembic migration environment
        url=database_url.render_as_string(hide_password=False),  # Provide database URL
        target_metadata=target_metadata,  # Provide model metadata
        literal_binds=True,  # Render SQL values directly
        dialect_opts={"paramstyle": "named"},  # Use named SQL parameters
    )

    with context.begin_transaction():  # Start migration transaction
        context.run_migrations()  # Execute migrations


def run_migrations_online():  # Configure migrations with a live database connection
    connectable = create_engine(  # Create SQLAlchemy database engine
        database_url,  # Use configured PostgreSQL URL
        poolclass=pool.NullPool,  # Avoid reusing database connections
    )

    with connectable.connect() as connection:  # Open database connection
        context.configure(  # Configure Alembic with active connection
            connection=connection,  # Provide database connection
            target_metadata=target_metadata,  # Provide model metadata
        )

        with context.begin_transaction():  # Start migration transaction
            context.run_migrations()  # Execute migrations

    connectable.dispose()  # Close and release database engine resources


if context.is_offline_mode():  # Check whether Alembic is running offline
    run_migrations_offline()  # Execute offline migration configuration
else:  # Otherwise run with a live database
    run_migrations_online()  # Execute online migration configuration
