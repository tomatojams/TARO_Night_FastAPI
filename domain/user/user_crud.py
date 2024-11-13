import bcrypt
from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from model import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_existing_user(db: Session, user_create: UserCreate):
    return (
        db.query(User)
        .filter((User.id == user_create.id) | (User.email == user_create.email))
        .first()
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user is None or not verify_password(password, user.password):
        return False
    return True
