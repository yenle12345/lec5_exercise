import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Lấy URL từ biến môi trường, mặc định là SQLite nếu không tìm thấy (để chạy test nhanh)
# Khi dùng Docker-compose, biến này sẽ là: postgresql://user:password@db:5432/todo_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data.db")

# Nếu dùng Postgres, engine không cần "check_same_thread"
# Nếu dùng SQLite, cần "check_same_thread": False để FastAPI hoạt động đa luồng
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    DATABASE_URL, 
    echo=True, 
    connect_args=connect_args
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()