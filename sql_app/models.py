import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from .database import Base


# Database models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

    users_history = relationship("UserHistory", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    portfolios = relationship("Portfolio", back_populates="user")
    balance_info = relationship("Balance", back_populates="user")


class UserHistory(Base):
    __tablename__ = "users_history"
    id = Column(Integer, primary_key=True, index=True)
    time = Column(DateTime(timezone=True), default=sqlalchemy.func.now())
    # user_id = Column(Integer, ForeignKey("users.id"))
    username = Column(Integer, ForeignKey("users.username"))
    event = Column(String)

    user = relationship("User", back_populates="users_history")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")