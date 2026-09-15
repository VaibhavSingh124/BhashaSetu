"""
BhashaSetu - Database Layer
Provides connection interfaces and session management.
Database schemas, migrations, and storage logic will be implemented in subsequent steps.
"""

import os
from typing import Generator

# In Step 0, placeholders are defined without establishing live database connections
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./database/bhashasetu.db")


class Base:
    """
    Placeholder base class for ORM models.
    To be replaced with sqlalchemy.orm.DeclarativeBase in Step 1+.
    """
    pass


def get_db() -> Generator[None, None, None]:
    """
    Dependency generator for database sessions in FastAPI routes.
    Implementation of engine and sessionmaker deferred to Step 1+.
    """
    yield None
