from fastapi import HTTPException, status

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from . import models, schemas


def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, password: str):
    try:
        db_user = models.User(username=username, password=password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user")


def create_balance(db: Session, user_id: int):
    try:
        db_balance = models.Balance(user_id=user_id, balance=0.0)
        db.add(db_balance)
        db.commit()
        db.refresh(db_balance)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create balance")
    

def create_history(db: Session, username: str, event: str):
    try:
        db_user_history = models.UserHistory(username=username, event=event)
        db.add(db_user_history)
        db.commit()
        db.refresh(db_user_history)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create history")
    

def get_balance(db: Session, user_id: int):
    return db.query(models.Balance).filter(models.Balance.user_id == user_id).first()

