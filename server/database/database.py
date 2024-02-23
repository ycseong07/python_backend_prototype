from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL") 

# echo=True: SQL 로그 활성화
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

try:
    with engine.connect() as conn:
        print("DB 연결 성공")
except Exception as e:
    print(f"DB 연결 실패: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()