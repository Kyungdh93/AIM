from pydantic import BaseModel


# Balance
class Balance(BaseModel):
    user_id: int
    balance: float

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

