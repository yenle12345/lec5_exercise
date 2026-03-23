from sqlalchemy.orm import Session
from fastapi import HTTPException
from repositories import user_repo
from core.security import hash_password, verify_password
from core.jwt import create_access_token

def register_user(db: Session, email: str, password: str):
    existing = user_repo.get_user_by_email(db, email)
    if existing:
        raise HTTPException(status_code=400, detail="Email exists")

    return user_repo.create_user(
        db,
        email=email,
        hashed_password=hash_password(password)
    )

def login_user(db: Session, email: str, password: str):
    user = user_repo.get_user_by_email(db, email)

    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(user.id)})
    return token