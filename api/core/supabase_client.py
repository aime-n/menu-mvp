import os
from supabase import create_client, Client
from api.core.config import settings

url: str = settings.SUPABASE_URL.get_secret_value()
key: str = settings.SUPABASE_KEY.get_secret_value()
supabase: Client = create_client(url, key)



# api/core/database.py
# This file centralizes database connection logic.

from sqlmodel import create_engine, Session
from .config import settings

# Create the SQLAlchemy engine using the DATABASE_URL from settings
engine = create_engine(settings.DATABASE_URL, echo=False)

def get_session():
    """Dependency to get a database session for each request."""
    with Session(engine) as session:
        yield session