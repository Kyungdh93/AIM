from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from src import crud, models, schemas
from src.database import SessionLocal, engine

from sqlalchemy.orm import Session

import json
from typing import Annotated
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == token).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return db_user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/users", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    crud.create_user(db, username=user.username, password=hashed_password)

    db_user = crud.get_user(db, username=user.username)
    crud.create_balance(db, user_id=db_user.id)
    return db_user


@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=form_data.username)
    if not db_user or not pwd_context.verify(form_data.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    crud.create_history(db, username=form_data.username, event='LOGIN')
    return {"access_token": db_user.username, "token_type": "bearer"}


@app.post("/logout")
def logout(user: schemas.UserLogout, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    crud.create_history(db, username=user.username, event='LOGOUT')
    return {"message": "Logout successful"}



@app.post("/securities", response_model=schemas.Security)
def create_security(security: schemas.SecurityCreate, db: Session = Depends(get_db)):
    db_securities = crud.get_securities(db)
    if not db_securities:
        with open('./init_securities.json', 'r') as file:
            init_securities = json.load(file)

        crud.create_init_securities(db, security, init_securities)
    
    db_security = crud.create_security(db, security)
    return db_security


@app.put("/securities/{security_id}", response_model=schemas.Security)
def update_security_price(security_id: int, price: int, db: Session = Depends(get_db)):
    db_security = crud.update_security(db, security_id=security_id, price=price)
    if not db_security:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Security not found")

    return db_security


@app.delete("/securities/{security_id}", response_model=schemas.Security)
def delete_security(security_id: int, db: Session = Depends(get_db)):
    db_security = crud.delete_security(db, security_id=security_id)
    if not db_security:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Security not found")
    
    return db_security


@app.get("/balance")
def get_balance(current_user: Annotated[schemas.User, Depends(get_current_active_user)], db: Session = Depends(get_db)):
    # user_balance = db.query(func.sum(models.Transaction.amount)).filter(models.Transaction.user_id == current_user.id).scalar()
    user_balance = crud.get_balance(db, user_id=current_user.id)
    if user_balance is None:
        user_balance = 0
    
    return {"user_id": current_user.id, "balance": user_balance}


if __name__ == "__main__":
	import uvicorn
	uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    # python -m main