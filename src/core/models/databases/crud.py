from sqlalchemy.orm import Session

from . import models
from src.core.schemas.user import UserInDB


def get_user_by_user_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def delete_user_by_user_id(db: Session, user_id: int):
    try:
        query_result = db.query(models.User).filter(models.User.id == user_id).delete()
    except Exception:
        db.rollback()
    else:
        db.commit()
        return query_result


def delete_user_by_email(db: Session, email: str):
    try:
        query_result = db.query(models.User).filter(models.User.email == email).delete()
    except Exception:
        db.rollback()
    else:
        db.commit()
        return query_result


def delete_user_by_username(db: Session, username: str):
    try:
        query_result = db.query(models.User).filter(models.User.username == username).delete()
    except Exception:
        db.rollback()
    else:
        db.commit()
        return query_result


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserInDB):
    db_user = models.User(**user.dict())
    try:
        db.add(db_user)
    except Exception:
        db.rollback()
    else:
        db.commit()
        db.refresh(db_user)
        return True
