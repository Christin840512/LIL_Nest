from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

engine = create_engine("postgresql+psycopg2://christin@localhost:5432/mydb")  
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
