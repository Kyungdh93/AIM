from pydantic import BaseModel


# Balance
class Balance(BaseModel):
    user_id: int
    balance: int

    class Config:
        orm_mode = True


# User
class UserBase(BaseModel):
    username: str


class User(UserBase):
    id: int
    balance_info: list[Balance] = []

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class UserLogout(UserBase):
    pass


class UserHistory(BaseModel):
    username: str
    event: str

# Transaction
class TransactionBase(BaseModel):
    amount: int
    transaction_type: str


class Transaction(TransactionBase):
    # user_id: int
    username: str

    # 얘가 있어야 main.py 에서 return db_transaction 할 때 dict 형식으로 return 돼서 에러 안남 
    class Config:
        orm_mode = True

class TransactionCreate(TransactionBase):
    pass


# Portfolio
class PortfolioBase(BaseModel):
    risk_level: str


class Portfolio(PortfolioBase):
    portfolio: str
    class Config:
        orm_mode = True


class PortfolioCreate(PortfolioBase):
    pass


# Security
class SecurityBase(BaseModel):
    code: str
    name: str
    price: int


class Security(SecurityBase):
    class Config:
        orm_mode = True


class SecurityCreate(SecurityBase):
    pass

