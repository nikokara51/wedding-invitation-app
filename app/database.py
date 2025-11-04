import os
import sqlalchemy
from dotenv import load_dotenv
from app.models import metadata

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./invites.db")

# SQLAlchemy engine (sync) for table creation
engine = sqlalchemy.create_engine(
    DATABASE_URL.replace("+aiosqlite", ""),
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create tables if they don't exist
metadata.create_all(engine)
