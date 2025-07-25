from sqlalchemy.orm import Session
from . import models, schemas
from .auth import hash_password, verify_password

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(
	username=user.username,
	hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def update_user(db: Session, username: str, update_data: schemas.UserUpdate):
    user = get_user_by_username(db, username)
    if not user:
        return None
    if update_data.username:
        user.username = update_data.username
    if update_data.password:
        user.hashed_password = hash_password(update_data.password)
    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, username: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True
