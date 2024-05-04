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


def create_security(db: Session, security: schemas.SecurityCreate):
    try:
        db_security = models.Security(code=security.code, name=security.name, price=security.price)
        db.add(db_security)
        db.commit()
        db.refresh(db_security)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create security")
    
    return db_security


def update_security(db: Session, security_id: int, price: int):
    try:
        db_security = db.query(models.Security).filter(models.Security.id == security_id).first()
        db_security.price = price
        db.commit()
        db.refresh(db_security)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to update security")
    
    return db_security


def delete_security(db: Session, security_id: int):
    try:
        db_security = db.query(models.Security).filter(models.Security.id == security_id).first()
        db.delete(db_security)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to delete security")
    
    return db_security
