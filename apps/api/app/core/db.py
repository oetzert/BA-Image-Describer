from sqlmodel import SQLModel, create_engine, Session
from .config import settings
import os

def get_engine():
    # SQLite needs check_same_thread=False for async-ish web usage
    connect_args = {"check_same_thread": False} if settings.DATABASE_URL.startswith("sqlite") else {}
    return create_engine(settings.DATABASE_URL, connect_args=connect_args)

engine = get_engine()

def init_db():
    os.makedirs("./data", exist_ok=True)
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
