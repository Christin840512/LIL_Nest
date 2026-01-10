from sqlalchemy.orm import Session, sessionmaker
from infrastructure.config.settings import get_settings
from sqlalchemy import create_engine

engine = create_engine(get_settings().DATABASE_URL)  
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
